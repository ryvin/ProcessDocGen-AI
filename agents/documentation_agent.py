from crewai import Agent
from agents.research_agent import research_agent
from agents.requirements_agent import requirements_agent
from crewai_tools import tool

@tool
def openai_tool_with_rag(prompt: str, context: str) -> str:
    """Tool to interact with OpenAI's GPT-3/4 using RAG-style generation.

    Args:
        prompt (str): The input text to send to OpenAI's model.
        context (str): Additional referenceable context data from research and requirements.

    Returns:
        str: The model's response to the prompt.
    """
    # Combine context and prompt to form the complete input
    complete_prompt = f"Context: {context}\nPrompt: {prompt}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=complete_prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()

# Define the documentation agent
documentation_agent = Agent(
    role="Documentation Specialist",
    goal="Generate comprehensive process documentation by referencing research data and requirements.",
    backstory="You are a specialist in writing process documentation and use data from other experts.",
    tools=[openai_tool_with_rag],  # Attach the OpenAI tool with RAG-style generation
)
