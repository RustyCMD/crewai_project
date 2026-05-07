"""
Subprocess controller for the agent crew.

Isolates the dashboard from any direct CrewAI imports so that GUI failures
never take down the agents. Exposes a small command interface that the GUI
panels consume.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
from pathlib import Path

from ..errors import Codes, GUIError
from ..logging_setup import get_logger

logger = get_logger(__name__)


class AgentRunner:
    """Owns the lifecycle of the agent subprocess."""

    def __init__(self, *, mode: str = "parallel", project_root: Path | None = None) -> None:
        self.mode = mode
        self.project_root = project_root or Path.cwd()
        self._process: subprocess.Popen[bytes] | None = None

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    @property
    def pid(self) -> int | None:
        return self._process.pid if self.running else None

    def start(self) -> int:
        if self.running:
            return self._process.pid  # type: ignore[union-attr]
        try:
            cmd = [sys.executable, "-m", "src.cli", "--mode", self.mode, "--no-menu"]
            kwargs: dict = dict(cwd=str(self.project_root))
            if sys.platform == "win32":
                kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            else:
                kwargs["stdout"] = subprocess.DEVNULL
                kwargs["stderr"] = subprocess.DEVNULL
                kwargs["preexec_fn"] = os.setsid
            self._process = subprocess.Popen(cmd, **kwargs)
            logger.info("agent subprocess started pid=%s mode=%s", self._process.pid, self.mode)
            return self._process.pid
        except OSError as exc:
            raise GUIError(
                "failed to start agent subprocess",
                code=Codes.GUI_PROCESS_FAILED,
                cause=exc,
                context={"mode": self.mode},
            ) from exc

    def stop(self, *, timeout: float = 5.0) -> None:
        if not self.running:
            return
        proc = self._process
        assert proc is not None
        try:
            if sys.platform == "win32":
                proc.terminate()
            else:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                logger.warning("agent did not exit within %.1fs, killing", timeout)
                proc.kill()
                proc.wait(timeout=timeout)
        except OSError as exc:
            raise GUIError(
                "failed to stop agent subprocess",
                code=Codes.GUI_PROCESS_FAILED,
                cause=exc,
                context={"pid": proc.pid},
            ) from exc
        finally:
            self._process = None
