"""
Inter-agent communication hub.

Single JSON file persisted under Game/shared/, guarded by OS-level file
locks. The legacy module had two redundant lock APIs (request_file_lock
and acquire_lock) and swallowed every exception with a bare log line.
This rewrite:

- Exposes one lock API (acquire_lock / release_lock).
- Reports failures via typed CommunicationError / FileLockError with codes.
- Reads/writes atomically: read-modify-write happens under a single LOCK_EX.
"""

from __future__ import annotations

import json
import os
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import portalocker

from .errors import Codes, CommunicationError, FileLockError
from .logging_setup import get_logger

logger = get_logger(__name__)

DEFAULT_STATE: dict[str, Any] = {
    "communications": [],
    "status_updates": [],
    "shared_context": {},
    "file_locks": {},
    "integration_points": [],
    "conflict_reports": [],
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CommunicationHub:
    state_file: Path = field(default_factory=lambda: Path("Game/shared/agent_communication.json"))
    max_status_updates: int = 200
    max_communications: int = 1000

    def __post_init__(self) -> None:
        self.state_file = Path(self.state_file)
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.state_file.exists():
                self._atomic_write(DEFAULT_STATE)
            else:
                self._heal()
        except OSError as exc:
            raise CommunicationError(
                "failed to initialize communication state",
                code=Codes.COMM_INIT_FAILED,
                cause=exc,
                context={"path": str(self.state_file)},
            ) from exc

    # ---- internal locking ----
    @contextmanager
    def _exclusive(self) -> Iterator[dict[str, Any]]:
        """Read-modify-write under a single exclusive lock."""
        try:
            with open(self.state_file, "r+", encoding="utf-8") as fh:
                portalocker.lock(fh, portalocker.LOCK_EX)
                try:
                    raw = fh.read()
                    data = json.loads(raw) if raw.strip() else dict(DEFAULT_STATE)
                    yield data
                    fh.seek(0)
                    json.dump(data, fh, indent=2, ensure_ascii=False)
                    fh.truncate()
                finally:
                    portalocker.unlock(fh)
        except FileNotFoundError as exc:
            raise CommunicationError(
                "state file disappeared",
                code=Codes.COMM_FILE_CORRUPT,
                cause=exc,
                context={"path": str(self.state_file)},
            ) from exc
        except json.JSONDecodeError as exc:
            raise CommunicationError(
                "state file is not valid JSON",
                code=Codes.COMM_FILE_CORRUPT,
                cause=exc,
                context={"path": str(self.state_file)},
            ) from exc
        except OSError as exc:
            raise CommunicationError(
                "failed to write communication state",
                code=Codes.COMM_WRITE_FAILED,
                cause=exc,
                context={"path": str(self.state_file)},
            ) from exc

    def _atomic_write(self, data: dict[str, Any]) -> None:
        tmp = self.state_file.with_suffix(self.state_file.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            portalocker.lock(fh, portalocker.LOCK_EX)
            try:
                json.dump(data, fh, indent=2, ensure_ascii=False)
            finally:
                portalocker.unlock(fh)
        os.replace(tmp, self.state_file)

    def _heal(self) -> None:
        """Ensure all required keys exist; recreate file if it's corrupt."""
        try:
            with open(self.state_file, "r", encoding="utf-8") as fh:
                portalocker.lock(fh, portalocker.LOCK_SH)
                try:
                    raw = fh.read()
                finally:
                    portalocker.unlock(fh)
            data = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            logger.warning("state file corrupt, recreating: %s", self.state_file)
            self._atomic_write(DEFAULT_STATE)
            return

        added = False
        for key, default in DEFAULT_STATE.items():
            if key not in data:
                data[key] = default if not isinstance(default, (list, dict)) else type(default)()
                added = True
        if added:
            self._atomic_write(data)

    # ---- public read API ----
    def snapshot(self) -> dict[str, Any]:
        try:
            with open(self.state_file, "r", encoding="utf-8") as fh:
                portalocker.lock(fh, portalocker.LOCK_SH)
                try:
                    return json.load(fh)
                finally:
                    portalocker.unlock(fh)
        except (OSError, json.JSONDecodeError) as exc:
            raise CommunicationError(
                "failed to read communication state",
                code=Codes.COMM_READ_FAILED,
                cause=exc,
                context={"path": str(self.state_file)},
            ) from exc

    # ---- messaging ----
    def send_message(self, sender: str, recipient: str, message: str, kind: str = "info") -> str:
        if not sender or not recipient or not message:
            raise CommunicationError(
                "send_message requires sender, recipient, message",
                code=Codes.COMM_INVALID_PAYLOAD,
                context={"sender": sender, "recipient": recipient},
            )
        msg_id = str(uuid.uuid4())
        with self._exclusive() as data:
            data["communications"].append(
                {
                    "id": msg_id,
                    "timestamp": _utcnow(),
                    "from_agent": sender,
                    "to_agent": recipient,
                    "message": message,
                    "type": kind,
                    "read": False,
                }
            )
            if len(data["communications"]) > self.max_communications:
                data["communications"] = data["communications"][-self.max_communications :]
        logger.info("message %s -> %s: %s", sender, recipient, message[:80])
        return msg_id

    def get_messages(self, recipient: str, *, unread_only: bool = True) -> list[dict[str, Any]]:
        data = self.snapshot()
        return [
            m
            for m in data.get("communications", [])
            if m.get("to_agent") == recipient and (not unread_only or not m.get("read"))
        ]

    def mark_read(self, message_id: str) -> bool:
        with self._exclusive() as data:
            for m in data.get("communications", []):
                if m.get("id") == message_id:
                    m["read"] = True
                    return True
        return False

    # ---- status ----
    def update_status(self, agent: str, status: str, details: dict[str, Any] | None = None) -> None:
        if not agent or not status:
            raise CommunicationError(
                "update_status requires agent and status",
                code=Codes.COMM_INVALID_PAYLOAD,
            )
        with self._exclusive() as data:
            data["status_updates"].append(
                {
                    "timestamp": _utcnow(),
                    "agent": agent,
                    "status": status,
                    "details": details or {},
                }
            )
            if len(data["status_updates"]) > self.max_status_updates:
                data["status_updates"] = data["status_updates"][-self.max_status_updates :]

    def get_status(self, agent: str | None = None) -> list[dict[str, Any]]:
        data = self.snapshot()
        updates = data.get("status_updates", [])
        if agent is None:
            return updates
        return [u for u in updates if u.get("agent") == agent]

    # ---- shared context ----
    def set_context(self, key: str, value: Any) -> None:
        with self._exclusive() as data:
            data["shared_context"][key] = value

    def get_context(self, key: str | None = None) -> Any:
        data = self.snapshot()
        ctx = data.get("shared_context", {})
        return ctx if key is None else ctx.get(key)

    # ---- file locks (single API) ----
    def acquire_lock(self, agent: str, file_path: str) -> bool:
        with self._exclusive() as data:
            locks = data["file_locks"]
            if file_path in locks:
                holder = locks[file_path].get("agent")
                if holder != agent:
                    return False
            locks[file_path] = {"agent": agent, "timestamp": _utcnow()}
            return True

    def release_lock(self, agent: str, file_path: str) -> bool:
        with self._exclusive() as data:
            locks = data["file_locks"]
            existing = locks.get(file_path)
            if existing and existing.get("agent") == agent:
                del locks[file_path]
                return True
        return False

    def lock_holder(self, file_path: str) -> str | None:
        data = self.snapshot()
        info = data.get("file_locks", {}).get(file_path)
        return info.get("agent") if info else None

    @contextmanager
    def file_lock(self, agent: str, file_path: str) -> Iterator[None]:
        if not self.acquire_lock(agent, file_path):
            holder = self.lock_holder(file_path)
            raise FileLockError(
                f"file is locked by {holder!r}",
                code=Codes.FILE_LOCK_HELD,
                context={"agent": agent, "file_path": file_path, "holder": holder},
            )
        try:
            yield
        finally:
            self.release_lock(agent, file_path)

    # ---- integration points ----
    def report_integration_point(self, agent: str, component: str, interface: dict[str, Any]) -> None:
        with self._exclusive() as data:
            data["integration_points"].append(
                {
                    "timestamp": _utcnow(),
                    "agent": agent,
                    "component": component,
                    "interface": interface,
                }
            )

    def report_conflict(self, agent: str, description: str, details: dict[str, Any] | None = None) -> None:
        with self._exclusive() as data:
            data["conflict_reports"].append(
                {
                    "timestamp": _utcnow(),
                    "agent": agent,
                    "description": description,
                    "details": details or {},
                }
            )


_default_hub: CommunicationHub | None = None


def default_hub() -> CommunicationHub:
    global _default_hub
    if _default_hub is None:
        _default_hub = CommunicationHub()
    return _default_hub
