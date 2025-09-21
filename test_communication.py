#!/usr/bin/env python3
"""
Test the communication system
"""

from agent_communication import comm_hub

# Test sending messages
print("🧪 Testing communication system...")

# Send test messages
comm_hub.send_message("Frontend Developer", "Backend Developer", "Hello from Frontend! Starting work on main_window.py", "info")
comm_hub.send_message("Backend Developer", "Frontend Developer", "Hi Frontend! I'm working on game_engine.py", "info")
comm_hub.send_message("Integration Agent", "all", "Coordinating between frontend and backend teams", "coordination")

# Update status
comm_hub.update_status("Frontend Developer", "Working on main window layout", {"file": "main_window.py", "progress": "25%"})
comm_hub.update_status("Backend Developer", "Implementing game engine", {"file": "game_engine.py", "progress": "40%"})

# Test file locking
print("🔒 Testing file locking...")
lock_result = comm_hub.request_file_lock("Frontend Developer", "Game/frontend/main_window.py")
print(f"File lock result: {lock_result}")

# Report integration point
comm_hub.report_integration_point("Frontend Developer", "MainWindow", {
    "interface": "GameWindow",
    "methods": ["start_game", "stop_game", "update_display"],
    "dependencies": ["GameEngine", "ResourceManager"]
})

print("✅ Communication test completed!")
print("📁 Check Game/shared/agent_communication.json for results")
print("📊 Check the dashboard for live updates")
