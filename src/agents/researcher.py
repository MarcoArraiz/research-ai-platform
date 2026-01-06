from crewai import Agent
from src.utils.config import config

def create_researcher_agent(tools):
    return Agent(
        role='Senio Research Assistant',
        goal='Uncover cutting-edge developments in {topic}',
        backstory="""You are an expert at a technology research firm.
        Your skill lies in identifying the most relevant and recent information
        from various web sources to provide a solid foundation for analysis.""",
        tools=tools,
        memory=True,
        verbose=True,
        allow_delegation=True,
        openai_api_key=config.OPENAI_API_KEY
    )
