import os  # Import os module to work with files and directories
import shutil  # Import shutil to move files
import tkinter as tk
from tkinter import filedialog

# Define file categories with their extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Music": [".mp3", ".wav"],
}

def get_file_category(filename):
    """Identify the category of a file based on its extension."""
    _, extension = os.path.splitext(filename)  # Get file extension
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category  # Return the matched category
    return "Others"  # Default category if no match found

def create_category_folders(directory):
    """Create category folders inside the given directory if they don’t exist."""
    for category in FILE_CATEGORIES.keys():
        folder_path = os.path.join(directory, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder

    # Create "Others" folder for unrecognized file types
    others_folder = os.path.join(directory, "Others")
    if not os.path.exists(others_folder):
        os.makedirs(others_folder)

def move_files(directory):
    """Move files into their respective category folders."""
    for filename in os.listdir(directory):  # List all files in the directory
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue  

        # Get category and move the file
        category = get_file_category(filename)
        destination_folder = os.path.join(directory, category)
        shutil.move(file_path, destination_folder)  # Move file

if __name__ == "__main__":
    # Use tkinter to open a folder selection dialog
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    if folder_path:  # Proceed only if a folder is selected
        print("Selected Folder:", folder_path)
        create_category_folders(folder_path)
        move_files(folder_path)
        print("Files have been organized successfully!")
    else:
        print("No folder selected. Please try again.")
