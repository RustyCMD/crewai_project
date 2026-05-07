"""Parallel/collaborative task definitions."""

from __future__ import annotations

from dataclasses import dataclass

from crewai import Task

from ..agents.parallel import ParallelAgents


@dataclass
class ParallelTasks:
    frontend: Task
    backend: Task
    integration: Task
    qa: Task
    performance: Task
    file_lock: Task

    def as_list(self) -> list[Task]:
        # NOTE: CrewAI requires the LAST task to be synchronous.
        return [
            self.frontend,
            self.backend,
            self.integration,
            self.qa,
            self.performance,
            self.file_lock,  # async_execution=False
        ]


def build_parallel_tasks(agents: ParallelAgents) -> ParallelTasks:
    frontend = Task(
        description=(
            "Build the complete GUI under Game/frontend/. Coordinate APIs with "
            "the Backend Developer, share progress through the team_communication "
            "tool, and request reviews from QA.\n"
            "Files: main_window.py, resource_display.py, upgrade_panel.py, "
            "game_controls.py, theme_manager.py, animation_system.py."
        ),
        expected_output=(
            "Frontend module with all listed files, integration logs in the "
            "communication hub, and review requests recorded."
        ),
        agent=agents.frontend,
        async_execution=True,
    )

    backend = Task(
        description=(
            "Build the engine under Game/backend/. Publish API specs to the "
            "Frontend Developer and coordinate with Integration on architecture.\n"
            "Files: game_engine.py, resource_system.py, upgrade_engine.py, "
            "save_system.py, event_system.py, achievement_engine.py."
        ),
        expected_output=(
            "Backend module with stable APIs, integration points registered "
            "via integration_coordinator, and testing hooks for QA."
        ),
        agent=agents.backend,
        async_execution=True,
    )

    integration = Task(
        description=(
            "Coordinate the team under Game/integration/. Track dependencies, "
            "monitor progress, and resolve conflicts.\n"
            "Files: coordinator.py, dependency_manager.py, communication_hub.py, "
            "conflict_resolver.py, project_status.py."
        ),
        expected_output="Integration module with dependency graph and conflict log.",
        agent=agents.integration,
        async_execution=True,
    )

    qa = Task(
        description=(
            "Run continuous QA under Game/qa/. Test components as they land, "
            "publish bugs through team_communication.\n"
            "Files: test_suite.py, continuous_testing.py, quality_metrics.py, "
            "bug_tracker.py."
        ),
        expected_output="QA module with bug tracker entries linked to commits.",
        agent=agents.qa,
        async_execution=True,
    )

    performance = Task(
        description=(
            "Profile and optimize under Game/performance/.\n"
            "Files: profiler.py, optimizer.py, metrics.py."
        ),
        expected_output="Performance module with benchmark results and recommendations.",
        agent=agents.performance,
        async_execution=True,
    )

    file_lock = Task(
        description=(
            "Operate the file-lock manager under Game/file_management/. Monitor "
            "and arbitrate write access for every other agent.\n"
            "Files: lock_manager.py, conflict_resolver.py, access_coordinator.py, "
            "audit_logger.py."
        ),
        expected_output="File-lock manager module with audit trail and access policies.",
        agent=agents.file_lock_manager,
        # MUST be sync — CrewAI requires the final task to be synchronous.
        async_execution=False,
    )

    return ParallelTasks(
        frontend=frontend,
        backend=backend,
        integration=integration,
        qa=qa,
        performance=performance,
        file_lock=file_lock,
    )
