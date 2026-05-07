"""Dashboard state model. Tk-free so it's testable."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DashboardState:
    session_start: datetime = field(default_factory=datetime.now)
    agents_running: bool = False
    agent_pid: int | None = None
    last_error_code: str | None = None
    last_error_message: str | None = None

    # mirrored from comms hub
    status_updates: list[dict[str, Any]] = field(default_factory=list)
    communications: list[dict[str, Any]] = field(default_factory=list)
    file_locks: dict[str, dict[str, Any]] = field(default_factory=dict)
    integration_points: list[dict[str, Any]] = field(default_factory=list)
    conflict_reports: list[dict[str, Any]] = field(default_factory=list)
    shared_context: dict[str, Any] = field(default_factory=dict)

    def latest_status_per_agent(self) -> dict[str, dict[str, Any]]:
        latest: dict[str, dict[str, Any]] = {}
        for u in self.status_updates:
            agent = u.get("agent")
            if not agent:
                continue
            latest[agent] = u
        return latest

    def session_duration(self) -> str:
        delta = datetime.now() - self.session_start
        seconds = int(delta.total_seconds())
        hours, rem = divmod(seconds, 3600)
        minutes, secs = divmod(rem, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
