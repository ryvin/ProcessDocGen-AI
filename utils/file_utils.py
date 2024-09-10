import logging
import os
import json
from datetime import datetime
from pytesseract import image_to_string

# Create logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# A method to handle file parsing
def parse_file(file_path):
    """Parse a file and return its content."""
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            return extract_text_from_docx(file_path)
        elif file_extension in [".txt", ".md"]:
            return extract_text_from_txt_or_md(file_path)
        elif file_extension in [".jpg", ".jpeg", ".png"]:
            return extract_text_from_image(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
    except Exception as e:
        logger.exception(f"Error parsing file {file_path}: {str(e)}")
        return None

def extract_text_from_pdf(file_path):
    try:
        # Add PDF extraction logic here
        return "PDF content"
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_from_docx(file_path):
    try:
        # Add DOCX extraction logic here
        return "DOCX content"
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        return None

def extract_text_from_txt_or_md(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {str(e)}")
        return None

def extract_text_from_image(file_path):
    try:
        return image_to_string(file_path)
    except Exception as e:
        logger.error(f"Error extracting text from image {file_path}: {str(e)}")
        return None


# Create logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# A method to handle file parsing
def parse_file(file_path):
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            return extract_text_from_docx(file_path)
        elif file_extension in [".txt", ".md"]:
            return extract_text_from_txt_or_md(file_path)
        elif file_extension in [".jpg", ".jpeg", ".png"]:
            return extract_text_from_image(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return None
    except Exception as e:
        logger.exception(f"Error parsing file {file_path}: {str(e)}")
        return None

def extract_text_from_pdf(file_path):
    try:
        return "PDF content"  # Implement real extraction logic
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_from_docx(file_path):
    try:
        return "DOCX content"  # Implement real extraction logic
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        return None

def extract_text_from_txt_or_md(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {str(e)}")
        return None

def extract_text_from_image(file_path):
    try:
        return image_to_string(file_path)
    except Exception as e:
        logger.error(f"Error extracting text from image {file_path}: {str(e)}")
        return None

def handle_uploaded_file(file, save_dir):
    """Handles an uploaded file and saves it to the specified directory."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.read())
    
    return file_path

def list_files_in_directory(directory):
    """Lists files in a directory."""
    if os.path.exists(directory):
        return os.listdir(directory)
    else:
        return []