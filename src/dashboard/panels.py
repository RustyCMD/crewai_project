"""Reusable panel widgets for the dashboard."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Iterable

from .state import DashboardState
from .theme import Palette


class BasePanel(ttk.Frame):
    title: str = ""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="TFrame")
        if self.title:
            ttk.Label(self, text=self.title, style="Header.TLabel").pack(
                anchor="w", padx=8, pady=(8, 4), fill="x"
            )

    def refresh(self, state: DashboardState) -> None:  # pragma: no cover - overridden
        raise NotImplementedError


class AgentStatusPanel(BasePanel):
    title = "Agent Status"

    columns = ("agent", "status", "updated")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=10)
        self.tree.heading("agent", text="Agent")
        self.tree.heading("status", text="Status")
        self.tree.heading("updated", text="Updated")
        self.tree.column("agent", width=180, anchor="w")
        self.tree.column("status", width=320, anchor="w")
        self.tree.column("updated", width=140, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def refresh(self, state: DashboardState) -> None:
        self.tree.delete(*self.tree.get_children())
        for agent, update in sorted(state.latest_status_per_agent().items()):
            self.tree.insert(
                "",
                "end",
                values=(agent, update.get("status", "?"), update.get("timestamp", "")[:19]),
            )


class CommunicationsPanel(BasePanel):
    title = "Recent Communications"

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.text = tk.Text(
            self,
            background=Palette.SURFACE,
            foreground=Palette.TEXT,
            insertbackground=Palette.TEXT,
            relief="flat",
            borderwidth=0,
            wrap="word",
            font=("Consolas", 9),
            height=12,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text.tag_config("from", foreground=Palette.ACCENT, font=("Consolas", 9, "bold"))
        self.text.tag_config("warn", foreground=Palette.WARN)
        self.text.tag_config("err", foreground=Palette.DANGER)
        self.text.config(state="disabled")

    def refresh(self, state: DashboardState) -> None:
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        for entry in state.communications[-50:]:
            ts = (entry.get("timestamp", "") or "")[:19]
            sender = entry.get("from_agent", "?")
            recipient = entry.get("to_agent", "?")
            kind = entry.get("type", "info")
            tag = "err" if kind == "conflict" else "warn" if kind == "code_review_request" else "from"
            self.text.insert("end", f"[{ts}] {sender} -> {recipient}: ", tag)
            self.text.insert("end", f"{entry.get('message', '')}\n")
        self.text.config(state="disabled")
        self.text.see("end")


class FileLocksPanel(BasePanel):
    title = "Active File Locks"

    columns = ("path", "agent", "since")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=8)
        self.tree.heading("path", text="Path")
        self.tree.heading("agent", text="Held By")
        self.tree.heading("since", text="Since")
        self.tree.column("path", width=380)
        self.tree.column("agent", width=160)
        self.tree.column("since", width=140)
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def refresh(self, state: DashboardState) -> None:
        self.tree.delete(*self.tree.get_children())
        for path, info in state.file_locks.items():
            self.tree.insert(
                "",
                "end",
                values=(path, info.get("agent", "?"), (info.get("timestamp", "") or "")[:19]),
            )


class IntegrationPanel(BasePanel):
    title = "Integration Points"

    columns = ("component", "agent", "deps")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=10)
        self.tree.heading("component", text="Component")
        self.tree.heading("agent", text="Owner")
        self.tree.heading("deps", text="Dependencies")
        self.tree.column("component", width=220)
        self.tree.column("agent", width=160)
        self.tree.column("deps", width=320)
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def refresh(self, state: DashboardState) -> None:
        self.tree.delete(*self.tree.get_children())
        for point in state.integration_points[-30:]:
            interface = point.get("interface") or {}
            deps: Iterable[str] = interface.get("dependencies", []) or []
            self.tree.insert(
                "",
                "end",
                values=(point.get("component", "?"), point.get("agent", "?"), ", ".join(deps)),
            )


class ConflictsPanel(BasePanel):
    title = "Conflicts"

    columns = ("when", "agent", "description")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=8)
        self.tree.heading("when", text="When")
        self.tree.heading("agent", text="Reporter")
        self.tree.heading("description", text="Description")
        self.tree.column("when", width=140)
        self.tree.column("agent", width=160)
        self.tree.column("description", width=480)
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def refresh(self, state: DashboardState) -> None:
        self.tree.delete(*self.tree.get_children())
        for entry in state.conflict_reports[-30:]:
            self.tree.insert(
                "",
                "end",
                values=(
                    (entry.get("timestamp", "") or "")[:19],
                    entry.get("agent", "?"),
                    entry.get("description", ""),
                ),
            )
