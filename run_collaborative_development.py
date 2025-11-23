#!/usr/bin/env python3
"""
Advanced Collaborative CrewAI Development Runner
Launches multiple AI agents working simultaneously on the idle game project
"""

import os
import sys
import time
import logging
from datetime import datetime
from collaborative_agents import run_collaborative_development
from agent_communication import comm_hub
from logging_config import setup_logging, get_logger, log_safe

# Configure logging
setup_logging()

# Create additional file handler for collaborative development
collab_log_file = 'collaborative_development.log'
collab_handler = logging.FileHandler(collab_log_file, encoding='utf-8')
collab_handler.setLevel(logging.INFO)
collab_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
collab_handler.setFormatter(collab_formatter)

# Add handler to root logger
root_logger = logging.getLogger()
root_logger.addHandler(collab_handler)

logger = get_logger(__name__)

def print_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🤖 ADVANCED COLLABORATIVE CREWAI DEVELOPMENT 🤖        ║
    ║                                                              ║
    ║  Multi-Agent Parallel Development with Real-time Collaboration ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🎯 MISSION: Create an advanced idle game through collaborative AI development
    
    👥 DEVELOPMENT TEAM:
    ├── 🎨 Frontend Developer Agent    - UI/GUI Components & Visual Design
    ├── ⚙️  Backend Developer Agent     - Core Logic & Systems Architecture
    ├── 🔗 Integration Developer Agent - Coordination & Dependency Management
    ├── 🧪 QA Engineer Agent           - Testing & Code Quality
    ├── ⚡ Performance Engineer Agent  - Optimization & Performance Monitoring
    └── 🔒 File Lock Manager Agent     - File Access Coordination & Conflict Prevention
    
    🚀 FEATURES:
    ├── ⚡ Parallel Execution (Process.hierarchical)
    ├── 💬 Real-time Inter-agent Communication
    ├── 🔄 Synchronized Development with Shared Memory
    ├── 🔒 File Locking & Conflict Resolution
    ├── 📊 Live Progress Monitoring
    └── 🎯 Collaborative Task Coordination
    """
    print(banner)

def monitor_collaboration():
    """Monitor and display collaboration progress"""
    log_safe(logger, "info", "[SEARCH] Starting collaboration monitoring...")

    start_time = time.time()
    last_status_check = 0

    while True:
        try:
            current_time = time.time()

            # Check status every 30 seconds
            if current_time - last_status_check > 30:
                log_safe(logger, "info", "[CHART] === COLLABORATION STATUS UPDATE ===")

                # Get team status
                status_updates = comm_hub.get_agent_status()
                if status_updates:
                    log_safe(logger, "info", "[TEAM] Team Status:")
                    agent_status = {}
                    for update in status_updates[-10:]:
                        agent = update["agent"]
                        agent_status[agent] = update["status"]

                    for agent, status in agent_status.items():
                        log_safe(logger, "info", f"   {agent}: {status}")
                
                # Check recent communications
                data = comm_hub._read_data()
                recent_comms = data["communications"][-5:]
                
                if recent_comms:
                    log_safe(logger, "info", "[CHAT] Recent Communications:")
                    for comm in recent_comms:
                        log_safe(logger, "info", f"   {comm['from_agent']} -> {comm['to_agent']}: {comm['message'][:50]}...")

                # Check file locks
                file_locks = data.get("file_locks", {})
                if file_locks:
                    log_safe(logger, "info", "[LOCK] Active File Locks:")
                    for file_path, lock_info in file_locks.items():
                        log_safe(logger, "info", f"   {file_path} (locked by {lock_info['agent']})")

                log_safe(logger, "info", "=" * 50)
                last_status_check = current_time
            
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            log_safe(logger, "info", "[STOP] Monitoring stopped by user")
            break
        except Exception as e:
            log_safe(logger, "error", f"[ERROR] Monitoring error: {e}")
            time.sleep(10)

def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == 'your_gemini_api_key_here':
            missing_vars.append(var)

    if missing_vars:
        log_safe(logger, "error", "[ERROR] Missing required environment variables:")
        for var in missing_vars:
            log_safe(logger, "error", f"   - {var}")
        log_safe(logger, "error", "Please update your .env file with the required API keys.")
        log_safe(logger, "error", "See .env file for instructions on obtaining API keys.")
        return False

    return True

def main():
    """Main function to run collaborative development"""
    
    print_banner()
    
    log_safe(logger, "info", "[ROCKET] Initializing Advanced Collaborative CrewAI Development")
    log_safe(logger, "info", "=" * 60)

    # Verify environment with robust validation
    if not validate_environment():
        sys.exit(1)

    log_safe(logger, "info", "[OK] Environment verified")
    log_safe(logger, "info", "[OK] Gemini API key configured")

    # Initialize communication system
    log_safe(logger, "info", "[TOOLS] Initializing communication system...")
    comm_hub.initialize_communication_file()
    log_safe(logger, "info", "[OK] Communication system ready")
    
    # Log start of collaborative development
    comm_hub.update_shared_context("development_start_time", datetime.now().isoformat())
    comm_hub.update_shared_context("project_name", "Advanced Idle Game")
    comm_hub.update_shared_context("development_mode", "collaborative_parallel")
    
    log_safe(logger, "info", "[TARGET] Starting collaborative development process...")
    log_safe(logger, "info", "[NOTE] Agents will work simultaneously with real-time coordination")
    log_safe(logger, "info", "[CHAT] Inter-agent communication enabled")
    log_safe(logger, "info", "[REFRESH] Shared memory and context active")
    log_safe(logger, "info", "[LOCK] File locking and conflict resolution enabled")
    
    # Start monitoring in a separate daemon thread
    import threading
    monitor_thread = threading.Thread(target=monitor_collaboration, daemon=True)
    monitor_thread.start()
    log_safe(logger, "info", "[SEARCH] Live progress monitoring started")
    
    try:
        # Start the collaborative development
        result = run_collaborative_development()
        
        if result:
            log_safe(logger, "info", "[PARTY] === COLLABORATIVE DEVELOPMENT COMPLETED! ===")
            log_safe(logger, "info", "[OK] All agents have completed their collaborative tasks")
            log_safe(logger, "info", "[GAME] Advanced idle game development finished")

            # Final status report
            log_safe(logger, "info", "[CHART] Final Team Status:")
            final_status = comm_hub.get_agent_status()
            agent_final = {}
            for update in final_status[-10:]:
                agent = update["agent"]
                agent_final[agent] = update["status"]

            for agent, status in agent_final.items():
                log_safe(logger, "info", f"   [OK] {agent}: {status}")

            log_safe(logger, "info", "[TARGET] Check the Game/ directory for the completed project!")

        else:
            log_safe(logger, "error", "[ERROR] Collaborative development encountered issues")
            log_safe(logger, "error", "Check the logs for details")
            
    except KeyboardInterrupt:
        log_safe(logger, "info", "[STOP] Development stopped by user")
        log_safe(logger, "info", "[SAVE] Saving current progress...")

        # Update shared context with interruption
        comm_hub.update_shared_context("development_interrupted", datetime.now().isoformat())

    except Exception as e:
        log_safe(logger, "error", f"[ERROR] Critical error in collaborative development: {e}")
        log_safe(logger, "error", "Check the logs and communication files for details")

        # Report error to communication system
        comm_hub.update_shared_context("development_error", str(e))

    finally:
        log_safe(logger, "info", "[REFRESH] Collaborative development session ended")
        log_safe(logger, "info", "[FILE] Check Game/ directory for generated files")
        log_safe(logger, "info", "[LIST] Check collaborative_development.log for detailed logs")
        log_safe(logger, "info", "[CHAT] Check Game/shared/agent_communication.json for team communications")

if __name__ == "__main__":
    main()
