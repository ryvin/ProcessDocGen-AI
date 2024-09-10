from crewai import Task
from agents.research_agent import research_agent
from agents.requirements_agent import requirements_agent
from agents.documentation_agent import documentation_agent
from agents.virtual_tester_agent import virtual_tester_agent
from agents.overall_manager_agent import overall_manager_agent
import json
import logging
import readline  # Enables auto-completion in CLI
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROCESS_HISTORY_PATH = 'process_history.json'

# Helper function to load process history
def load_process_history():
    try:
        if os.path.exists(PROCESS_HISTORY_PATH):
            with open(PROCESS_HISTORY_PATH, 'r') as file:
                return json.load(file)
        return []
    except Exception as e:
        logger.error(f"Error loading process history: {str(e)}")
        return []

# Helper function to save process to history
def save_process_to_history(process_name, file_path, feedback=""):
    try:
        process_history = load_process_history()
        new_entry = {
            "process_name": process_name,
            "file_path": file_path,
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "feedback": feedback
        }
        process_history.append(new_entry)

        with open(PROCESS_HISTORY_PATH, 'w') as file:
            json.dump(process_history, file, indent=4)
    except Exception as e:
        logger.error(f"Error saving process to history: {str(e)}")

# Task creation function (dynamically based on inputs or process history)
def create_task(task_type=None):
    """Dynamically create tasks based on user input or process history"""
    try:
        # Get process history if available
        process_history = load_process_history()
        previous_tasks = [entry["process_name"] for entry in process_history]

        if task_type:
            task_name = input(f"Enter the name of the {task_type} task: ")
            task_description = input(f"Describe the task {task_name}: ")
            logger.info(f"Created new task: {task_name}")
        else:
            logger.info("No task type provided. Attempting to select from process history...")
            print("Previously documented tasks:")
            for idx, process in enumerate(previous_tasks, 1):
                print(f"{idx}. {process}")
            
            selected_task = input("Enter the number of the process to rerun or create a new task: ")
            if selected_task.isdigit() and 1 <= int(selected_task) <= len(previous_tasks):
                task_name = previous_tasks[int(selected_task) - 1]
                task_description = f"Rerunning {task_name}"
            else:
                task_name = input("Enter the name of the new task: ")
                task_description = input(f"Describe the task {task_name}: ")

        return {"name": task_name, "description": task_description}
    
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return None

# Interactive CLI function with auto-completion
def interactive_cli():
    """Interactive CLI with auto-completion and task selection"""
    def completer(text, state):
        options = [task for task in load_process_history() if task["process_name"].startswith(text)]
        if state < len(options):
            return options[state]["process_name"]
        return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    
    while True:
        user_input = input("Enter a command (type 'exit' to quit): ")
        if user_input == 'exit':
            break
        elif user_input == 'new':
            create_task(task_type='new')
        elif user_input == 'rerun':
            create_task()
        else:
            print(f"Unrecognized command: {user_input}")

# Improved Virtual Tester feedback
def virtual_tester_feedback(process_steps, environment, audience_level):
    """Simulate process testing and provide feedback based on audience knowledge level"""
    logger.info(f"Simulating process for an audience with {audience_level} knowledge level.")
    feedback = f"Simulating the process for an audience with {audience_level} knowledge.\n"
    feedback += f"Environment conditions: {environment}\n"

    unclear_steps = [step for step in process_steps if "unclear" in step.lower()]
    
    if unclear_steps:
        feedback += f"The following steps were unclear: {', '.join(unclear_steps)}.\n"
        feedback += "Suggestions: Revise the unclear steps to include more specific instructions.\n"
    else:
        feedback += "The process was successfully completed with all steps clear and actionable.\n"
    
    return feedback

def create_research_task(topic):
    """Creates a research task for the research agent."""
    return Task(
        description=f"Research information about the topic '{topic}' and gather referenceable data.",
        expected_output="A collection of information on the given topic, including key points and relevant facts.",
        agent=research_agent
    )

def create_requirements_task(process_name):
    """Creates a requirements gathering task for the requirements agent."""
    return Task(
        description=f"Identify and gather any requirements for the process '{process_name}', including constraints and compliance needs.",
        expected_output="A document listing all business requirements, rules, and compliance constraints.",
        agent=requirements_agent
    )

def create_documentation_task(topic, context):
    """Creates a documentation generation task that references the research and requirements data."""
    return Task(
        description=f"Generate documentation for the process '{topic}' using the provided context.",
        expected_output="Comprehensive documentation that includes process steps, requirements, and background information.",
        tools=documentation_agent.tools,
        agent=documentation_agent,
        inputs={"context": context}  # Pass context to the documentation agent
    )

def create_virtual_test_task(process, environment, audience_level):
    """Creates a virtual testing task for the virtual tester agent."""
    return Task(
        description=f"Simulate performing the process '{process}' in a virtual environment with restrictions '{environment}' "
                    f"and provide feedback.",
        expected_output="A detailed report on the outcomes of following the process and suggestions for improvement.",
        agent=virtual_tester_agent,
        inputs={"process": process, "environment": environment, "audience_level": audience_level}
    )

def create_review_task(test_feedback, process_details):
    """Creates a review task for the overall documentation manager."""
    return Task(
        description=f"Review the feedback from the virtual tester on the process '{process_details}' and determine the next steps.",
        expected_output="A review report determining if the documentation is successful or needs to be revised.",
        agent=overall_manager_agent,
        inputs={"test_feedback": test_feedback, "process_details": process_details}
    )


# Example of using auto-complete CLI
if __name__ == "__main__":
    interactive_cli()  # Start the interactive CLI with auto-completion
