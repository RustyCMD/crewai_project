import os
from crewai import Crew, Process
from agents.junior_agent import junior_agent
from agents.senior_agent import senior_agent
from agents.qa_agent import qa_agent
from agents.devops_agent import devops_agent
from tasks import architecture_task, features_task, testing_task, deployment_task

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def create_idle_game_crew():
    """
    Create and configure the CrewAI team for idle game development.

    Returns:
        Crew: Configured crew with agents and tasks for game development
    """

    # Assign agents to tasks
    architecture_task.agent = senior_agent
    features_task.agent = junior_agent
    testing_task.agent = qa_agent
    deployment_task.agent = devops_agent

    # Create the game development crew
    idle_game_crew = Crew(
        agents=[senior_agent, junior_agent, qa_agent, devops_agent],
        tasks=[architecture_task, features_task, testing_task, deployment_task],
        process=Process.sequential,
        verbose=True,
        memory=True,  # Re-enabled with Gemini embeddings
        embedder={
            "provider": "google-generativeai",
            "api_key": os.getenv("GEMINI_API_KEY")
        }
    )

    return idle_game_crew

# Create the crew instance
game_dev_crew = create_idle_game_crew()