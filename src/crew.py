"""Crew factory + execution wrapper for both modes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from crewai import Crew, Process

from .agents import build_parallel_agents, build_sequential_agents
from .config import Settings
from .errors import Codes, CrewError
from .llm import embedder_config, make_llm
from .logging_setup import get_logger
from .tasks import build_parallel_tasks, build_sequential_tasks

logger = get_logger(__name__)


@dataclass
class CrewBundle:
    crew: Crew
    description: str

    def kickoff(self, inputs: dict[str, Any] | None = None) -> Any:
        try:
            return self.crew.kickoff(inputs=inputs or {})
        except Exception as exc:  # noqa: BLE001
            raise CrewError(
                "crew kickoff failed",
                code=Codes.CREW_KICKOFF_FAILED,
                cause=exc,
                context={"mode": self.description},
            ) from exc


def build_sequential_crew(settings: Settings) -> CrewBundle:
    try:
        agents = build_sequential_agents(settings)
        tasks = build_sequential_tasks(agents)
        crew = Crew(
            agents=agents.as_list(),
            tasks=tasks.as_list(),
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder=embedder_config(settings),
        )
        return CrewBundle(crew=crew, description="sequential")
    except CrewError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise CrewError(
            "failed to build sequential crew",
            code=Codes.CREW_INIT_FAILED,
            cause=exc,
        ) from exc


def build_parallel_crew(settings: Settings) -> CrewBundle:
    try:
        agents = build_parallel_agents(settings)
        tasks = build_parallel_tasks(agents)
        crew = Crew(
            agents=agents.as_list(),
            tasks=tasks.as_list(),
            process=Process.hierarchical,
            manager_llm=make_llm(settings, temperature=0.4),
            verbose=True,
            memory=True,
            embedder=embedder_config(settings),
            max_rpm=4000,
            share_crew=True,
        )
        return CrewBundle(crew=crew, description="parallel")
    except CrewError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise CrewError(
            "failed to build parallel crew",
            code=Codes.CREW_INIT_FAILED,
            cause=exc,
        ) from exc


def default_inputs(settings: Settings) -> dict[str, Any]:
    return {
        "game_title": settings.game_title,
        "game_version": settings.game_version,
        "target_platforms": ["Windows", "macOS", "Linux"],
        "gui_framework": "tkinter",
        "features": [
            "Resource generation and management",
            "Multi-tier upgrade systems",
            "Achievement system with rewards",
            "Save/load functionality",
            "Automation features",
            "Prestige/rebirth mechanics",
            "Visual animations and effects",
            "Statistics tracking",
            "Settings and customization",
        ],
        "technical_requirements": [
            "Object-oriented architecture",
            "Modular design patterns",
            "Structured error handling and logging",
            "Performance optimization",
            "Cross-platform compatibility",
            "Automated testing suite",
        ],
    }
