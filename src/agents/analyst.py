from crewai import Agent
from src.utils.config import config

def create_analyst_agent():
    return Agent(
        role='Tech Strategy Analyst',
        goal='Analyze the collected data on {topic} to identify key trends and insights',
        backstory="""You are a seasoned analyst with a knack for seeing the big picture.
        You take raw research data and transform it into strategic insights,
        identifying risks, opportunities, and future implications.""",
        tools=[],
        memory=True,
        verbose=True,
        allow_delegation=False,
        openai_api_key=config.OPENAI_API_KEY
    )
