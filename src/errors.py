"""
Centralized error codes and exception hierarchy.

Every error raised by this project carries a stable code so log lines and
user-facing messages immediately identify the subsystem at fault.

Code ranges:
    E1xxx - Configuration / environment
    E2xxx - LLM / model API
    E3xxx - Inter-agent communication hub
    E4xxx - File I/O and locking
    E5xxx - Crew / task orchestration
    E6xxx - GUI / dashboard
    E9xxx - Unclassified / wrapped third-party failures
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorCode:
    code: str
    description: str

    def __str__(self) -> str:
        return self.code


class Codes:
    # E1xxx - configuration
    CONFIG_MISSING_API_KEY = ErrorCode("E1001", "Required API key is not set")
    CONFIG_PLACEHOLDER_API_KEY = ErrorCode("E1002", "API key still has placeholder value")
    CONFIG_INVALID_LOG_LEVEL = ErrorCode("E1003", "Invalid log level requested")
    CONFIG_MISSING_FILE = ErrorCode("E1004", "Required project file is missing")
    CONFIG_INVALID_VALUE = ErrorCode("E1005", "Configuration value is invalid")

    # E2xxx - LLM / model
    LLM_INIT_FAILED = ErrorCode("E2001", "Failed to initialize LLM client")
    LLM_REQUEST_FAILED = ErrorCode("E2002", "LLM request failed")

    # E3xxx - communication hub
    COMM_INIT_FAILED = ErrorCode("E3001", "Failed to initialize communication hub")
    COMM_FILE_CORRUPT = ErrorCode("E3002", "Communication state file is corrupt")
    COMM_READ_FAILED = ErrorCode("E3003", "Failed to read communication state")
    COMM_WRITE_FAILED = ErrorCode("E3004", "Failed to write communication state")
    COMM_INVALID_PAYLOAD = ErrorCode("E3005", "Communication payload failed validation")

    # E4xxx - file / locking
    FILE_LOCK_HELD = ErrorCode("E4001", "File lock is already held by another agent")
    FILE_LOCK_TIMEOUT = ErrorCode("E4002", "Timed out waiting for file lock")
    FILE_WRITE_FAILED = ErrorCode("E4003", "Failed to write file")
    FILE_READ_FAILED = ErrorCode("E4004", "Failed to read file")
    FILE_PATH_INVALID = ErrorCode("E4005", "File path is invalid")

    # E5xxx - crew / task
    CREW_INIT_FAILED = ErrorCode("E5001", "Failed to initialize crew")
    CREW_KICKOFF_FAILED = ErrorCode("E5002", "Crew execution failed")
    TASK_INVALID = ErrorCode("E5003", "Task definition is invalid")
    AGENT_INVALID = ErrorCode("E5004", "Agent definition is invalid")

    # E6xxx - GUI
    GUI_INIT_FAILED = ErrorCode("E6001", "Failed to initialize dashboard")
    GUI_UPDATE_FAILED = ErrorCode("E6002", "Dashboard refresh failed")
    GUI_PROCESS_FAILED = ErrorCode("E6003", "Failed to manage agent subprocess")

    # E9xxx - generic
    UNEXPECTED = ErrorCode("E9001", "Unexpected error")
    UNHANDLED = ErrorCode("E9002", "Unhandled third-party exception")


class CrewAIError(Exception):
    """Base exception. Always carries a stable error code."""

    code: ErrorCode = Codes.UNEXPECTED

    def __init__(
        self,
        message: str,
        *,
        code: ErrorCode | None = None,
        cause: BaseException | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.code = code or self.code
        self.context = context or {}
        self._cause = cause
        full = f"[{self.code.code}] {message}"
        if context:
            full += f" | context={context}"
        if cause is not None:
            full += f" | cause={type(cause).__name__}: {cause}"
        super().__init__(full)
        if cause is not None:
            self.__cause__ = cause


class ConfigError(CrewAIError):
    code = Codes.CONFIG_INVALID_VALUE


class LLMError(CrewAIError):
    code = Codes.LLM_INIT_FAILED


class CommunicationError(CrewAIError):
    code = Codes.COMM_INIT_FAILED


class FileLockError(CrewAIError):
    code = Codes.FILE_LOCK_HELD


class CrewError(CrewAIError):
    code = Codes.CREW_INIT_FAILED


class GUIError(CrewAIError):
    code = Codes.GUI_INIT_FAILED
