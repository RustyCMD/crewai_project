@echo off
REM ============================================================================
REM True Parallel CrewAI Development Launcher
REM Starts agents in parallel threads, then launches the dashboard
REM ============================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🤖 TRUE PARALLEL CREWAI DEVELOPMENT LAUNCHER 🤖        ║
echo ║                                                              ║
echo ║     Automated startup for parallel agent development         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Check if required files exist
if not exist "run_collaborative_development.py" (
    echo ❌ ERROR: run_collaborative_development.py not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

if not exist "collaboration_dashboard.py" (
    echo ❌ ERROR: collaboration_dashboard.py not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

echo ✅ Required files found
echo.

REM Check for .env file
if not exist ".env" (
    echo ⚠️  WARNING: .env file not found
    echo Please ensure your GEMINI_API_KEY is configured
    echo.
)

echo 🚀 Starting True Parallel CrewAI Development...
echo.
echo 📋 Process:
echo    1. Launch parallel agents in background
echo    2. Wait for agents to initialize
echo    3. Start collaboration dashboard
echo.

REM Start the parallel development in background
echo 🧵 Starting parallel agents...
start "Parallel Agents" /MIN python run_collaborative_development.py

REM Wait for agents to initialize (give them time to start up)
echo ⏳ Waiting for agents to initialize...
timeout /t 10 /nobreak >nul

REM Check if agents are starting up by looking for the communication file
set "wait_count=0"
:wait_loop
if exist "Game\shared\agent_communication.json" (
    echo ✅ Agents initialized successfully
    goto start_dashboard
)

set /a wait_count+=1
if %wait_count% geq 30 (
    echo ⚠️  Agents taking longer than expected to initialize
    echo Continuing with dashboard startup...
    goto start_dashboard
)

echo    Waiting for agents... (%wait_count%/30)
timeout /t 2 /nobreak >nul
goto wait_loop

:start_dashboard
echo.
echo 📊 Starting Collaboration Dashboard...
echo.
echo 💡 TIP: You should now see all agents active simultaneously in the dashboard!
echo 💡 Check the "Agent Status" panel to verify parallel execution
echo.

REM Start the dashboard (this will be the foreground process)
python collaboration_dashboard.py

echo.
echo 🏁 Development session ended
echo.
echo 📁 Check the Game/ directory for generated files
echo 📋 Check collaborative_development.log for detailed logs
echo 💬 Check Game/shared/agent_communication.json for team communications
echo.
pause
