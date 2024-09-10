# Process Documentation Generator with AI Agents

This project implements a multi-agent system designed to generate, test, improve, and refine **process documentation**. It allows users to create documentation based on existing files, research, and user-defined processes. The system utilizes **virtual testers** to simulate following the documentation, provide feedback, and continuously improve the documentation until it is accurate and clear.

## Key Agents

The system uses the following agents to manage the documentation process:

1. **Research Agent**: Uses internet search tools to gather relevant information on the process and become the Subject Matter Expert (SME).
2. **Requirements Agent**: Identifies and gathers business requirements, compliance needs, and constraints to ensure the documentation adheres to all necessary guidelines.
3. **Documentation Agent**: Creates the process documentation based on inputs from research, requirements, and existing documentation or reference files. This agent also revises the documentation based on feedback.
4. **Reviewer Agent**: Reviews the generated documentation for completeness, clarity, and accuracy, ensuring it's suitable for the target audience before virtual testing.
5. **Virtual Tester Agent**: Simulates following the process documentation in a virtual environment, based on the knowledge level of the target audience, and provides detailed feedback on the success and clarity of each step.
6. **Overall Documentation Manager**: Oversees the entire process, evaluates feedback from the Virtual Tester Agent, and determines if the documentation is realistic, clear, and complete. If necessary, the manager agent sends the documentation back for improvement.

## Key Features

1. **Input Handling**:
   - Users specify the process to document and provide relevant files (PDF, DOCX, MD, TXT, images) to serve as reference material.
   - The system lists available files in a directory and allows the user to select which files to include as references for generating the documentation.
   
2. **Process Documentation Generation**:
   - The system generates process documentation based on reference files, online research, and business requirements.
   - Users can rerun the process to improve existing documentation or reference previous documentation to generate new similar documents.

3. **Testing & Iteration**:
   - The Virtual Tester Agent simulates following the documentation, provides feedback, and suggests improvements based on the audience level and environmental conditions.
   - The system reruns the process iteratively, refining the documentation based on feedback from the Virtual Tester and Reviewer agents until the documentation is accurate and complete.

4. **Feedback Loop**:
   - The Overall Documentation Manager evaluates feedback and determines if further revisions are necessary, creating an ongoing feedback loop to ensure the documentation is continuously improved.

5. **Process History**:
   - The system tracks all previously generated process documentation, allowing users to either rerun the process for improvements or reference existing documentation to generate new similar processes.

6. **Interactive CLI**:
   - An interactive CLI with auto-completion allows users to easily create tasks or rerun previously documented processes. It helps guide users through the process of creating new documentation or selecting past processes.

## Installation

### 1. Clone the repository:

```bash
git clone <repository-url>
cd processdoc_crew
```

### 2. Set up the environment:

It is recommended to use a **virtual environment** or **Conda** environment for isolated package management.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up API keys for online research:

Create a `.env` file in the root directory with the following content to store your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
CLAUDE_API_KEY=your_claude_api_key
GEMINI_API_KEY=your_gemini_api_key
```

These API keys are used by agents for performing online research and generating content using LLMs.

## How to Use

### 1. Run the program:

```bash
python processdoc_crew.py
```

### 2. Interactive CLI:

The system provides an interactive CLI for users to create new tasks or rerun previous processes. Auto-completion is available for selecting past processes.

- **Commands**:
  - `new`: Create a new process documentation task.
  - `rerun`: Rerun a previously generated process.
  - `exit`: Quit the CLI.

```bash
Enter a command (type 'exit' to quit): new
```

### 3. Process Documentation Generation:

- The system will list previously documented processes, allowing the user to rerun or reference existing documentation.
- Users can specify a directory containing relevant files (PDF, DOCX, TXT, MD, images), and the system will display available files for selection.
- Once selected, the system will parse the files and include their content as references in the process documentation.

### 4. Output:

- The final documentation is saved to a specified file, and feedback from the Virtual Tester Agent is included in the history for future references or improvements.

## Project Structure

```
processdoc_crew/
├── agents/
│   ├── documentation_agent.py        # Generates process documentation
│   ├── overall_manager_agent.py      # Oversees feedback and documentation improvements
│   ├── requirements_agent.py         # Gathers business requirements and constraints
│   ├── research_agent.py             # Performs online research
│   ├── reviewer_agent.py             # Reviews the documentation for accuracy and clarity
│   └── virtual_tester_agent.py       # Simulates following the process and provides feedback
├── tasks/
│   └── create_tasks.py               # Dynamically creates tasks for agents
├── utils/
│   ├── file_utils.py                 # File parsing utilities (PDF, DOCX, MD, TXT, images)
│   └── history_utils.py              # Manages process history (reruns and references)
├── processdoc_crew.py                # Main entry point to run the program
├── requirements.txt                  # Dependencies for the project
├── process_history.json              # Stores history of previously generated documentation
└── README.md                         # Documentation
```

## Future Enhancements

- **Machine Learning-Based Feedback Analysis**: Use machine learning models to analyze feedback from agents and automatically refine the documentation based on feedback patterns.
- **Multi-Language Support**: Expand the system to generate process documentation in multiple languages.
- **Enhanced RAG (Retrieval-Augmented Generation) Support**: Integrate an advanced knowledge base to improve RAG by referencing prior documentation and requirements more effectively.

Created by Raul Pineda
Apache License 2.0
