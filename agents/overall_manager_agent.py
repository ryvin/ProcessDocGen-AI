from crewai import Agent
from crewai_tools import tool

@tool
def review_documentation(test_feedback: str, process_details: str) -> str:
    """Review feedback from the virtual tester and determine the next steps for documentation improvement.

    Args:
        test_feedback (str): The feedback provided by the virtual tester after simulating the process.
        process_details (str): The name or details of the process being documented.

    Returns:
        str: A review summary determining whether the documentation is successful or requires revisions.
    """
    review = f"Feedback from tester on process '{process_details}': {test_feedback}\n"
    
    if "unclear" in test_feedback or "issue" in test_feedback:
        review += "Conclusion: The documentation is not yet successful. There are issues or unclear steps.\n"
        review += "Action: Send it back to the Documentation Agent for improvements based on the tester's feedback."
    else:
        review += "Conclusion: The documentation is successful and ready for use."

    return review

# Define the Overall Documentation Manager agent
overall_manager_agent = Agent(
    role="Overall Documentation Manager",
    goal="Review feedback from the virtual tester and determine if the documentation is successful.",
    backstory="You are responsible for ensuring the documentation is complete, realistic, and ready for use. If issues arise, you decide what improvements need to be made.",
    tools=[review_documentation],  # Attach the review tool
)
