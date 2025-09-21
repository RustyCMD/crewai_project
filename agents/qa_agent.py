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
    temperature=0.3,
    max_tokens=8192
)

# Initialize tools for QA agent
code_search_tool = CodeDocsSearchTool(
    config=dict(
        llm=dict(
            provider="google-generativeai",
            config=dict(
                model="gemini/gemini-2.0-flash-lite",
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.3,
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

qa_agent = Agent(
    role='Game QA Engineer',
    goal='Ensure game quality, balance, and user experience through comprehensive testing.',
    backstory='''You are a specialized game QA engineer with expertise in testing idle/incremental games.
    You focus on game balance testing, progression validation, save/load functionality, UI/UX testing,
    and performance optimization. You create comprehensive test plans and identify edge cases that
    could break the game experience.''',
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
    tools=[code_search_tool, file_read_tool, file_writer_tool],
    max_iter=4,
    memory=True
)