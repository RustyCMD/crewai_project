"""Sequential task definitions."""

from __future__ import annotations

from dataclasses import dataclass

from crewai import Task

from ..agents.sequential import SequentialAgents


@dataclass
class SequentialTasks:
    architecture: Task
    features: Task
    testing: Task
    deployment: Task

    def as_list(self) -> list[Task]:
        return [self.architecture, self.features, self.testing, self.deployment]


def build_sequential_tasks(agents: SequentialAgents) -> SequentialTasks:
    architecture = Task(
        description=(
            "Design and implement the core architecture for a Python idle game.\n"
            "Requirements: MVC engine, resource manager, modular upgrade system, "
            "JSON save/load, threaded game loop, modern tkinter GUI scaffolding.\n"
            "Deliverables under Game/: game_engine.py, resource_manager.py, "
            "upgrade_system.py, save_manager.py, gui_framework.py."
        ),
        expected_output=(
            "Five Python files implementing a modular game engine with proper "
            "state management, multi-resource system, dependency-aware upgrades, "
            "robust save/load, and the tkinter scaffolding. All files include "
            "docstrings and structured error handling."
        ),
        agent=agents.senior,
    )

    features = Task(
        description=(
            "Implement game features and UI panels.\n"
            "Requirements: achievement system, animations, multiple UI panels, "
            "automation features, prestige mechanics, polish.\n"
            "Deliverables under Game/: achievement_system.py, animation_manager.py, "
            "ui_components.py, automation_manager.py, prestige_system.py, "
            "main_interface.py."
        ),
        expected_output=(
            "Six Python files providing achievements, animations, UI panels, "
            "automation helpers, prestige logic, and an integrated main interface. "
            "Components must be visually consistent and keyboard-accessible."
        ),
        agent=agents.junior,
    )

    testing = Task(
        description=(
            "Run a full QA pass: automated tests, balance analysis, save/load "
            "regression, UI responsiveness, performance and edge-case testing.\n"
            "Deliverables under Game/: test_suite.py, balance_analysis.py, "
            "performance_report.md, bug_report.md, ux_evaluation.md, "
            "test_results.json."
        ),
        expected_output=(
            "Test suite plus balance and UX reports. All tests pass; balance "
            "recommendations are actionable; bug list has reproduction steps."
        ),
        agent=agents.qa,
    )

    deployment = Task(
        description=(
            "Package and prepare the game for distribution.\n"
            "Requirements: cross-platform PyInstaller builds, requirements.txt, "
            "setup.py, Dockerfile, GitHub Actions CI, user docs.\n"
            "Deliverables under Game/: build_scripts/, installers/, requirements.txt, "
            "setup.py, Dockerfile, .github/workflows/, docs/, README.md."
        ),
        expected_output=(
            "Complete distribution package with build scripts and CI config. "
            "Builds documented and reproducible."
        ),
        agent=agents.devops,
    )

    return SequentialTasks(
        architecture=architecture,
        features=features,
        testing=testing,
        deployment=deployment,
    )
