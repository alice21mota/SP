import os
import subprocess

# Set the DYLD_LIBRARY_PATH environment variable
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/Cellar/highs/1.7.2/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')

# Define the paths to the tsp-instances folder and the output folder
tsp_folder_path = 'tsp-instances'
output_folder_path = 'output'

def remove_elapsed_time_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if lines and lines[-1].startswith("Elapsed time:"):
        lines = lines[:-1]
    
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Loop through each file in the tsp-instances folder
for filename in os.listdir(tsp_folder_path):
    # Only process files that start with 't20'
    if filename.startswith('t20'):
        # Construct the input and output file paths
        input_file = os.path.join(tsp_folder_path, filename)
        output_file = os.path.join(output_folder_path, filename)
        
        # Remove the last line if it starts with "Elapsed time:"
        remove_elapsed_time_line(output_file)
        
        # Construct the command to run checker.py with the input and output files
        command = ['python', 'checker.py', input_file, output_file]
        
        # Execute the command with the current environment variables
        subprocess.run(command, env=os.environ)

print("All t20 input files have been processed.")