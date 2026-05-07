"""Agents used by the sequential workflow."""

from __future__ import annotations

from dataclasses import dataclass

from crewai import Agent

from ..config import Settings
from ..errors import Codes, CrewError
from ..llm import make_default_tools, make_llm


@dataclass
class SequentialAgents:
    senior: Agent
    junior: Agent
    qa: Agent
    devops: Agent

    def as_list(self) -> list[Agent]:
        return [self.senior, self.junior, self.qa, self.devops]


def build_sequential_agents(settings: Settings) -> SequentialAgents:
    try:
        senior_llm = make_llm(settings, temperature=0.5)
        junior_llm = make_llm(settings, temperature=0.7)
        qa_llm = make_llm(settings, temperature=0.3)
        devops_llm = make_llm(settings, temperature=0.4)

        senior_tools = make_default_tools(settings, temperature=0.5)
        junior_tools = make_default_tools(settings, temperature=0.7)
        qa_tools = make_default_tools(settings, temperature=0.3)
        devops_tools = make_default_tools(settings, temperature=0.4)

        senior = Agent(
            role="Senior Game Architect",
            goal=(
                "Design and implement complex game systems, architecture, and "
                "advanced features for the idle game."
            ),
            backstory=(
                "Senior game developer with 8+ years of Python game-development "
                "experience. Specializes in scalable architectures, save/load "
                "systems, achievements, and balance design."
            ),
            llm=senior_llm,
            tools=senior_tools,
            allow_delegation=True,
            verbose=True,
            memory=True,
            max_iter=25,
        )

        junior = Agent(
            role="Junior Game Developer",
            goal="Implement game mechanics, UI components, and helper functions.",
            backstory=(
                "Enthusiastic junior developer with solid Python fundamentals "
                "and tkinter/pygame experience. Writes clean, documented code."
            ),
            llm=junior_llm,
            tools=junior_tools,
            allow_delegation=False,
            verbose=True,
            memory=True,
            max_iter=25,
        )

        qa = Agent(
            role="Game QA Engineer",
            goal="Validate quality, balance, and UX through comprehensive testing.",
            backstory=(
                "Specialist in idle/incremental game testing — balance, "
                "progression, save/load, performance, and edge cases."
            ),
            llm=qa_llm,
            tools=qa_tools,
            allow_delegation=False,
            verbose=True,
            memory=True,
            max_iter=15,
        )

        devops = Agent(
            role="Game DevOps Engineer",
            goal="Handle packaging, distribution, and deployment.",
            backstory=(
                "DevOps engineer specializing in Python game packaging — "
                "executable builds, installers, auto-updaters, release pipelines."
            ),
            llm=devops_llm,
            tools=devops_tools,
            allow_delegation=False,
            verbose=True,
            memory=True,
            max_iter=15,
        )

        return SequentialAgents(senior=senior, junior=junior, qa=qa, devops=devops)
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, CrewError):
            raise
        raise CrewError(
            "failed to build sequential agents",
            code=Codes.AGENT_INVALID,
            cause=exc,
        ) from exc
