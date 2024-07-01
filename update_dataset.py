import shutil
import os

def copy_directory(source, destination):
    try:
        # Check if the source directory exists
        if not os.path.exists(source):
            print(f"Source directory {source} does not exist.")
            return
        
        # Check if the destination directory exists, create it if it doesn't
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        # Copy the directory
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(f"Copied {source} to {destination} successfully.")
    except Exception as e:
        print(f"Error copying directory: {e}")

# Example usage
source_directory = 'Scraping/Election_Results'
destination_directory = 'Dataset'

copy_directory(source_directory, destination_directory)
