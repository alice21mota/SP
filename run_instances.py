import os
import subprocess

# Set the DYLD_LIBRARY_PATH environment variable
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/Cellar/highs/1.7.2/lib:' + os.environ.get('DYLD_LIBRARY_PATH', '')

# Define the paths to the tsp-instances folder and the output folder
tsp_folder_path = 'tsp-instances'
output_folder_path = 'output'

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Loop through each file in the tsp-instances folder
for filename in os.listdir(tsp_folder_path):
    # Only process files that start with 't20'
    if filename.startswith('t20'):
        # Construct the command to run test.py with the input file
        input_file = os.path.join(tsp_folder_path, filename)
        output_file = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.txt")
        command = ['python', 'test.py', input_file, output_file]
        
        # Execute the command with the current environment variables
        subprocess.run(command, env=os.environ)

print("All t20 input files have been processed.")