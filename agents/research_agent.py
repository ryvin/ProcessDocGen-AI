from crewai import Agent
from crewai_tools import SerperDevTool
from crewai_tools import OllamaLLM

# Initialize the internet searching tool (using Serper as an example)
serper_tool = SerperDevTool()

class DocumentationAgent(Agent):
    def __init__(self, llm_provider=None):
        super().__init__(
    role="Subject Matter Expert",
    goal="Search for information about the topic and gather data to be referenced during documentation creation.",
    backstory="You are a subject matter expert with access to the internet to research any given topic.",
    tools=[serper_tool],  # Attach the internet searching tool
    llm=llm_provider  # Pass the LLM provider
)
