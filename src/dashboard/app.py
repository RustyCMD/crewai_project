"""Dashboard application — modular MVC tkinter rewrite."""

from __future__ import annotations

import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from ..comms import CommunicationHub
from ..errors import Codes, CrewAIError, GUIError
from ..logging_setup import get_logger
from .agent_runner import AgentRunner
from .panels import (
    AgentStatusPanel,
    CommunicationsPanel,
    ConflictsPanel,
    FileLocksPanel,
    IntegrationPanel,
)
from .state import DashboardState
from .theme import Palette, apply_theme

logger = get_logger(__name__)

REFRESH_MS = 1500


class DashboardApp:
    def __init__(self, *, mode: str = "parallel", hub: CommunicationHub | None = None) -> None:
        self.root = tk.Tk()
        self.root.title("CrewAI Collaboration Dashboard")
        self.root.geometry("1280x780")
        self.root.configure(bg=Palette.BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        try:
            apply_theme(self.root)
        except tk.TclError as exc:
            raise GUIError(
                "failed to apply tkinter theme",
                code=Codes.GUI_INIT_FAILED,
                cause=exc,
            ) from exc

        self.state = DashboardState()
        self.hub = hub or CommunicationHub()
        self.runner = AgentRunner(mode=mode)
        self._stop_event = threading.Event()

        self._build_ui()
        self._start_polling_thread()
        self.root.after(REFRESH_MS, self._refresh_ui)

    # ---------- UI construction ----------
    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, style="TFrame")
        header.pack(fill="x", padx=12, pady=(12, 6))

        title = ttk.Label(header, text="CrewAI Collaboration Dashboard", style="Title.TLabel")
        title.pack(side="left")

        controls = ttk.Frame(header, style="TFrame")
        controls.pack(side="right")

        self.start_btn = ttk.Button(controls, text="Start Agents", style="Success.TButton", command=self._on_start)
        self.start_btn.pack(side="left", padx=(0, 6))

        self.stop_btn = ttk.Button(controls, text="Stop Agents", style="Danger.TButton", command=self._on_stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 6))

        self.reset_btn = ttk.Button(controls, text="Reset View", style="Accent.TButton", command=self._on_reset)
        self.reset_btn.pack(side="left")

        meta = ttk.Frame(self.root, style="TFrame")
        meta.pack(fill="x", padx=12)
        self.session_label = ttk.Label(meta, text="", style="Muted.TLabel")
        self.session_label.pack(side="left")
        self.error_label = ttk.Label(meta, text="", style="Muted.TLabel")
        self.error_label.pack(side="right")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=(8, 8))

        self.agent_panel = AgentStatusPanel(notebook)
        self.comm_panel = CommunicationsPanel(notebook)
        self.locks_panel = FileLocksPanel(notebook)
        self.integration_panel = IntegrationPanel(notebook)
        self.conflicts_panel = ConflictsPanel(notebook)

        notebook.add(self.agent_panel, text="Agents")
        notebook.add(self.comm_panel, text="Messages")
        notebook.add(self.locks_panel, text="File Locks")
        notebook.add(self.integration_panel, text="Integration")
        notebook.add(self.conflicts_panel, text="Conflicts")

        self.status_bar = ttk.Label(self.root, text="Idle", style="Status.TLabel")
        self.status_bar.pack(side="bottom", fill="x", padx=12, pady=(0, 8))

    # ---------- background polling ----------
    def _start_polling_thread(self) -> None:
        thread = threading.Thread(target=self._poll_loop, name="hub-poll", daemon=True)
        thread.start()

    def _poll_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                snapshot = self.hub.snapshot()
                self.state.status_updates = snapshot.get("status_updates", [])
                self.state.communications = snapshot.get("communications", [])
                self.state.file_locks = snapshot.get("file_locks", {})
                self.state.integration_points = snapshot.get("integration_points", [])
                self.state.conflict_reports = snapshot.get("conflict_reports", [])
                self.state.shared_context = snapshot.get("shared_context", {})
            except CrewAIError as exc:
                self.state.last_error_code = exc.code.code
                self.state.last_error_message = str(exc)
                logger.warning("hub poll failed: %s", exc)
            except Exception as exc:  # noqa: BLE001 - resilience for poll thread
                self.state.last_error_code = Codes.GUI_UPDATE_FAILED.code
                self.state.last_error_message = f"{type(exc).__name__}: {exc}"
                logger.exception("unexpected poll failure")
            self._stop_event.wait(REFRESH_MS / 1000)

    # ---------- refresh ----------
    def _refresh_ui(self) -> None:
        try:
            self.session_label.config(
                text=f"Session: {self.state.session_start.strftime('%Y-%m-%d %H:%M:%S')}    "
                     f"Uptime: {self.state.session_duration()}    "
                     f"Agents: {'running' if self.runner.running else 'stopped'}"
            )
            if self.state.last_error_code:
                self.error_label.config(
                    text=f"[{self.state.last_error_code}] {self.state.last_error_message}",
                    foreground=Palette.DANGER,
                )
            else:
                self.error_label.config(text="", foreground=Palette.MUTED)

            self.state.agents_running = self.runner.running
            self.state.agent_pid = self.runner.pid
            self.start_btn.state(["disabled"] if self.runner.running else ["!disabled"])
            self.stop_btn.state(["!disabled"] if self.runner.running else ["disabled"])

            self.agent_panel.refresh(self.state)
            self.comm_panel.refresh(self.state)
            self.locks_panel.refresh(self.state)
            self.integration_panel.refresh(self.state)
            self.conflicts_panel.refresh(self.state)

            self.status_bar.config(
                text=f"OK | last refresh {datetime.now().strftime('%H:%M:%S')}"
            )
        except Exception as exc:  # noqa: BLE001 - never let refresh kill the loop
            logger.exception("refresh failed")
            self.status_bar.config(
                text=f"[{Codes.GUI_UPDATE_FAILED.code}] refresh failed: {exc}"
            )
        finally:
            self.root.after(REFRESH_MS, self._refresh_ui)

    # ---------- button handlers ----------
    def _on_start(self) -> None:
        try:
            pid = self.runner.start()
            self.status_bar.config(text=f"Agent process started (pid={pid})")
        except GUIError as exc:
            messagebox.showerror(f"[{exc.code.code}] Failed to start", str(exc))

    def _on_stop(self) -> None:
        try:
            self.runner.stop()
            self.status_bar.config(text="Agent process stopped")
        except GUIError as exc:
            messagebox.showerror(f"[{exc.code.code}] Failed to stop", str(exc))

    def _on_reset(self) -> None:
        self.state = DashboardState()

    def _on_close(self) -> None:
        self._stop_event.set()
        try:
            self.runner.stop()
        except GUIError as exc:
            logger.warning("error stopping agents on close: %s", exc)
        self.root.destroy()

    def run(self) -> None:
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_close()


def run_dashboard(mode: str = "parallel") -> None:
    DashboardApp(mode=mode).run()
