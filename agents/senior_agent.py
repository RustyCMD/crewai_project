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
    temperature=0.5,
    max_tokens=8192
)

# Initialize tools for senior agent
code_search_tool = CodeDocsSearchTool(
    config=dict(
        llm=dict(
            provider="google-generativeai",
            config=dict(
                model="gemini/gemini-2.5-flash-lite",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.5,
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

senior_agent = Agent(
    role='Senior Game Architect',
    goal='Design and implement complex game systems, architecture, and advanced features for the idle game.',
    backstory='''You are a senior game developer with 8+ years of experience in Python game development.
    You excel at designing scalable game architectures, implementing complex systems like save/load
    mechanisms, achievement systems, and game balance. You mentor junior developers and ensure
    code quality and performance optimization.''',
    verbose=True,
    allow_delegation=True,
    llm=gemini_llm,
    tools=[code_search_tool, file_read_tool, file_writer_tool, directory_search_tool],
    max_iter=25,
    memory=True
)