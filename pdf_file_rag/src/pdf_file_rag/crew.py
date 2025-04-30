from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class PdfFileRag():
    """PdfFileRag crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    def pdf_file_rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_file_rag_agent'],
            verbose=True
        )

    @agent
    def pdf_file_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_file_summary_agent'], 
            verbose=True
        )

    
    @task
    def pdf_file_rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_file_rag_task'], 
        )

    @task
    def pdf_file_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_file_summary_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PdfFileRag crew"""
       
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
