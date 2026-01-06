from crewai import Agent
from src.utils.config import config

def create_critic_agent():
    return Agent(
        role='Editorial Critic',
        goal='Ensure the final report on {topic} is accurate, professional, and follows best practices',
        backstory="""You are a perfectionist editor. Your role is to review the final report,
        checking for factual consistency, tone, and formatting issues. 
        You provide critical feedback to ensure the output is world-class.""",
        tools=[],
        memory=True,
        verbose=True,
        allow_delegation=False,
        openai_api_key=config.OPENAI_API_KEY
    )
