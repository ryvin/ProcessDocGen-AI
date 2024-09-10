from crewai import Agent
from crewai_tools import SerperDevTool
import ollama

# Function to use Ollama for generating LLM responses
def generate_llm_response(prompt):
    try:
        client = ollama.Client()
        response = client.chat(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        return response['message']
    except Exception as e:
        print(f"Error with Ollama LLM: {str(e)}")
        return "Error generating response."
    
def perform_research(query):
    research_prompt = f"Research the following topic: {query}"
    result = generate_llm_response(research_prompt)
    return result

# Initialize the internet searching tool (using Serper as an example)
serper_tool = SerperDevTool()

# Define the research agent
research_agent = Agent(
    role="Subject Matter Expert",
    goal="Search for information about the topic and gather data to be referenced during documentation creation.",
    backstory="You are a subject matter expert with access to the internet to research any given topic.",
    tools=[serper_tool],  # Attach the internet searching tool
    
)
