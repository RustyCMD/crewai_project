"""
Advanced Collaborative CrewAI Setup
Multi-agent parallel development environment with real-time communication
"""

import os
from crewai import Agent, LLM, Task, Crew, Process
from crewai_tools import FileWriterTool, FileReadTool, DirectorySearchTool
from collaborative_tools import (
    collaborative_file_writer,
    team_communication,
    integration_coordinator,
    project_status,
    file_lock_manager
)
from dotenv import load_dotenv
import logging
from agent_communication import comm_hub

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_tokens=8192
)

# Enhanced collaborative tools for all agents
collaborative_tools = [
    collaborative_file_writer,
    team_communication,
    integration_coordinator,
    project_status,
    FileReadTool(),
    DirectorySearchTool()
]

# File Lock Manager tools (only for the File Lock Manager agent)
file_lock_manager_tools = [
    file_lock_manager,
    team_communication,
    project_status,
    FileReadTool()
]

class CollaborativeAgentManager:
    """Manages collaborative agent communication and coordination"""
    
    def __init__(self):
        self.shared_context = {
            "project_status": {},
            "file_dependencies": {},
            "communication_log": [],
            "integration_points": []
        }
    
    def log_communication(self, from_agent, to_agent, message):
        """Log inter-agent communication"""
        self.communication_log.append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": "now"
        })

# Initialize collaborative manager
collab_manager = CollaborativeAgentManager()

# Frontend Developer Agent
frontend_agent = Agent(
    role='Frontend Developer',
    goal='Develop the user interface, GUI components, and visual elements of the idle game with real-time collaboration',
    backstory="""You are an expert frontend developer specializing in Python GUI development with tkinter.
    You work collaboratively with backend and integration teams, constantly communicating progress and 
    coordinating on shared interfaces. You proactively share updates and request feedback from other agents.""",
    verbose=True,
    allow_delegation=True,
    tools=collaborative_tools,
    llm=gemini_llm,
    max_iter=10,
    memory=True
)

# Backend Developer Agent  
backend_agent = Agent(
    role='Backend Developer',
    goal='Develop core game logic, systems, and data management with continuous coordination with frontend team',
    backstory="""You are a backend systems expert focused on game engines, resource management, and core logic.
    You actively collaborate with the frontend team to ensure seamless integration, regularly sharing API 
    specifications and system updates. You coordinate closely on data structures and system interfaces.""",
    verbose=True,
    allow_delegation=True,
    tools=collaborative_tools,
    llm=gemini_llm,
    max_iter=10,
    memory=True
)

# Integration Developer Agent
integration_agent = Agent(
    role='Integration Developer',
    goal='Coordinate between teams, manage dependencies, ensure system integration, and facilitate communication',
    backstory="""You are the integration specialist who ensures all components work together seamlessly.
    You actively monitor other agents' progress, identify integration points, resolve conflicts, and
    facilitate communication between frontend and backend teams. You're the coordination hub of the project.""",
    verbose=True,
    allow_delegation=True,
    tools=collaborative_tools,
    llm=gemini_llm,
    max_iter=15,
    memory=True
)

# Quality Assurance Agent
qa_agent = Agent(
    role='Quality Assurance Engineer',
    goal='Continuously test components, provide feedback to developers, and ensure code quality throughout development',
    backstory="""You are a QA engineer who works in parallel with development, providing real-time feedback
    and testing. You collaborate closely with all developers, running tests as they develop, identifying
    issues early, and ensuring quality standards are maintained throughout the collaborative process.""",
    verbose=True,
    allow_delegation=True,
    tools=collaborative_tools,
    llm=gemini_llm,
    max_iter=8,
    memory=True
)

# Performance Optimization Agent
performance_agent = Agent(
    role='Performance Engineer',
    goal='Monitor and optimize system performance, provide real-time optimization suggestions to developers',
    backstory="""You are a performance optimization specialist who works alongside the development team,
    continuously analyzing code for performance improvements, memory optimization, and efficiency gains.
    You provide real-time suggestions and collaborate on performance-critical components.""",
    verbose=True,
    allow_delegation=True,
    tools=collaborative_tools,
    llm=gemini_llm,
    max_iter=6,
    memory=True
)

# File Lock Manager Agent
file_lock_manager_agent = Agent(
    role='File Lock Manager',
    goal='Manage file access permissions, approve/deny file lock requests, and prevent file conflicts',
    backstory="""You are the File Lock Manager responsible for coordinating file access between all development agents.
    Your job is to review file lock requests, approve them when safe, and deny them when there would be conflicts.
    You work quickly to prevent development bottlenecks while ensuring file integrity. You approve requests that
    make sense and deny conflicting requests with clear explanations.""",
    verbose=True,
    allow_delegation=False,
    tools=file_lock_manager_tools,
    llm=gemini_llm,
    max_iter=5,
    memory=True
)

def create_collaborative_tasks():
    """Create interconnected tasks that require real-time collaboration"""
    
    # Frontend Development Task
    frontend_task = Task(
        description="""Develop the complete GUI framework and user interface components for the idle game.
        
        COLLABORATION REQUIREMENTS:
        - Continuously communicate with Backend Agent about data structures and API requirements
        - Coordinate with Integration Agent on component interfaces and dependencies
        - Share progress updates every major milestone
        - Request code reviews from QA Agent for UI components
        - Collaborate with Performance Agent on UI optimization
        
        DELIVERABLES (create in Game/frontend/):
        - Game/frontend/main_window.py: Main game window and layout
        - Game/frontend/resource_display.py: Resource visualization components
        - Game/frontend/upgrade_panel.py: Upgrade interface and controls
        - Game/frontend/game_controls.py: Start/stop, save/load controls
        - Game/frontend/theme_manager.py: Visual themes and styling
        - Game/frontend/animation_system.py: UI animations and effects
        
        COMMUNICATION PROTOCOL:
        - Send status updates to Integration Agent every 15 minutes of work
        - Request backend API specifications from Backend Agent
        - Coordinate with QA Agent on testing UI components
        - Share performance concerns with Performance Agent""",
        expected_output="""Complete frontend system with real-time collaboration logs showing:
        - All GUI components implemented and documented
        - Communication logs with other agents
        - Integration points clearly defined
        - Performance considerations documented
        - Code review feedback incorporated""",
        agent=frontend_agent
    )
    
    # Backend Development Task  
    backend_task = Task(
        description="""Develop the core game engine, systems, and data management.
        
        COLLABORATION REQUIREMENTS:
        - Provide API specifications to Frontend Agent for UI integration
        - Coordinate with Integration Agent on system architecture
        - Share data structure updates with all relevant agents
        - Collaborate with Performance Agent on optimization opportunities
        - Work with QA Agent on unit testing strategies
        
        DELIVERABLES (create in Game/backend/):
        - Game/backend/game_engine.py: Core game loop and state management
        - Game/backend/resource_system.py: Resource generation and management
        - Game/backend/upgrade_engine.py: Upgrade logic and progression
        - Game/backend/save_system.py: Data persistence and loading
        - Game/backend/event_system.py: Game events and notifications
        - Game/backend/achievement_engine.py: Achievement tracking and rewards
        
        COMMUNICATION PROTOCOL:
        - Share API specifications with Frontend Agent immediately upon creation
        - Notify Integration Agent of any architectural changes
        - Coordinate with Performance Agent on system optimization
        - Provide testing hooks for QA Agent""",
        expected_output="""Complete backend system with collaboration evidence:
        - All core systems implemented with clear APIs
        - Documentation of integration points
        - Communication logs with frontend team
        - Performance optimization notes
        - Testing interfaces provided""",
        agent=backend_agent
    )
    
    # Integration Coordination Task
    integration_task = Task(
        description="""Coordinate development between all agents, manage dependencies, and ensure seamless integration.

        COLLABORATION REQUIREMENTS:
        - Monitor progress of Frontend and Backend agents continuously
        - Facilitate communication between all team members
        - Identify and resolve integration conflicts in real-time
        - Coordinate shared file access and version control
        - Manage project timeline and dependencies

        DELIVERABLES (create in Game/integration/):
        - Game/integration/coordinator.py: Main integration coordinator
        - Game/integration/dependency_manager.py: Manage component dependencies
        - Game/integration/communication_hub.py: Inter-agent communication system
        - Game/integration/conflict_resolver.py: Handle integration conflicts
        - Game/integration/project_status.py: Real-time project status tracking

        COMMUNICATION PROTOCOL:
        - Check in with all agents every 10 minutes
        - Immediately address any integration conflicts
        - Maintain real-time project status dashboard
        - Coordinate code reviews and testing""",
        expected_output="""Integration coordination system with:
        - Real-time project status tracking
        - Communication logs between all agents
        - Dependency management system
        - Conflict resolution documentation
        - Integration test results""",
        agent=integration_agent
    )

    # Quality Assurance Task
    qa_task = Task(
        description="""Provide continuous testing and quality assurance throughout parallel development.

        COLLABORATION REQUIREMENTS:
        - Test components as they're developed by Frontend and Backend agents
        - Provide immediate feedback on code quality and bugs
        - Coordinate with Integration Agent on system-wide testing
        - Work with Performance Agent on performance testing

        DELIVERABLES (create in Game/qa/):
        - Game/qa/test_suite.py: Comprehensive test suite
        - Game/qa/continuous_testing.py: Real-time testing framework
        - Game/qa/quality_metrics.py: Code quality measurement
        - Game/qa/bug_tracker.py: Issue tracking and reporting

        COMMUNICATION PROTOCOL:
        - Provide immediate feedback on tested components
        - Report bugs and issues to relevant developers
        - Coordinate testing schedules with all agents""",
        expected_output="""Quality assurance system with:
        - Comprehensive test coverage
        - Real-time quality metrics
        - Bug reports and resolution tracking
        - Collaboration logs with development teams""",
        agent=qa_agent
    )

    # Performance Optimization Task
    performance_task = Task(
        description="""Continuously monitor and optimize system performance during development.

        COLLABORATION REQUIREMENTS:
        - Analyze code from Frontend and Backend agents for performance issues
        - Provide real-time optimization suggestions
        - Coordinate with Integration Agent on system-wide performance
        - Work with QA Agent on performance testing

        DELIVERABLES (create in Game/performance/):
        - Game/performance/profiler.py: Performance monitoring system
        - Game/performance/optimizer.py: Optimization recommendations
        - Game/performance/metrics.py: Performance metrics tracking

        COMMUNICATION PROTOCOL:
        - Provide immediate performance feedback
        - Suggest optimizations to relevant developers
        - Monitor system performance continuously""",
        expected_output="""Performance optimization system with:
        - Performance monitoring and profiling
        - Optimization recommendations
        - Performance metrics and trends
        - Collaboration logs with development teams""",
        agent=performance_agent
    )

    # File Lock Manager Task
    file_lock_task = Task(
        description="""Manage file access permissions and coordinate file locks between all development agents.

        RESPONSIBILITIES:
        - Monitor file lock requests from all agents
        - Approve file lock requests when safe (no conflicts)
        - Deny conflicting requests with clear explanations
        - Maintain file access coordination to prevent deadlocks
        - Respond quickly to prevent development bottlenecks

        WORKFLOW:
        1. Continuously monitor for file lock requests using file_lock_manager tool
        2. Review each request for potential conflicts
        3. Approve non-conflicting requests immediately
        4. Deny conflicting requests with clear reasons
        5. Use approve_all for batch approvals when safe

        COMMUNICATION PROTOCOL:
        - Check for new requests every 30 seconds
        - Approve requests within 1 minute when possible
        - Send clear denial reasons for rejected requests
        - Coordinate with Integration Agent on complex conflicts""",
        expected_output="""File lock management system with:
        - All file lock requests processed
        - Clear approval/denial decisions
        - No development bottlenecks from file access
        - Coordination logs with all agents""",
        agent=file_lock_manager_agent
    )

    return [frontend_task, backend_task, integration_task, qa_task, performance_task, file_lock_task]

def create_collaborative_crew():
    """Create the collaborative crew with hierarchical process for parallel execution"""

    tasks = create_collaborative_tasks()

    # Create crew with hierarchical process for parallel execution
    collaborative_crew = Crew(
        agents=[frontend_agent, backend_agent, integration_agent, qa_agent, performance_agent, file_lock_manager_agent],
        tasks=tasks,
        process=Process.hierarchical,  # Enables parallel execution with coordination
        manager_llm=gemini_llm,  # LLM for the manager agent in hierarchical process
        verbose=True,
        memory=True,  # Enable shared memory for collaboration
        max_rpm=4000,  # High rate limit for parallel execution
        share_crew=True,  # Enable crew sharing for inter-agent communication
        step_callback=lambda step: logger.info(f"Collaborative Step: {step}"),
        task_callback=lambda task: logger.info(f"Task Update: {task.description[:50]}...")
    )

    return collaborative_crew

def setup_collaboration_environment():
    """Set up the collaborative development environment"""

    # Create directory structure for collaborative development
    directories = [
        "Game/frontend",
        "Game/backend",
        "Game/integration",
        "Game/qa",
        "Game/performance",
        "Game/shared",
        "Game/docs"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

    # FIX: Use comm_hub.initialize_communication_file() instead of manual JSON creation
    # This ensures proper structure and consistency with the communication hub
    comm_hub.initialize_communication_file()

    logger.info("Collaborative environment setup complete!")

def run_collaborative_development():
    """Run the collaborative development process"""

    logger.info("🚀 Starting Advanced Collaborative CrewAI Development")
    logger.info("=" * 60)

    # Setup environment
    setup_collaboration_environment()

    # Create and run collaborative crew
    crew = create_collaborative_crew()

    logger.info("🤝 Launching parallel agent collaboration...")
    logger.info("Agents will work simultaneously with real-time communication")

    try:
        result = crew.kickoff()

        logger.info("✅ Collaborative development completed!")
        logger.info("=" * 60)

        return result

    except Exception as e:
        logger.error(f"❌ Error in collaborative development: {e}")
        return None

if __name__ == "__main__":
    run_collaborative_development()
