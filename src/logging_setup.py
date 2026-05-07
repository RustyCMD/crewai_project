"""
Logging setup. UTF-8 throughout, no emoji-replacement hack.

The previous implementation hand-rewrote a fixed list of emoji to ASCII.
That broke for any character outside the table. Here we just use UTF-8
file/stream handlers and let the OS deal with it; on Windows we reconfigure
stdout/stderr to UTF-8.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
from pathlib import Path

from .errors import Codes, ConfigError

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _coerce_level(level: str | int) -> int:
    if isinstance(level, int):
        return level
    upper = (level or "INFO").upper()
    if upper not in VALID_LEVELS:
        raise ConfigError(
            f"log level {level!r} not in {sorted(VALID_LEVELS)}",
            code=Codes.CONFIG_INVALID_LOG_LEVEL,
            context={"requested": level},
        )
    return getattr(logging, upper)


def _ensure_utf8_streams() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def setup_logging(
    level: str | int = "INFO",
    log_file: str | os.PathLike[str] | None = "logs/crewai.log",
    *,
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    """Configure root logger. Idempotent — safe to call multiple times."""
    _ensure_utf8_streams()
    numeric_level = _coerce_level(level)

    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    formatter = logging.Formatter(fmt, datefmt=datefmt)

    handlers: list[logging.Handler] = []

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    handlers.append(console)

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    for handler in handlers:
        handler.setLevel(numeric_level)
        root.addHandler(handler)

    root.setLevel(numeric_level)
    return root


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
