from crewai import Agent
from src.utils.config import config

def create_writer_agent():
    return Agent(
        role='Senior Technical Writer',
        goal='Create a professional and engaging research report on {topic}',
        backstory="""You are a professional writer specialized in technology and business.
        Your job is to take complex insights and present them in a clear, 
        concise, and well-structured Markdown report that is easy for executives to read.""",
        tools=[],
        memory=True,
        verbose=True,
        allow_delegation=False,
        openai_api_key=config.OPENAI_API_KEY
    )
