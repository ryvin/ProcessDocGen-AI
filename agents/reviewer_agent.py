from crewai import Agent
from crewai_tools import tool

@tool
def review_process_documentation(documentation: str) -> str:
    """Review the process documentation for clarity, completeness, and accuracy.

    Args:
        documentation (str): The process documentation generated by the Documentation Agent.

    Returns:
        str: Feedback on the quality of the documentation.
    """
    feedback = f"Reviewing the following documentation:\n{documentation}\n"

    # Basic review simulation (this can be extended with specific checks)
    if "missing step" in documentation or "unclear" in documentation:
        feedback += "Conclusion: The documentation has unclear steps or missing details. Please revise.\n"
    else:
        feedback += "Conclusion: The documentation appears to be clear and complete."

    return feedback

# Define the Reviewer agent
reviewer_agent = Agent(
    role="Reviewer",
    goal="Review process documentation to ensure it is clear, complete, and accurate.",
    backstory="You are a documentation reviewer, ensuring that the generated process documentation meets quality standards before being tested by the Virtual Tester Agent.",
    tools=[review_process_documentation],  # Attach the review tool
)
