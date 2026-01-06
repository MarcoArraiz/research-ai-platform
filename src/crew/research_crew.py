from crewai import Crew, Process, Task
from src.agents.researcher import create_researcher_agent
from src.agents.analyst import create_analyst_agent
from src.agents.writer import create_writer_agent
from src.agents.critic import create_critic_agent
from src.tools.web_search import create_search_tool

class ResearchCrew:
    def __init__(self, topic):
        self.topic = topic
        self.search_tool = create_search_tool()
        
    def run(self):
        print(f"DEBUG: ResearchCrew.run() iniciado para tema: {self.topic}")
        # 1. Initialize Agents
        print("DEBUG: Inicializando agentes...")
        search_tools = [self.search_tool] if self.search_tool else []
        researcher = create_researcher_agent(search_tools)
        analyst = create_analyst_agent()
        writer = create_writer_agent()
        critic = create_critic_agent()

        # 2. Define Tasks
        research_task = Task(
            description=f'Conduct a comprehensive research on {self.topic}. Find the latest news, key players, and technological breakthroughs.',
            expected_output='A detailed collection of raw research data and sources.',
            agent=researcher
        )

        analysis_task = Task(
            description=f'Based on the research data, identify 5 key trends and their potential impact on the industry regarding {self.topic}.',
            expected_output='A structured analysis identifying trends, risks, and opportunities.',
            agent=analyst
        )

        writing_task = Task(
            description=f'Write a professional Markdown report about {self.topic} based on the analysis. Include an Executive Summary, Key Findings, and Conclusion.',
            expected_output='A complete, well-formatted Markdown report.',
            agent=writer
        )

        review_task = Task(
            description=f'Review the Markdown report for {self.topic}. Check for clarity, accuracy, and professional tone. Request changes if necessary.',
            expected_output='The final, polished version of the report in Markdown.',
            agent=critic
        )

        # 3. Assemble Crew
        crew = Crew(
            agents=[researcher, analyst, writer, critic],
            tasks=[research_task, analysis_task, writing_task, review_task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()
