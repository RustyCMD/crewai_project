"""
Collaborative tools that wrap the communication hub.

Replacement for collaborative_tools.py. Bug fixes vs the original:
  * The original used os.makedirs(os.path.dirname(file_path)) which crashed
    when file_path had no directory component.
  * The original released file locks on writes but never blocked reads.
  * Bare excepts and emoji prefixes are replaced with structured returns and
    error codes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from crewai.tools.base_tool import BaseTool

from .comms import CommunicationHub, default_hub
from .errors import Codes, CrewAIError, FileLockError
from .logging_setup import get_logger

logger = get_logger(__name__)


def _safe_mkdir(path: Path) -> None:
    parent = path.parent
    if str(parent) and parent != Path(""):
        parent.mkdir(parents=True, exist_ok=True)


class CollaborativeFileWriterTool(BaseTool):
    name: str = "collaborative_file_writer"
    description: str = "Write a file under a coordinated lock and notify the team."

    def _run(self, file_path: str, content: str, agent_name: str = "agent") -> str:
        hub = default_hub()
        path = Path(file_path)
        try:
            with hub.file_lock(agent_name, str(path)):
                action = "modified" if path.exists() else "created"
                _safe_mkdir(path)
                path.write_text(content, encoding="utf-8")
                hub.send_message(
                    agent_name, "all", f"{action} {path}", "file_change"
                )
                hub.update_status(
                    agent_name,
                    f"{action} {path}",
                    {"file": str(path), "lines": content.count("\n") + 1, "action": action},
                )
            return f"OK: {action} {path}"
        except FileLockError as exc:
            logger.warning("%s", exc)
            return f"LOCKED [{exc.code.code}]: {path} held by {exc.context.get('holder')}"
        except CrewAIError as exc:
            logger.error("%s", exc)
            return f"ERROR [{exc.code.code}]: {exc}"
        except OSError as exc:
            logger.exception("file write failed")
            return f"ERROR [{Codes.FILE_WRITE_FAILED.code}]: {exc}"


class TeamCommunicationTool(BaseTool):
    name: str = "team_communication"
    description: str = (
        "Coordinate with the team. Actions: send_message, get_messages, request_review, share_progress."
    )

    def _run(self, action: str, **kwargs: Any) -> str:
        hub = default_hub()
        try:
            if action == "send_message":
                hub.send_message(
                    kwargs.get("from_agent", "agent"),
                    kwargs.get("to_agent", "all"),
                    kwargs.get("message", ""),
                    kwargs.get("type", "info"),
                )
                return "OK: message sent"

            if action == "get_messages":
                msgs = hub.get_messages(kwargs.get("agent_name", "agent"))
                if not msgs:
                    return "No new messages"
                lines = []
                for m in msgs:
                    lines.append(f"- {m['from_agent']}: {m['message']}")
                    hub.mark_read(m["id"])
                return "\n".join(lines)

            if action == "request_review":
                hub.send_message(
                    kwargs.get("from_agent", "agent"),
                    kwargs.get("reviewer", "qa_engineer"),
                    f"please review {kwargs.get('file_path', '<unknown>')}",
                    "code_review_request",
                )
                return "OK: review requested"

            if action == "share_progress":
                agent = kwargs.get("agent_name", "agent")
                progress = kwargs.get("progress", "")
                hub.update_status(agent, progress, kwargs.get("details") or {})
                hub.send_message(agent, "all", f"progress: {progress}", "progress")
                return "OK: progress shared"

            # Treat the action string as a free-form broadcast.
            hub.send_message(kwargs.get("from_agent", "agent"), "all", action, "info")
            return "OK: broadcast sent"
        except CrewAIError as exc:
            logger.error("%s", exc)
            return f"ERROR [{exc.code.code}]: {exc}"


class IntegrationCoordinatorTool(BaseTool):
    name: str = "integration_coordinator"
    description: str = (
        "Coordinate integration. Actions: register_interface, check_dependencies, report_conflict."
    )

    def _run(self, action: str, **kwargs: Any) -> str:
        hub = default_hub()
        try:
            if action == "register_interface":
                hub.report_integration_point(
                    kwargs.get("agent_name", "agent"),
                    kwargs.get("component", ""),
                    kwargs.get("interface") or {},
                )
                return f"OK: interface registered for {kwargs.get('component', '?')}"

            if action == "check_dependencies":
                target = kwargs.get("component", "")
                points = hub.snapshot().get("integration_points", [])
                deps = [
                    p for p in points
                    if target in (p.get("interface") or {}).get("dependencies", [])
                ]
                if not deps:
                    return f"OK: no dependencies for {target}"
                return "\n".join(f"- {d['component']} by {d['agent']}" for d in deps)

            if action == "report_conflict":
                hub.report_conflict(
                    kwargs.get("agent_name", "agent"),
                    kwargs.get("conflict", "unspecified"),
                    kwargs.get("details") or {},
                )
                return "OK: conflict reported"

            hub.send_message(kwargs.get("agent_name", "agent"), "all", f"integration: {action}", "integration")
            return "OK: integration broadcast sent"
        except CrewAIError as exc:
            logger.error("%s", exc)
            return f"ERROR [{exc.code.code}]: {exc}"


class ProjectStatusTool(BaseTool):
    name: str = "project_status"
    description: str = "Read team status. Actions: team_status, file_status, integration_status."

    def _run(self, action: str = "team_status", **_: Any) -> str:
        hub = default_hub()
        try:
            data = hub.snapshot()
            if action == "file_status":
                locks = data.get("file_locks", {})
                if not locks:
                    return "No files locked"
                return "\n".join(f"- {p} locked by {info['agent']}" for p, info in locks.items())

            if action == "integration_status":
                points = data.get("integration_points", [])[-10:]
                if not points:
                    return "No integration points"
                return "\n".join(f"- {p['component']} ({p['agent']})" for p in points)

            # default = team_status
            updates = data.get("status_updates", [])[-20:]
            if not updates:
                return "No status updates"
            latest: dict[str, dict[str, Any]] = {}
            for u in updates:
                latest[u["agent"]] = u
            return "\n".join(f"- {a}: {u['status']}" for a, u in latest.items())
        except CrewAIError as exc:
            logger.error("%s", exc)
            return f"ERROR [{exc.code.code}]: {exc}"


def make_collab_toolset(hub: CommunicationHub | None = None) -> list[BaseTool]:
    """Tools share the default hub unless one is passed (mainly for tests)."""
    if hub is not None:
        # default_hub is module-level singleton; tests can replace it.
        from . import comms

        comms._default_hub = hub
    return [
        CollaborativeFileWriterTool(),
        TeamCommunicationTool(),
        IntegrationCoordinatorTool(),
        ProjectStatusTool(),
    ]
