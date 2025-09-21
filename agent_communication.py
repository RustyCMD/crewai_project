"""
Real-time Agent Communication System
Enables inter-agent messaging, status updates, and collaborative coordination
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any
import threading
import logging
import uuid

logger = logging.getLogger(__name__)

class AgentCommunicationHub:
    """Central hub for agent-to-agent communication and coordination"""
    
    def __init__(self, communication_file="Game/shared/agent_communication.json"):
        self.communication_file = communication_file
        # Use RLock to prevent deadlocks when locked methods call other locked methods
        self.lock = threading.RLock()
        self.initialize_communication_file()
    
    def initialize_communication_file(self):
        """Initialize the communication file if it doesn't exist or ensure it has all required keys"""
        with self.lock:
            os.makedirs(os.path.dirname(self.communication_file), exist_ok=True)

            # Required structure
            required_keys = {
                "communications": [],
                "status_updates": [],
                "shared_context": {},
                "file_locks": {},
                "file_lock_requests": [],
                "integration_points": [],
                "conflict_reports": []
            }

            # If file doesn't exist, create it with initial structure
            if not os.path.exists(self.communication_file):
                with open(self.communication_file, 'w') as f:
                    json.dump(required_keys, f, indent=2)
                return

            # If file exists, ensure it has all required keys
            try:
                with open(self.communication_file, 'r+') as f:
                    existing_data = json.load(f)

                    # Check if any keys are missing and add them
                    updated = False
                    for key, default_value in required_keys.items():
                        if key not in existing_data:
                            existing_data[key] = default_value
                            updated = True
                            logger.info(f"Added missing key '{key}' to communication file")

                    # Only write back if we added missing keys
                    if updated:
                        f.seek(0)
                        json.dump(existing_data, f, indent=2)
                        f.truncate()

            except Exception as e:
                logger.error(f"Error reading communication file, recreating: {e}")
                # If file is corrupted, recreate it
                with open(self.communication_file, 'w') as f:
                    json.dump(required_keys, f, indent=2)

    def _read_data(self):
        """Safely reads data from the JSON file. Must be called within a lock."""
        with open(self.communication_file, 'r') as f:
            return json.load(f)

    def _write_data(self, data):
        """Safely writes data to the JSON file. Must be called within a lock."""
        with open(self.communication_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def send_message(self, from_agent: str, to_agent: str, message: str, message_type: str = "info"):
        """Send a message from one agent to another"""
        with self.lock:
            try:
                data = self._read_data()

                communication = {
                    "id": str(uuid.uuid4()),  # Use UUID for robust unique IDs
                    "timestamp": datetime.now().isoformat(),
                    "from_agent": from_agent,
                    "to_agent": to_agent,
                    "message": message,
                    "type": message_type,
                    "read": False
                }

                data["communications"].append(communication)
                self._write_data(data)

                logger.info(f"📨 {from_agent} → {to_agent}: {message[:50]}...")

            except Exception as e:
                logger.error(f"Error sending message: {e}")
    
    def get_messages(self, agent_name: str, unread_only: bool = True) -> List[Dict]:
        """Get messages for a specific agent"""
        with self.lock:  # FIX: Added lock to prevent race conditions
            try:
                data = self._read_data()

                messages = [
                    msg for msg in data["communications"]
                    if msg["to_agent"] == agent_name and (not unread_only or not msg.get("read", False))
                ]

                return messages

            except Exception as e:
                logger.error(f"Error getting messages: {e}")
                return []
    
    def mark_message_read(self, message_id: str):
        """Mark a message as read"""
        with self.lock:
            try:
                data = self._read_data()

                for msg in data["communications"]:
                    if msg["id"] == message_id:
                        msg["read"] = True
                        break

                self._write_data(data)

            except Exception as e:
                logger.error(f"Error marking message read: {e}")
    
    def update_status(self, agent_name: str, status: str, details: Dict = None):
        """Update agent status"""
        with self.lock:
            try:
                data = self._read_data()

                status_update = {
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_name,
                    "status": status,
                    "details": details or {}
                }

                data["status_updates"].append(status_update)

                # Keep only last 50 status updates
                if len(data["status_updates"]) > 50:
                    data["status_updates"] = data["status_updates"][-50:]

                self._write_data(data)

                logger.info(f"📊 {agent_name} status: {status}")

            except Exception as e:
                logger.error(f"Error updating status: {e}")
    
    def get_agent_status(self, agent_name: str = None) -> List[Dict]:
        """Get status updates for specific agent or all agents"""
        with self.lock:  # FIX: Added lock to prevent race conditions
            try:
                data = self._read_data()

                if agent_name:
                    return [
                        status for status in data["status_updates"]
                        if status["agent"] == agent_name
                    ]
                else:
                    return data["status_updates"]

            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return []
    
    def update_shared_context(self, key: str, value: Any):
        """Update shared context that all agents can access"""
        with self.lock:
            try:
                data = self._read_data()
                data["shared_context"][key] = value
                self._write_data(data)

                logger.info(f"🔄 Updated shared context: {key}")

            except Exception as e:
                logger.error(f"Error updating shared context: {e}")
    
    def get_shared_context(self, key: str = None):
        """Get shared context"""
        with self.lock:  # FIX: Added lock to prevent race conditions
            try:
                data = self._read_data()

                if key:
                    return data["shared_context"].get(key)
                else:
                    return data["shared_context"]

            except Exception as e:
                logger.error(f"Error getting shared context: {e}")
                return None
    
    def request_file_lock(self, agent_name: str, file_path: str) -> bool:
        """Request exclusive access to a file"""
        with self.lock:
            try:
                with open(self.communication_file, 'r') as f:
                    data = json.load(f)
                
                if file_path in data["file_locks"]:
                    return False  # File is already locked
                
                data["file_locks"][file_path] = {
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                }
                
                with open(self.communication_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logger.info(f"🔒 {agent_name} locked file: {file_path}")
                return True
                
            except Exception as e:
                logger.error(f"Error requesting file lock: {e}")
                return False
    
    def release_file_lock(self, agent_name: str, file_path: str):
        """Release file lock"""
        with self.lock:
            try:
                with open(self.communication_file, 'r') as f:
                    data = json.load(f)

                if file_path in data["file_locks"] and data["file_locks"][file_path]["agent"] == agent_name:
                    del data["file_locks"][file_path]

                    with open(self.communication_file, 'w') as f:
                        json.dump(data, f, indent=2)

                    logger.info(f"🔓 {agent_name} released file: {file_path}")

            except Exception as e:
                logger.error(f"Error releasing file lock: {e}")



    def acquire_lock(self, agent_name: str, file_path: str) -> bool:
        """Simplified lock acquisition - returns True if lock acquired, False if already locked"""
        with self.lock:
            try:
                data = self._read_data()

                # Check if file is already locked
                if file_path in data["file_locks"]:
                    return False  # File is already locked

                # Acquire the lock
                data["file_locks"][file_path] = {
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                }

                self._write_data(data)
                logger.info(f"🔒 {agent_name} acquired lock for: {file_path}")
                return True

            except Exception as e:
                logger.error(f"Error acquiring lock: {e}")
                return False

    def get_lock_holder(self, file_path: str) -> str:
        """Get the name of the agent holding the lock for a file"""
        with self.lock:
            try:
                data = self._read_data()

                if file_path in data["file_locks"]:
                    return data["file_locks"][file_path]["agent"]
                else:
                    return "No one"

            except Exception as e:
                logger.error(f"Error getting lock holder: {e}")
                return "Unknown"

    def report_integration_point(self, agent_name: str, component: str, interface: Dict):
        """Report an integration point for coordination"""
        with self.lock:
            try:
                data = self._read_data()

                integration_point = {
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_name,
                    "component": component,
                    "interface": interface
                }

                data["integration_points"].append(integration_point)
                self._write_data(data)

                logger.info(f"🔗 {agent_name} reported integration point: {component}")

            except Exception as e:
                logger.error(f"Error reporting integration point: {e}")

# Global communication hub instance
comm_hub = AgentCommunicationHub()

# Convenience functions for agents to use
def send_to_agent(from_agent: str, to_agent: str, message: str, msg_type: str = "info"):
    """Send message to another agent"""
    comm_hub.send_message(from_agent, to_agent, message, msg_type)

def get_my_messages(agent_name: str):
    """Get messages for this agent"""
    return comm_hub.get_messages(agent_name)

def update_my_status(agent_name: str, status: str, details: Dict = None):
    """Update this agent's status"""
    comm_hub.update_status(agent_name, status, details)

def share_context(key: str, value: Any):
    """Share context with all agents"""
    comm_hub.update_shared_context(key, value)

def get_context(key: str = None):
    """Get shared context"""
    return comm_hub.get_shared_context(key)

def lock_file(agent_name: str, file_path: str) -> bool:
    """Request file lock"""
    return comm_hub.request_file_lock(agent_name, file_path)

def unlock_file(agent_name: str, file_path: str):
    """Release file lock"""
    comm_hub.release_file_lock(agent_name, file_path)
