from crewai import Agent
from crewai_tools import SerperDevTool  # Alternatively, use a specific tool for requirements analysis

# Initialize the research tool for requirements gathering
serper_tool = SerperDevTool()

# Define the requirements agent
requirements_agent = Agent(
    role="Requirements Analyst",
    goal="Understand and gather any requirements, constraints, or compliance considerations for the process.",
    backstory="You are an analyst specializing in identifying and documenting business requirements, rules, and compliance constraints.",
    tools=[serper_tool],  # Attach the internet searching tool or custom checklist
)
