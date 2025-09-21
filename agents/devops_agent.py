import os
from crewai import Agent, LLM
from crewai_tools import CodeDocsSearchTool, FileReadTool, FileWriterTool, DirectorySearchTool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini 2.5 Flash-Lite LLM
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4,
    max_tokens=8192
)

# Initialize tools for DevOps agent
code_search_tool = CodeDocsSearchTool(
    config=dict(
        llm=dict(
            provider="google-generativeai",
            config=dict(
                model="gemini/gemini-2.5-flash-lite",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.4,
            ),
        ),
        embedder=dict(
            provider="google-generativeai",
            config=dict(
                model="models/embedding-001",
                api_key=os.getenv("GEMINI_API_KEY"),
                task_type="retrieval_document",
            ),
        ),
    )
)
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()
directory_search_tool = DirectorySearchTool()

devops_agent = Agent(
    role='Game DevOps Engineer',
    goal='Handle game packaging, distribution, and deployment infrastructure for the idle game.',
    backstory='''You are a DevOps engineer specializing in Python game deployment and distribution.
    You handle creating executable builds, setting up auto-updaters, managing game assets,
    creating installation packages, and ensuring smooth deployment across different platforms.
    You also manage version control and release pipelines.''',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
    tools=[code_search_tool, file_read_tool, file_writer_tool, directory_search_tool],
    max_iter=15,
    memory=True
)