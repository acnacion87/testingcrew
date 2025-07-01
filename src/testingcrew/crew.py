import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import CodeDocsSearchTool
from typing import List
from pydantic import BaseModel

from dotenv import load_dotenv

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class Selectors(BaseModel):
    selectors: dict[str, dict[str, str]]
    
class Urls(BaseModel):
    urls: list[str]

@CrewBase
class Testingcrew():
    """Testingcrew crew"""

    def __init__(self, tools =[]):
        super().__init__()
        load_dotenv()
        self.tools = tools
        self.llm = LLM(
            model=os.getenv("MODEL"), # call model by provider/model_name
            temperature=0.0,
        )

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'], # type: ignore[index]
            tools=self.tools,
            llm=self.llm,
            verbose=True
        )

    @agent
    def ui_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_tester'], # type: ignore[index]
            tools=self.tools,
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def playwright_tester(self) -> Agent:
        tools = [CodeDocsSearchTool(docs_url="https://vitalets.github.io/playwright-bdd/#/api")].extend(self.tools)
        return Agent(
            config=self.agents_config['playwright_tester'], # type: ignore[index]
            tools=tools,
            llm=self.llm,
            verbose=True
        ) 

    @task
    def create_business_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_business_requirements_task'], # type: ignore[index]
            output_file="output/test.feature"
        )

    @task
    def generate_selectors_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_selectors_task'], # type: ignore[index]
            output_file="output/selectors.json",
            output_json=Selectors
        )

    @task
    def test_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_generation_task'], # type: ignore[index]
            output_file="output/test.spec.ts"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Testingcrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
