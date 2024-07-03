import json
import os


PROJECT_DATA = {
    "name": "Starter Program",
    "description": "Just another program...",
    "files": ["starter_program.py"]
}

# Current program loaded on the robot
LOADED_PROGRAM = "Starter Program"
# Used to remember which program the user may want to override
PROGRAM_TO_OVERRIDE = ""
    
def read_project_file(filename):
    root_dir = "Programs"  # Base directory to search

    global PROGRAM_TO_OVERRIDE, PROJECT_DATA, LOADED_PROGRAM
    # Walk through all directories and files in root_dir
    for dirpath, dirnames, files in os.walk(root_dir):
        if filename in files:
            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, 'r') as file:
                    print("File is being read")
                    PROJECT_DATA = json.load(file)
                    # program = [Keyframe.from_dict(kf) for kf in data['program']]
                    print(PROJECT_DATA)
                
                return f"Program was found and loaded from {full_path}. :)"
            except json.JSONDecodeError:
                return "Error decoding the JSON file."

    # If the file is not found in any subdirectory, load a default Keyframe
    PROJECT_DATA = {
        "name": "Starter Program",
        "description": "Just another program...",
        "files": ["starter_program.py"]
    }

    return "Program was not found. :("
    
def save_project_file(filename, override=False):
    """
    Searches for a file in the Programs folder. If found and override is False, returns a warning message.
    Otherwise, writes data to the file.
    
    Args:
    filename (str): The name of the file to write to.
    override (bool): If True, overrides the file if it exists. Default is False.
    
    Returns:
    None: Returns a message if the file already exists and override is False, otherwise writes to the file.
    """
    global PROGRAM_TO_OVERRIDE, PROJECT_DATA, LOADED_PROGRAM
    root_dir = "Programs"  # Base directory to search

    # Attempt to find the file in the directory structure
    file_path = None
    for dirpath, dirnames, files in os.walk(root_dir):
        if filename in files:
            file_path = os.path.join(dirpath, filename)
            break

    if file_path and not override:
        PROGRAM_TO_OVERRIDE = filename
        return "File already exists. Do you want to overwrite it?"

    # If file was not found or override is True, write to the specified path
    if not file_path:
        file_path = os.path.join("Programs/Others", filename)  # Default path if not found
        try:  
            os.mkdir(file_path)  
        except OSError as error:  
            print(error)   

    # # Write to python files
    # for file in LOADED_PROGRAM.files:
    #     try:
    #         with open(os.path.join(file_path, f"{file}.py"), 'w') as file:
    #             file.write(data)
    #     except IOError as e:
    #         print(f"An error occurred: {e}")

    # Write data to the file
    try:
            with open(os.path.join(file_path, f"{file}.py"), 'w') as file:
                file.write(data)
    except IOError as e:
            print(f"An error occurred: {e}")

    LOADED_PROGRAM = filename
    return f"Data written to {file_path}"

