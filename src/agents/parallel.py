"""Agents used by the parallel/hierarchical collaborative workflow."""

from __future__ import annotations

from dataclasses import dataclass

from crewai import Agent

from ..config import Settings
from ..errors import Codes, CrewError
from ..llm import make_default_tools, make_llm
from ..tools import make_collab_toolset


@dataclass
class ParallelAgents:
    frontend: Agent
    backend: Agent
    integration: Agent
    qa: Agent
    performance: Agent
    file_lock_manager: Agent

    def as_list(self) -> list[Agent]:
        return [
            self.frontend,
            self.backend,
            self.integration,
            self.qa,
            self.performance,
            self.file_lock_manager,
        ]


def build_parallel_agents(settings: Settings) -> ParallelAgents:
    try:
        llm = make_llm(settings, temperature=0.6)
        collab_tools = make_collab_toolset()
        common_tools = collab_tools + make_default_tools(settings, temperature=0.6)

        common = dict(llm=llm, tools=common_tools, verbose=True, memory=True)

        frontend = Agent(
            role="Frontend Developer",
            goal="Build the GUI and visual layer with continuous coordination with backend and integration teams.",
            backstory=(
                "Expert in Python GUI development with tkinter. Communicates "
                "progress proactively and integrates with backend APIs as they evolve."
            ),
            allow_delegation=True,
            max_iter=10,
            **common,
        )

        backend = Agent(
            role="Backend Developer",
            goal="Build the game engine, resource systems, and persistence with shared APIs.",
            backstory=(
                "Backend specialist focused on game engines, resource management, "
                "and stable interfaces for the frontend."
            ),
            allow_delegation=True,
            max_iter=10,
            **common,
        )

        integration = Agent(
            role="Integration Developer",
            goal="Coordinate between teams, manage dependencies, and resolve conflicts.",
            backstory=(
                "Integration specialist who watches all components, identifies "
                "integration points, and brokers between teams."
            ),
            allow_delegation=True,
            max_iter=15,
            **common,
        )

        qa = Agent(
            role="QA Engineer",
            goal="Continuously test components and feed back issues to developers.",
            backstory="QA engineer running parallel tests against new components as they land.",
            allow_delegation=True,
            max_iter=8,
            **common,
        )

        performance = Agent(
            role="Performance Engineer",
            goal="Profile and optimize the game's runtime characteristics.",
            backstory="Performance specialist analyzing CPU, memory, and rendering hot paths.",
            allow_delegation=True,
            max_iter=6,
            **common,
        )

        file_lock_manager = Agent(
            role="File Lock Manager",
            goal="Coordinate file access and prevent conflicts during concurrent development.",
            backstory=(
                "Specialist in coordinating file-level locks across the team. "
                "Maintains audit trails and prevents lost writes."
            ),
            allow_delegation=True,
            max_iter=8,
            **common,
        )

        return ParallelAgents(
            frontend=frontend,
            backend=backend,
            integration=integration,
            qa=qa,
            performance=performance,
            file_lock_manager=file_lock_manager,
        )
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, CrewError):
            raise
        raise CrewError(
            "failed to build parallel agents",
            code=Codes.AGENT_INVALID,
            cause=exc,
        ) from exc
