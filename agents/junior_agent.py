import os
from crewai import Agent, LLM
from crewai_tools import CodeDocsSearchTool, FileReadTool, FileWriterTool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini 2.0 Flash-Lite LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_tokens=8192
)

# Initialize tools for junior agent
code_search_tool = CodeDocsSearchTool(
    config=dict(
        llm=dict(
            provider="google-generativeai",
            config=dict(
                model="gemini/gemini-2.0-flash-lite",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.7,
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

junior_agent = Agent(
    role='Junior Game Developer',
    goal='Implement basic game mechanics, UI components, and helper functions for the idle game.',
    backstory='''You are an enthusiastic junior game developer with solid Python fundamentals and
    experience with tkinter/pygame. You specialize in implementing well-defined game features like
    resource systems, basic UI elements, and utility functions. You write clean, documented code
    and follow established patterns.''',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
    tools=[code_search_tool, file_read_tool, file_writer_tool],
    max_iter=3,
    memory=True
)