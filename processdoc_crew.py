import os
import json
from datetime import datetime
from crewai import Crew, Process
from tasks.create_tasks import (
    create_research_task, create_requirements_task, 
    create_documentation_task, create_virtual_test_task, create_review_task
)
from utils.file_utils import handle_uploaded_file, list_files_in_directory
from dotenv import load_dotenv

load_dotenv()
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')
LLM_PROVIDER = "Ollama"  # Use Ollama as the default LLM
PROCESS_HISTORY_PATH = "./process_history.json"

def load_process_history():
    """Load the history of previously generated process documentation.

    Returns:
        list: A list of dictionaries representing past process documentation.
    """
    if os.path.exists(PROCESS_HISTORY_PATH):
        with open(PROCESS_HISTORY_PATH, 'r') as file:
            return json.load(file)
    return []

def save_process_to_history(process_name, file_path, feedback=""):
    """Save a new process entry to the process history file.

    Args:
        process_name (str): Name of the process.
        file_path (str): Path where the process documentation is saved.
        feedback (str): Any feedback related to the process.
    """
    process_history = load_process_history()
    new_entry = {
        "process_name": process_name,
        "file_path": file_path,
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
        "feedback": feedback
    }
    process_history.append(new_entry)

    # Save the updated history
    with open(PROCESS_HISTORY_PATH, 'w') as file:
        json.dump(process_history, file, indent=4)

def list_previous_processes():
    """List previously generated process documentation."""
    process_history = load_process_history()

    if not process_history:
        print("No process documentation has been generated yet.")
        return None
    
    print("Previously generated process documentation:")
    for idx, entry in enumerate(process_history, 1):
        print(f"{idx}. {entry['process_name']} (Generated on: {entry['generated_date']})")

    choice = input("Select a process to rerun or reference (Enter the number, or press Enter to skip): ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(process_history):
        selected_process = process_history[int(choice) - 1]
        action = input(f"Do you want to rerun (r) or reference (ref) the '{selected_process['process_name']}' documentation? (r/ref): ")
        if action == 'r':
            return {"action": "rerun", "process": selected_process}
        elif action == 'ref':
            return {"action": "reference", "process": selected_process}
    
    return None

def select_files_to_reference(directory):
    """List files in a specified directory and allow the user to select files for referencing.

    Args:
        directory (str): The directory path.

    Returns:
        list: List of file paths selected by the user for referencing.
    """
    files = list_files_in_directory(directory)

    if not files:
        print(f"No files found in directory: {directory}")
        return []

    print("Available files in the directory:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    selected_files = input("Enter the numbers of the files you want to include (comma-separated): ")
    selected_indices = selected_files.split(",")

    # Validate selected indices and return the corresponding file paths
    selected_paths = []
    for idx in selected_indices:
        if idx.strip().isdigit() and 1 <= int(idx.strip()) <= len(files):
            selected_paths.append(files[int(idx.strip()) - 1])

    return selected_paths

def get_user_input():
    """Collect user inputs for the process documentation."""
    previous_process = list_previous_processes()

    if previous_process and previous_process['action'] == 'rerun':
        # If rerunning, return the old process for improvement
        return previous_process['process'], 'rerun'
    
    process_name = input("What process would you like to document? ")

    directory = input("Provide a directory path to reference files (PDF, DOCX, TXT, MD, etc.): ")
    referenced_files = select_files_to_reference(directory)
    
    existing_docs = "\n".join([handle_uploaded_file(file) for file in referenced_files])
    
    target_audience = input("Who is the target audience (e.g., developers, managers, end-users)? ")
    environment = input("What are the restrictions or environment considerations for performing the process? ")

    # Create a new entry
    return {
        'process_name': process_name,
        'existing_docs': existing_docs,
        'target_audience': target_audience,
        'environment': environment
    }, 'new'

def main():
    """Main function to execute the documentation creation crew."""
    # Collect user input (either new process or rerun existing one)
    user_input, mode = get_user_input()

    if mode == 'rerun':
        print(f"Rerunning process: {user_input['process_name']}")
        user_input['existing_docs'] = user_input['process']['feedback']
    
    # Create research task
    research_task = create_research_task(user_input['process_name'])
    
    # Create requirements gathering task
    requirements_task = create_requirements_task(user_input['process_name'])

    # Create documentation task (RAG)
    combined_context = f"{user_input['existing_docs']} {research_task.expected_output} {requirements_task.expected_output}"
    documentation_task = create_documentation_task(user_input['process_name'], combined_context)
    
    # Create virtual testing task
    virtual_test_task = create_virtual_test_task(
        process=documentation_task.expected_output, 
        environment=user_input['environment'], 
        audience_level=user_input['target_audience']
    )

    # Create review task
    review_task = create_review_task(virtual_test_task.expected_output, user_input['process_name'])
    
    # Create crew and run all tasks sequentially
    crew = Crew(
        agents=[
            research_task.agent, requirements_task.agent, 
            documentation_task.agent, virtual_test_task.agent, review_task.agent
        ],
        tasks=[research_task, requirements_task, documentation_task, virtual_test_task, review_task],
        process=Process.sequential
    )

    # Run the tasks and store the result
    result = crew.kickoff(inputs=user_input)
    
    # Save the newly generated process to history
    if mode == 'new':
        save_process_to_history(user_input['process_name'], "./path/to/saved_document.md", review_task.expected_output)

    print(result)

if __name__ == "__main__":
    main()
