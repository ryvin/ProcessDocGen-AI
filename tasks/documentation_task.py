def create_documentation_task(user_inputs):
    """Dynamically creates a documentation task based on user inputs.

    Args:
        user_inputs (dict): Dictionary containing 'process', 'notes', and 'audience'.

    Returns:
        Task: A task object that describes the process documentation task.
    """
    process = user_inputs.get('process', 'a general process')
    notes = user_inputs.get('notes', 'No additional notes provided.')
    audience = user_inputs.get('audience', 'a general audience')

    # Use existing notes in the task description if provided
    task_description = (
        f"Create detailed documentation for the following process: {process}.\n"
        f"Existing notes: {notes}.\n"
        f"Target audience: {audience}. Adjust the complexity and tone accordingly."
    )

    expected_output = (
        f"A well-structured documentation suitable for {audience}, "
        f"explaining the process '{process}' clearly and concisely."
    )

    # Create the documentation task dynamically
    return Task(
        description=task_description,
        expected_output=expected_output,
        tools=documentation_agent.tools,  # Use the tools defined in the agent
        agent=documentation_agent         # Attach the agent to the task
    )
