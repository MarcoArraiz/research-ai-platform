from crewai import Crew, Process, Task
from src.agents.researcher import create_researcher_agent
from src.agents.analyst import create_analyst_agent
from src.agents.writer import create_writer_agent
from src.agents.critic import create_critic_agent
from src.agents.coordinator import create_coordinator_agent
from src.tools.web_search import create_search_tool
from src.tools.web_scraper import web_scraper

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic
        self.search_tool = create_search_tool()
        
    def run(self, task_callback=None, step_callback=None):
        # 1. Initialize Agents
        search_tools = [self.search_tool, web_scraper] if self.search_tool else [web_scraper]
        researcher = create_researcher_agent(search_tools)
        analyst = create_analyst_agent()
        writer = create_writer_agent()
        critic = create_critic_agent()
        coordinator = create_coordinator_agent()

        # 2. Define Tasks
        research_task = Task(
            description=f'Coordinate with the Senior Research Assistant to conduct a comprehensive research on {self.topic}. Gather news, key players, and technological breakthroughs.',
            expected_output='A raw collection of research data, facts, and sources provided by the researcher.',
            agent=researcher,
            callback=task_callback
        )

        analysis_task = Task(
            description=f'Direct the Tech Strategy Analyst to analyze the research data on {self.topic}. Identify 5 key trends and their industry impact.',
            expected_output='A structured technical analysis identifying trends, risks, and opportunities.',
            agent=analyst,
            callback=task_callback
        )

        writing_task = Task(
            description=f'Manage the Senior Technical Writer to create a professional Markdown report about {self.topic}. Ensure it includes Executive Summary and Key Findings.',
            expected_output='A complete, well-formatted Markdown report drafted by the writer.',
            agent=writer,
            callback=task_callback
        )

        review_task = Task(
            description=f'Supervise the Editorial Critic as they review the Markdown report for {self.topic}. Ensure accuracy, clarity, and professional tone.',
            expected_output='The final, polished version of the report after a total editorial review.',
            agent=critic,
            callback=task_callback
        )

        # 3. Assemble Crew
        crew = Crew(
            agents=[researcher, analyst, writer, critic],
            tasks=[research_task, analysis_task, writing_task, review_task],
            process=Process.hierarchical,
            manager_agent=coordinator,
            step_callback=step_callback,
            verbose=True
        )

        return crew.kickoff()
