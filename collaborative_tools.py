"""
Collaborative Development Tools
Enhanced tools for multi-agent collaborative development
"""

import os
import json
from typing import Dict, List, Any
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from agent_communication import comm_hub
import logging

logger = logging.getLogger(__name__)

class CollaborativeFileWriterTool(BaseTool):
    """File writer with collaboration features"""
    name: str = "collaborative_file_writer"
    description: str = "Write files with collaboration awareness, conflict detection, and team notifications"
    
    def _run(self, file_path: str, content: str, agent_name: str = "Frontend Developer") -> str:
        """Write file with collaboration features"""
        try:
            # Request file lock and wait for approval
            lock_result = comm_hub.request_file_lock_with_approval(agent_name, file_path)
            if not lock_result["approved"]:
                return f"❌ File lock request denied: {lock_result['reason']}"
            
            # Check if file exists and notify other agents
            file_exists = os.path.exists(file_path)
            if file_exists:
                comm_hub.send_message(
                    agent_name, 
                    "all", 
                    f"Modifying existing file: {file_path}",
                    "file_modification"
                )
            else:
                comm_hub.send_message(
                    agent_name,
                    "all", 
                    f"Creating new file: {file_path}",
                    "file_creation"
                )
            
            # Write the file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update status and notify team
            comm_hub.update_status(agent_name, f"Created/Updated {file_path}", {
                "file_path": file_path,
                "lines": len(content.split('\n')),
                "action": "created" if not file_exists else "modified"
            })
            
            # Release file lock
            comm_hub.release_file_lock(agent_name, file_path)
            
            logger.info(f"✅ {agent_name} successfully wrote {file_path}")
            return f"✅ Successfully wrote {file_path}. Team has been notified."
            
        except Exception as e:
            error_msg = f"❌ Error writing {file_path}: {str(e)}"
            logger.error(error_msg)
            return error_msg

class TeamCommunicationTool(BaseTool):
    """Tool for inter-agent communication"""
    name: str = "team_communication"
    description: str = "Send messages to other agents, request code reviews, and coordinate development"
    
    def _run(self, action: str, **kwargs) -> str:
        """Handle team communication actions"""
        try:
            # If action is a message itself, treat it as send_message
            if action not in ["send_message", "get_messages", "request_review", "share_progress"]:
                # Treat the action as the message content
                message = action
                from_agent = kwargs.get("from_agent", "Frontend Developer")
                to_agent = kwargs.get("to_agent", "all")
                msg_type = kwargs.get("type", "info")

                comm_hub.send_message(from_agent, to_agent, message, msg_type)
                return f"✅ Message sent to {to_agent}: {message[:50]}..."

            elif action == "send_message":
                from_agent = kwargs.get("from_agent", "unknown")
                to_agent = kwargs.get("to_agent", "all")
                message = kwargs.get("message", "")
                msg_type = kwargs.get("type", "info")

                comm_hub.send_message(from_agent, to_agent, message, msg_type)
                return f"✅ Message sent to {to_agent}"
                
            elif action == "get_messages":
                agent_name = kwargs.get("agent_name", "unknown")
                messages = comm_hub.get_messages(agent_name)
                
                if not messages:
                    return "📭 No new messages"
                
                result = "📬 New messages:\n"
                # FIX: Process ALL messages, not just the last 5
                for msg in messages:
                    result += f"- From {msg['from_agent']}: {msg['message']}\n"
                    comm_hub.mark_message_read(msg['id'])
                
                return result
                
            elif action == "request_review":
                from_agent = kwargs.get("from_agent", "unknown")
                file_path = kwargs.get("file_path", "")
                reviewer = kwargs.get("reviewer", "qa_agent")
                
                message = f"Please review {file_path} - ready for code review"
                comm_hub.send_message(from_agent, reviewer, message, "code_review_request")
                return f"✅ Code review requested from {reviewer}"
                
            elif action == "share_progress":
                agent_name = kwargs.get("agent_name", "unknown")
                progress = kwargs.get("progress", "")
                details = kwargs.get("details", {})
                
                comm_hub.update_status(agent_name, progress, details)
                comm_hub.send_message(agent_name, "all", f"Progress update: {progress}", "progress")
                return "✅ Progress shared with team"
                
            else:
                return f"❌ Unknown action: {action}"
                
        except Exception as e:
            error_msg = f"❌ Communication error: {str(e)}"
            logger.error(error_msg)
            return error_msg

class IntegrationCoordinatorTool(BaseTool):
    """Tool for managing integration points and dependencies"""
    name: str = "integration_coordinator"
    description: str = "Coordinate integration points, manage dependencies, and resolve conflicts"
    
    def _run(self, action: str, **kwargs) -> str:
        """Handle integration coordination actions"""
        try:
            # If action is not a known command, treat it as a general integration message
            if action not in ["register_interface", "check_dependencies", "report_conflict"]:
                message = action
                agent_name = kwargs.get("agent_name", "Integration Agent")

                comm_hub.send_message(
                    agent_name,
                    "all",
                    f"Integration: {message}",
                    "integration"
                )
                return f"✅ Integration message sent: {message[:50]}..."

            elif action == "register_interface":
                agent_name = kwargs.get("agent_name", "unknown")
                component = kwargs.get("component", "")
                interface = kwargs.get("interface", {})

                comm_hub.report_integration_point(agent_name, component, interface)
                comm_hub.send_message(
                    agent_name,
                    "integration_agent",
                    f"New interface registered: {component}",
                    "integration_point"
                )
                return f"✅ Interface registered for {component}"
                
            elif action == "check_dependencies":
                component = kwargs.get("component", "")
                
                # Get all integration points
                with open(comm_hub.communication_file, 'r') as f:
                    data = json.load(f)
                
                dependencies = [
                    point for point in data["integration_points"]
                    if component in point.get("interface", {}).get("dependencies", [])
                ]
                
                if dependencies:
                    result = f"📋 Dependencies for {component}:\n"
                    for dep in dependencies:
                        result += f"- {dep['component']} by {dep['agent']}\n"
                    return result
                else:
                    return f"✅ No dependencies found for {component}"
                    
            elif action == "report_conflict":
                agent_name = kwargs.get("agent_name", "unknown")
                conflict_details = kwargs.get("conflict", "")
                
                comm_hub.send_message(
                    agent_name,
                    "integration_agent",
                    f"CONFLICT DETECTED: {conflict_details}",
                    "conflict"
                )
                return "⚠️ Conflict reported to integration team"
                
            else:
                return f"❌ Unknown integration action: {action}"
                
        except Exception as e:
            error_msg = f"❌ Integration error: {str(e)}"
            logger.error(error_msg)
            return error_msg

class FileLockManagerTool(BaseTool):
    name: str = "file_lock_manager"
    description: str = "Manage file lock requests - approve or deny file access for other agents"

    def _run(self, action: str, request_id: str = None, reason: str = None) -> str:
        """Manage file lock requests"""
        try:
            from datetime import datetime

            # FIX: Use proper locking to prevent race conditions
            with comm_hub.lock:
                data = comm_hub._read_data()

                if action == "list_requests":
                    pending_requests = [r for r in data["file_lock_requests"] if r["status"] == "pending"]
                    if not pending_requests:
                        return "📋 No pending file lock requests"

                    result = "📋 Pending File Lock Requests:\n"
                    for i, request in enumerate(pending_requests, 1):
                        result += f"{i}. {request['agent']} wants {request['file_path']} (ID: {request['id']})\n"
                    return result

                elif action == "approve" and request_id:
                    # Find and approve the request
                    for request in data["file_lock_requests"]:
                        if request["id"] == request_id and request["status"] == "pending":
                            request["status"] = "approved"
                            request["approval_time"] = datetime.now().isoformat()
                            comm_hub._write_data(data)

                            # Send approval message outside the lock
                            comm_hub.send_message(
                                "File Lock Manager",
                                request["agent"],
                                f"File lock approved for {request['file_path']}",
                                "file_lock_approval"
                            )

                            logger.info(f"✅ File Lock Manager approved {request['agent']} for {request['file_path']}")
                            return f"✅ Approved file lock for {request['agent']} on {request['file_path']}"

                    return f"❌ Request {request_id} not found or already processed"

                elif action == "deny" and request_id:
                    # Find and deny the request
                    for request in data["file_lock_requests"]:
                        if request["id"] == request_id and request["status"] == "pending":
                            request["status"] = "denied"
                            request["denial_reason"] = reason or "Denied by File Lock Manager"
                            request["denial_time"] = datetime.now().isoformat()
                            comm_hub._write_data(data)

                            # Send denial message outside the lock
                            comm_hub.send_message(
                                "File Lock Manager",
                                request["agent"],
                                f"File lock denied for {request['file_path']}: {request['denial_reason']}",
                                "file_lock_denial"
                            )

                            logger.info(f"❌ File Lock Manager denied {request['agent']} for {request['file_path']}")
                            return f"❌ Denied file lock for {request['agent']} on {request['file_path']}: {request['denial_reason']}"

                    return f"❌ Request {request_id} not found or already processed"

                elif action == "approve_all":
                    approved_count = 0
                    approved_requests = []

                    for request in data["file_lock_requests"]:
                        if request["status"] == "pending":
                            request["status"] = "approved"
                            request["approval_time"] = datetime.now().isoformat()
                            approved_count += 1
                            approved_requests.append(request)

                    if approved_count > 0:
                        comm_hub._write_data(data)

                        # Send approval messages outside the lock
                        for request in approved_requests:
                            comm_hub.send_message(
                                "File Lock Manager",
                                request["agent"],
                                f"File lock approved for {request['file_path']}",
                                "file_lock_approval"
                            )

                        logger.info(f"✅ File Lock Manager approved {approved_count} requests")
                        return f"✅ Approved {approved_count} file lock requests"
                    else:
                        return "📋 No pending requests to approve"

                else:
                    return "❌ Invalid action. Use: list_requests, approve, deny, or approve_all"

        except Exception as e:
            error_msg = f"❌ Error managing file locks: {str(e)}"
            logger.error(error_msg)
            return error_msg

class ProjectStatusTool(BaseTool):
    """Tool for checking project status and team progress"""
    name: str = "project_status"
    description: str = "Check project status, team progress, and coordination information"
    
    def _run(self, action: str, **kwargs) -> str:
        """Handle project status actions"""
        try:
            # If action is not a known command, treat it as a status request
            if action not in ["team_status", "file_status", "integration_status"]:
                # Default to team_status for any unknown action
                action = "team_status"

            if action == "team_status":
                status_updates = comm_hub.get_agent_status()

                if not status_updates:
                    return "📊 No status updates available"

                # Group by agent
                agent_status = {}
                for update in status_updates[-20:]:  # Last 20 updates
                    agent = update["agent"]
                    if agent not in agent_status:
                        agent_status[agent] = []
                    agent_status[agent].append(update)

                result = "📊 Team Status:\n"
                for agent, updates in agent_status.items():
                    latest = updates[-1]
                    result += f"- {agent}: {latest['status']}\n"

                return result
                
            elif action == "file_status":
                with open(comm_hub.communication_file, 'r') as f:
                    data = json.load(f)
                
                if data["file_locks"]:
                    result = "🔒 Locked files:\n"
                    for file_path, lock_info in data["file_locks"].items():
                        result += f"- {file_path} (locked by {lock_info['agent']})\n"
                    return result
                else:
                    return "✅ No files currently locked"
                    
            elif action == "integration_status":
                with open(comm_hub.communication_file, 'r') as f:
                    data = json.load(f)
                
                points = data["integration_points"]
                if points:
                    result = "🔗 Integration Points:\n"
                    for point in points[-10:]:  # Last 10 points
                        result += f"- {point['component']} by {point['agent']}\n"
                    return result
                else:
                    return "📋 No integration points registered yet"
                    
            else:
                return f"❌ Unknown status action: {action}"
                
        except Exception as e:
            error_msg = f"❌ Status error: {str(e)}"
            logger.error(error_msg)
            return error_msg

# Create tool instances
collaborative_file_writer = CollaborativeFileWriterTool()
team_communication = TeamCommunicationTool()
integration_coordinator = IntegrationCoordinatorTool()
project_status = ProjectStatusTool()
file_lock_manager = FileLockManagerTool()
