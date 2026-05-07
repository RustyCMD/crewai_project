"""
Project configuration loaded from environment variables.

A single Settings dataclass is the only source of truth. Validate once at
startup; failures raise ConfigError with a typed code so the launcher can
produce a precise message.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from .errors import Codes, ConfigError

PLACEHOLDERS = {"", "your_gemini_api_key_here", "changeme", "todo"}


def _required(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise ConfigError(
            f"environment variable {name} is not set",
            code=Codes.CONFIG_MISSING_API_KEY,
            context={"variable": name},
        )
    if value.strip().lower() in PLACEHOLDERS:
        raise ConfigError(
            f"environment variable {name} still has placeholder value",
            code=Codes.CONFIG_PLACEHOLDER_API_KEY,
            context={"variable": name},
        )
    return value


def _optional(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    model: str = "gemini/gemini-2.5-flash-lite"
    embed_model: str = "models/embedding-001"
    log_level: str = "INFO"
    log_file: str = "logs/crewai.log"
    game_title: str = "Idle Adventure"
    game_version: str = "1.0.0"
    project_root: Path = field(default_factory=Path.cwd)
    comm_file: Path = field(default_factory=lambda: Path("Game/shared/agent_communication.json"))

    @classmethod
    def load(cls, *, dotenv_path: str | os.PathLike[str] | None = None) -> "Settings":
        load_dotenv(dotenv_path=dotenv_path, override=False)
        return cls(
            gemini_api_key=_required("GEMINI_API_KEY"),
            model=_optional("GEMINI_MODEL", "gemini/gemini-2.5-flash-lite"),
            embed_model=_optional("GEMINI_EMBED_MODEL", "models/embedding-001"),
            log_level=_optional("LOG_LEVEL", "INFO"),
            log_file=_optional("LOG_FILE", "logs/crewai.log"),
            game_title=_optional("GAME_TITLE", "Idle Adventure"),
            game_version=_optional("GAME_VERSION", "1.0.0"),
        )
