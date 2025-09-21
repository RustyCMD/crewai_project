#!/usr/bin/env python3
"""
Collaborative Development Launcher
Launch collaborative development with optional real-time dashboard
"""

import os
import sys
import subprocess
import threading
import time
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🚀 COLLABORATIVE CREWAI DEVELOPMENT LAUNCHER 🚀        ║
    ║                                                              ║
    ║     Multi-Agent Parallel Development with Real-time Dashboard  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🎯 LAUNCH OPTIONS:
    
    1. 🤖 Development Only    - Run collaborative agents without dashboard
    2. 📊 Dashboard Only      - Monitor existing development session  
    3. 🚀 Full Launch         - Run both development and dashboard
    
    👥 AGENT TEAM:
    ├── 🎨 Frontend Developer    - UI/GUI Components
    ├── ⚙️  Backend Developer     - Core Logic & Systems
    ├── 🔗 Integration Developer - Coordination & Dependencies
    ├── 🧪 QA Engineer           - Testing & Quality
    └── ⚡ Performance Engineer  - Optimization & Monitoring
    """
    print(banner)

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    
    # Check environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment")
        print("   Please set your Gemini API key in .env file")
        return False
    print("✅ Gemini API key configured")
    
    # Check required files
    required_files = [
        "collaborative_agents.py",
        "agent_communication.py", 
        "collaborative_tools.py",
        "run_collaborative_development.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file missing: {file}")
            return False
    print("✅ All required files present")
    
    return True

def launch_development():
    """Launch collaborative development"""
    print("🚀 Launching collaborative development...")
    
    try:
        # Run the collaborative development
        result = subprocess.run([
            sys.executable, 
            "run_collaborative_development.py"
        ], capture_output=False, text=True)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error launching development: {e}")
        return False

def launch_dashboard():
    """Launch real-time dashboard"""
    print("📊 Launching real-time dashboard...")
    
    try:
        # Run the dashboard in a separate process
        subprocess.Popen([
            sys.executable,
            "collaboration_dashboard.py"
        ])
        
        print("✅ Dashboard launched successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False

def launch_both():
    """Launch both development and dashboard"""
    print("🚀 Launching full collaborative environment...")
    
    # Launch dashboard first
    if not launch_dashboard():
        return False
    
    # Wait a moment for dashboard to initialize
    time.sleep(2)
    
    # Launch development
    return launch_development()

def interactive_menu():
    """Show interactive menu for launch options"""
    while True:
        print("\n" + "="*60)
        print("🎯 COLLABORATIVE DEVELOPMENT LAUNCHER")
        print("="*60)
        print("1. 🤖 Development Only    - Run agents without dashboard")
        print("2. 📊 Dashboard Only      - Monitor existing session")
        print("3. 🚀 Full Launch         - Run both development and dashboard")
        print("4. ❌ Exit")
        print("="*60)
        
        try:
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                print("\n🤖 Starting development only...")
                return launch_development()
                
            elif choice == "2":
                print("\n📊 Starting dashboard only...")
                return launch_dashboard()
                
            elif choice == "3":
                print("\n🚀 Starting full collaborative environment...")
                return launch_both()
                
            elif choice == "4":
                print("\n👋 Goodbye!")
                return True
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return True

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Launch Collaborative CrewAI Development")
    parser.add_argument("--mode", choices=["dev", "dashboard", "full"], 
                       help="Launch mode: dev (development only), dashboard (dashboard only), full (both)")
    parser.add_argument("--no-banner", action="store_true", help="Skip banner display")
    
    args = parser.parse_args()
    
    if not args.no_banner:
        print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All requirements satisfied!")
    
    # Launch based on mode
    if args.mode == "dev":
        print("\n🤖 Launching development only...")
        success = launch_development()
        
    elif args.mode == "dashboard":
        print("\n📊 Launching dashboard only...")
        success = launch_dashboard()
        
    elif args.mode == "full":
        print("\n🚀 Launching full collaborative environment...")
        success = launch_both()
        
    else:
        # Interactive mode
        success = interactive_menu()
    
    if success:
        print("\n🎉 Launch completed successfully!")
        if args.mode in ["dev", "full"] or (not args.mode):
            print("📁 Check the Game/ directory for generated files")
            print("📋 Check collaborative_development.log for detailed logs")
            print("💬 Check Game/shared/agent_communication.json for team communications")
    else:
        print("\n❌ Launch encountered issues. Check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
