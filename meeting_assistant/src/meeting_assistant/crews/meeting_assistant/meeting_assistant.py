from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool

file_writer_tool_summary = FileWriterTool(file_name="summary.txt", directory="meeting_assistant")
file_writer_tool_action_items = FileWriterTool(file_name="action_items.txt", directory="meeting_assistant")
file_writer_tool_sentiment = FileWriterTool(file_name="sentiment.txt", directory="meeting_assistant")


@CrewBase
class MeetingAssistantCrew:
    """Poem Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def meeting_minutes_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_summarizer"],
        )

    @agent
    def meeting_minutes_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_writer"]
        )

    @task
    def meeting_minutes_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_summary_task"],
        )
    
    @task 
    def meeting_minutes_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_writing_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
