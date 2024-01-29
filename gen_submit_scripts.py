import os

# Define the path to the text file containing the list of input file paths
file_list_path = "/expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_17/Relax/relax_command_list.txt"

# Read the list of file paths from the text file
with open(file_list_path, "r") as file_list_file:
    file_paths = file_list_file.read().splitlines()

# Define the submit template with placeholders
submit_template = """#!/bin/bash
#SBATCH --job-name="relax"
#SBATCH --output="{output_filename}"
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=2G
#SBATCH --constraint="lustre"
#SBATCH --export=ALL
#SBATCH --account=was136
#SBATCH -t 48:00:00


# Start of job commands
"""

# Function to split a list into chunks of a specified size
def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

# Divide the list of file paths into chunks of 6
chunks = list(chunk_list(file_paths, 1))

# Create a job file for each chunk
for i, chunk in enumerate(chunks):
    # Define job file name
    job_file_name = f"relax_{i + 1}.sb"

    # Define the output filename based on the job file name
    output_filename = os.path.splitext(job_file_name.split("/")[-1])[0] + f".%j.%N.out"
    # Replace placeholders in the submit template with actual values
    job_file_content = submit_template.format(job_name=job_file_name, output_filename=output_filename) + "\n"

    # Append the command with file paths to the job file content
    for file_path in chunk:
        # Define the output name based on the input file name
        #output_name = os.path.splitext(os.path.basename(file_path))[0] + "__oeomega.oeb"

        # Define the command template with input and output paths
        command_template = f"{file_path}"

        command = command_template
        job_file_content += command + "\n"

    # Write the job file content to a file
    with open(job_file_name, "w") as job_file:
        job_file.write(job_file_content)

    print(f"Created job file: {job_file_name}")

print("Job files created successfully.")

