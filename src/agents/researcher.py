from crewai import Agent
from src.utils.config import config

def create_researcher_agent(tools):
    return Agent(
        role='Senior Research Assistant',
        goal='Uncover cutting-edge developments and detailed technical data in {topic}',
        backstory="""You are an expert at a technology research firm.
        Your skill lies in identifying the most relevant and recent information.
        You don't just stop at search results; you dive deep into web pages using your scraper 
        to extract the actual content that provides a solid foundation for analysis.""",
        tools=tools,
        memory=True,
        verbose=True,
        allow_delegation=False,
        openai_api_key=config.OPENAI_API_KEY
    )
