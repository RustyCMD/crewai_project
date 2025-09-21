#!/usr/bin/env python3
"""
True Parallel CrewAI Development Launcher (Cross-platform)
Starts agents in parallel threads, then launches the dashboard
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 TRUE PARALLEL CREWAI DEVELOPMENT LAUNCHER 🤖        ║
║                                                              ║
║     Automated startup for parallel agent development         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_requirements():
    """Check if all required files exist"""
    
    required_files = [
        "run_collaborative_development.py",
        "collaboration_dashboard.py"
    ]
    
    print("🔍 Checking requirements...")
    
    # Check Python version
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check required files
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ {file} found")
    
    if missing_files:
        print(f"❌ ERROR: Missing required files: {', '.join(missing_files)}")
        print("Please ensure you're running this from the correct directory")
        return False
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  WARNING: .env file not found")
        print("Please ensure your GEMINI_API_KEY is configured")
    else:
        print("✅ .env file found")
    
    print()
    return True

def wait_for_agents():
    """Wait for agents to initialize"""
    
    print("⏳ Waiting for agents to initialize...")
    
    communication_file = Path("Game/shared/agent_communication.json")
    wait_count = 0
    max_wait = 30
    
    while wait_count < max_wait:
        if communication_file.exists():
            print("✅ Agents initialized successfully")
            return True
        
        wait_count += 1
        print(f"   Waiting for agents... ({wait_count}/{max_wait})")
        time.sleep(2)
    
    print("⚠️  Agents taking longer than expected to initialize")
    print("Continuing with dashboard startup...")
    return False

def main():
    """Main launcher function"""
    
    print_banner()
    
    # Check requirements
    if not check_requirements():
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("🚀 Starting True Parallel CrewAI Development...")
    print()
    print("📋 Process:")
    print("   1. Launch parallel agents in background")
    print("   2. Wait for agents to initialize")
    print("   3. Start collaboration dashboard")
    print()
    
    try:
        # Start the parallel development in background
        print("🧵 Starting parallel agents...")
        
        # Use subprocess.Popen to start in background
        if sys.platform == "win32":
            # Windows
            agent_process = subprocess.Popen(
                [sys.executable, "run_collaborative_development.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Unix/Linux/macOS
            agent_process = subprocess.Popen(
                [sys.executable, "run_collaborative_development.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        print(f"✅ Agents started in background (PID: {agent_process.pid})")
        
        # Wait for agents to initialize
        wait_for_agents()
        
        print()
        print("📊 Starting Collaboration Dashboard...")
        print()
        print("💡 TIP: You should now see all agents active simultaneously in the dashboard!")
        print("💡 Check the 'Agent Status' panel to verify parallel execution")
        print()
        
        # Start the dashboard (this will be the foreground process)
        dashboard_process = subprocess.run([sys.executable, "collaboration_dashboard.py"])
        
        print()
        print("🏁 Development session ended")
        
        # Try to terminate the agent process gracefully
        try:
            agent_process.terminate()
            agent_process.wait(timeout=5)
            print("✅ Agent processes terminated gracefully")
        except subprocess.TimeoutExpired:
            agent_process.kill()
            print("⚠️  Agent processes force-killed")
        except:
            print("⚠️  Could not terminate agent processes")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        
        # Try to terminate the agent process
        try:
            agent_process.terminate()
            agent_process.wait(timeout=5)
        except:
            try:
                agent_process.kill()
            except:
                pass
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    finally:
        print()
        print("📁 Check the Game/ directory for generated files")
        print("📋 Check collaborative_development.log for detailed logs")
        print("💬 Check Game/shared/agent_communication.json for team communications")
        print()
        
        if sys.platform == "win32":
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
