from crewai import Agent
from crewai_tools import tool

@tool
def simulate_process(process: str, environment: str, audience_level: str) -> str:
    """Simulate following the documented process in a virtual environment based on the audience's knowledge level.

    Args:
        process (str): The process steps to follow as described in the documentation.
        environment (str): The restrictions or conditions of the virtual environment.
        audience_level (str): The knowledge level of the target audience (e.g., beginner, expert).

    Returns:
        str: Feedback on what happened when following the process documentation.
    """
    feedback = f"Simulating the process for an audience with {audience_level} knowledge.\n"
    feedback += f"Environment conditions: {environment}\n"

    # Example outcome of following the process (can be made more dynamic based on real process testing)
    if "unclear" in process:
        feedback += "Outcome: The process was unclear at several steps. Specifically, Step 3 was missing details on how to set up the environment.\n"
        feedback += "Suggestion: Revise Step 3 and include specific instructions for the setup."
    else:
        feedback += "Outcome: The process was successful. All steps were clear, and the task was completed as expected."

    return feedback

# Define the Virtual Tester agent
virtual_tester_agent = Agent(
    role="Virtual Tester",
    goal="Simulate following the process documentation in a virtual environment and provide feedback.",
    backstory="You are a virtual tester who simulates performing the documented process under realistic conditions. Your goal is to follow the process and report back on the clarity and effectiveness of the documentation.",
    tools=[simulate_process],  # Attach the simulation tool
)
