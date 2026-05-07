@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM  CrewAI Idle Game Development Workbench
REM  Unified launcher (Windows)
REM ============================================================

cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo [E1004] Python is not on PATH. Install Python 3.10+ from https://www.python.org/.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [E1001] .env file not found.
    echo         Create one with GEMINI_API_KEY=your_key
    pause
    exit /b 1
)

:menu
cls
echo ================================================================
echo   CrewAI Idle Game Development Workbench
echo   v2.0  ^|  unified launcher
echo ================================================================
echo.
echo   1^) Sequential development (4 agents, simple, fastest)
echo   2^) Parallel collaborative (6 agents, hierarchical)
echo   3^) Dashboard only (monitor an existing run)
echo   4^) Full launch (parallel agents + live dashboard)
echo   5^) Exit
echo.
set "choice="
set /p "choice=Enter choice [1-5]: "

if "%choice%"=="1" (
    python -m src.cli --mode sequential --no-menu
    goto end
)
if "%choice%"=="2" (
    python -m src.cli --mode parallel --no-menu
    goto end
)
if "%choice%"=="3" (
    python -m src.cli --mode dashboard --no-menu
    goto end
)
if "%choice%"=="4" (
    python -m src.cli --mode full --no-menu
    goto end
)
if "%choice%"=="5" (
    goto :eof
)

echo Invalid choice: %choice%
timeout /t 2 >nul
goto menu

:end
echo.
echo Session ended. Logs in logs\crewai.log; team state in Game\shared\agent_communication.json
pause
