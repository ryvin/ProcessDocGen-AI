PROCESS_HISTORY_PATH = 'process_history.json'

def load_process_history():
    try:
        if os.path.exists(PROCESS_HISTORY_PATH):
            with open(PROCESS_HISTORY_PATH, 'r') as file:
                return json.load(file)
        return []
    except Exception as e:
        logger.error(f"Error loading process history: {str(e)}")
        return []

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
