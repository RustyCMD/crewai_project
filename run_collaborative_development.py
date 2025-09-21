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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('collaborative_development.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

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
    logger.info("🔍 Starting collaboration monitoring...")
    
    start_time = time.time()
    last_status_check = 0
    
    while True:
        try:
            current_time = time.time()
            
            # Check status every 30 seconds
            if current_time - last_status_check > 30:
                logger.info("📊 === COLLABORATION STATUS UPDATE ===")
                
                # Get team status
                status_updates = comm_hub.get_agent_status()
                if status_updates:
                    logger.info("👥 Team Status:")
                    agent_status = {}
                    for update in status_updates[-10:]:
                        agent = update["agent"]
                        agent_status[agent] = update["status"]
                    
                    for agent, status in agent_status.items():
                        logger.info(f"   {agent}: {status}")
                
                # Check recent communications
                # FIX: Use comm_hub.lock to prevent race conditions when reading JSON file
                with comm_hub.lock:
                    data = comm_hub._read_data()
                    recent_comms = data["communications"][-5:]
                    
                    if recent_comms:
                        logger.info("💬 Recent Communications:")
                        for comm in recent_comms:
                            logger.info(f"   {comm['from_agent']} → {comm['to_agent']}: {comm['message'][:50]}...")
                
                # Check file locks
                file_locks = data.get("file_locks", {})
                if file_locks:
                    logger.info("🔒 Active File Locks:")
                    for file_path, lock_info in file_locks.items():
                        logger.info(f"   {file_path} (locked by {lock_info['agent']})")
                
                logger.info("=" * 50)
                last_status_check = current_time
            
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
            time.sleep(10)

def main():
    """Main function to run collaborative development"""
    
    print_banner()
    
    logger.info("🚀 Initializing Advanced Collaborative CrewAI Development")
    logger.info("=" * 60)
    
    # Verify environment
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        logger.error("Please set your Gemini API key in the .env file")
        sys.exit(1)
    
    logger.info("✅ Environment verified")
    logger.info("✅ Gemini API key configured")
    
    # Initialize communication system
    logger.info("🔧 Initializing communication system...")
    comm_hub.initialize_communication_file()
    logger.info("✅ Communication system ready")
    
    # Log start of collaborative development
    comm_hub.update_shared_context("development_start_time", datetime.now().isoformat())
    comm_hub.update_shared_context("project_name", "Advanced Idle Game")
    comm_hub.update_shared_context("development_mode", "collaborative_parallel")
    
    logger.info("🎯 Starting collaborative development process...")
    logger.info("📝 Agents will work simultaneously with real-time coordination")
    logger.info("💬 Inter-agent communication enabled")
    logger.info("🔄 Shared memory and context active")
    logger.info("🔒 File locking and conflict resolution enabled")
    
    try:
        # Start the collaborative development
        result = run_collaborative_development()
        
        if result:
            logger.info("🎉 === COLLABORATIVE DEVELOPMENT COMPLETED! ===")
            logger.info("✅ All agents have completed their collaborative tasks")
            logger.info("🎮 Advanced idle game development finished")
            
            # Final status report
            logger.info("📊 Final Team Status:")
            final_status = comm_hub.get_agent_status()
            agent_final = {}
            for update in final_status[-10:]:
                agent = update["agent"]
                agent_final[agent] = update["status"]
            
            for agent, status in agent_final.items():
                logger.info(f"   ✅ {agent}: {status}")
            
            logger.info("🎯 Check the Game/ directory for the completed project!")
            
        else:
            logger.error("❌ Collaborative development encountered issues")
            logger.error("Check the logs for details")
            
    except KeyboardInterrupt:
        logger.info("🛑 Development stopped by user")
        logger.info("💾 Saving current progress...")
        
        # Update shared context with interruption
        comm_hub.update_shared_context("development_interrupted", datetime.now().isoformat())
        
    except Exception as e:
        logger.error(f"❌ Critical error in collaborative development: {e}")
        logger.error("Check the logs and communication files for details")
        
        # Report error to communication system
        comm_hub.update_shared_context("development_error", str(e))
        
    finally:
        logger.info("🔄 Collaborative development session ended")
        logger.info("📁 Check Game/ directory for generated files")
        logger.info("📋 Check collaborative_development.log for detailed logs")
        logger.info("💬 Check Game/shared/agent_communication.json for team communications")

if __name__ == "__main__":
    main()
