"""
Shared LLM and tool factories.

The legacy code re-instantiated the same Gemini LLM and CodeDocsSearchTool
config in every agent file. We centralize it here so changing the model
or embedder is a single edit.
"""

from __future__ import annotations

from functools import lru_cache

from crewai import LLM
from crewai_tools import (
    CodeDocsSearchTool,
    DirectorySearchTool,
    FileReadTool,
    FileWriterTool,
)

from .config import Settings
from .errors import Codes, LLMError


def make_llm(settings: Settings, *, temperature: float = 0.5, max_tokens: int = 8192) -> LLM:
    try:
        return LLM(
            model=settings.model,
            api_key=settings.gemini_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:  # noqa: BLE001 - wrap third-party
        raise LLMError(
            "failed to construct LLM client",
            code=Codes.LLM_INIT_FAILED,
            cause=exc,
            context={"model": settings.model, "temperature": temperature},
        ) from exc


def _docs_tool_config(settings: Settings, temperature: float) -> dict:
    return dict(
        llm=dict(
            provider="google-generativeai",
            config=dict(
                model=settings.model,
                api_key=settings.gemini_api_key,
                temperature=temperature,
            ),
        ),
        embedder=dict(
            provider="google-generativeai",
            config=dict(
                model=settings.embed_model,
                api_key=settings.gemini_api_key,
                task_type="retrieval_document",
            ),
        ),
    )


def make_default_tools(settings: Settings, *, temperature: float = 0.5):
    """Return the default toolset shared by most agents."""
    try:
        return [
            CodeDocsSearchTool(config=_docs_tool_config(settings, temperature)),
            FileReadTool(),
            FileWriterTool(),
            DirectorySearchTool(),
        ]
    except Exception as exc:  # noqa: BLE001
        raise LLMError(
            "failed to construct default tool set",
            code=Codes.LLM_INIT_FAILED,
            cause=exc,
        ) from exc


@lru_cache(maxsize=1)
def embedder_config(settings: Settings) -> dict:
    return {
        "provider": "google-generativeai",
        "api_key": settings.gemini_api_key,
    }
