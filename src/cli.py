"""
Single CLI entrypoint with an interactive menu.

Usage:
    python -m src.cli                    # interactive menu
    python -m src.cli --mode sequential  # run sequential crew
    python -m src.cli --mode parallel    # run parallel/hierarchical crew
    python -m src.cli --mode dashboard   # launch dashboard only
    python -m src.cli --mode full        # launch dashboard + agents (parallel)
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from typing import Callable

from .comms import default_hub
from .config import Settings
from .crew import build_parallel_crew, build_sequential_crew, default_inputs
from .errors import Codes, ConfigError, CrewAIError
from .logging_setup import get_logger, setup_logging

MODES = {
    "1": ("sequential", "Sequential development (4 agents, simple, fastest)"),
    "2": ("parallel", "Parallel collaborative (6 agents, hierarchical)"),
    "3": ("dashboard", "Dashboard only (monitor an existing run)"),
    "4": ("full", "Full launch (parallel agents + live dashboard)"),
    "5": ("exit", "Exit"),
}


def _print_banner() -> None:
    print("=" * 64)
    print(" CrewAI Idle Game Development Workbench")
    print(" v2.0  |  unified launcher")
    print("=" * 64)


def _print_menu() -> None:
    print()
    print("Select a mode:")
    for key, (_, label) in MODES.items():
        print(f"  {key}) {label}")
    print()


def _prompt_mode() -> str:
    while True:
        choice = input("Enter choice [1-5]: ").strip()
        if choice in MODES:
            return MODES[choice][0]
        print(f"Invalid choice {choice!r}.")


def _run_sequential(settings: Settings) -> int:
    logger = get_logger(__name__)
    logger.info("starting sequential crew")
    bundle = build_sequential_crew(settings)
    result = bundle.kickoff(default_inputs(settings))
    logger.info("sequential crew finished")
    print("\n=== RESULT ===\n")
    print(result)
    return 0


def _run_parallel(settings: Settings) -> int:
    logger = get_logger(__name__)
    logger.info("starting parallel crew")
    bundle = build_parallel_crew(settings)
    result = bundle.kickoff(default_inputs(settings))
    logger.info("parallel crew finished")
    print("\n=== RESULT ===\n")
    print(result)
    return 0


def _run_dashboard(_: Settings) -> int:
    from .dashboard import run_dashboard

    run_dashboard(mode="parallel")
    return 0


def _run_full(settings: Settings) -> int:
    """Launch the dashboard. The dashboard's Start Agents button spawns the
    crew subprocess via AgentRunner, so there's nothing to do here besides
    pre-warm the comms hub and hand off to the GUI."""
    default_hub()  # ensure state file exists before dashboard polls
    return _run_dashboard(settings)


DISPATCH: dict[str, Callable[[Settings], int]] = {
    "sequential": _run_sequential,
    "parallel": _run_parallel,
    "dashboard": _run_dashboard,
    "full": _run_full,
}


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="crewai-cli", description="CrewAI development workbench")
    parser.add_argument("--mode", choices=sorted(DISPATCH.keys()) + ["menu"], default="menu")
    parser.add_argument("--no-menu", action="store_true", help="Skip interactive menu (requires --mode).")
    parser.add_argument("--log-level", default=None)
    parser.add_argument("--log-file", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    try:
        settings = Settings.load()
    except ConfigError as exc:
        sys.stderr.write(f"{exc}\n")
        sys.stderr.write(
            "Set GEMINI_API_KEY in your .env file. See .env.example for details.\n"
        )
        return int(exc.code.code[1:]) % 100 + 10  # non-zero exit codes
    setup_logging(
        level=args.log_level or settings.log_level,
        log_file=args.log_file or settings.log_file,
    )
    logger = get_logger(__name__)

    if args.mode == "menu" and not args.no_menu:
        _print_banner()
        _print_menu()
        try:
            mode = _prompt_mode()
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            return 0
    else:
        mode = args.mode if args.mode != "menu" else "sequential"

    if mode == "exit":
        return 0

    handler = DISPATCH.get(mode)
    if handler is None:
        sys.stderr.write(f"[{Codes.CONFIG_INVALID_VALUE.code}] unknown mode: {mode}\n")
        return 2

    started = datetime.now()
    logger.info("mode=%s started=%s", mode, started.isoformat())
    try:
        return handler(settings)
    except CrewAIError as exc:
        logger.error("aborted: %s", exc)
        sys.stderr.write(f"{exc}\n")
        return 3
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        return 130
    finally:
        elapsed = datetime.now() - started
        logger.info("mode=%s elapsed=%s", mode, elapsed)


if __name__ == "__main__":
    raise SystemExit(main())
