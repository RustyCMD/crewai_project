#!/usr/bin/env bash
# CrewAI Idle Game Development Workbench - unified launcher (Unix)
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "[E1004] python3 is not on PATH." >&2
    exit 1
fi

if [[ ! -f .env ]]; then
    echo "[E1001] .env file not found. Create one with GEMINI_API_KEY=your_key" >&2
    exit 1
fi

PYTHON="${PYTHON:-python3}"

print_menu() {
    cat <<'MENU'
================================================================
  CrewAI Idle Game Development Workbench
  v2.0  |  unified launcher
================================================================

  1) Sequential development (4 agents, simple, fastest)
  2) Parallel collaborative (6 agents, hierarchical)
  3) Dashboard only (monitor an existing run)
  4) Full launch (parallel agents + live dashboard)
  5) Exit

MENU
}

print_menu
read -rp "Enter choice [1-5]: " choice

case "${choice}" in
    1) "${PYTHON}" -m src.cli --mode sequential --no-menu ;;
    2) "${PYTHON}" -m src.cli --mode parallel   --no-menu ;;
    3) "${PYTHON}" -m src.cli --mode dashboard  --no-menu ;;
    4) "${PYTHON}" -m src.cli --mode full       --no-menu ;;
    5) exit 0 ;;
    *) echo "Invalid choice: ${choice}" >&2; exit 1 ;;
esac
