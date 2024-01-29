import shutil
import os
from pathlib import Path
import argparse

def args():
    parser = argparse.ArgumentParser()
    # Add command line arguments
    parser.add_argument('folder_path', type=str, help='path to location of AF folder output')
    # Parse the command line arguments
    args = parser.parse_args()

    return args

def make_folders_and_copy_files(folder_path_str, working_directory):
    files = os.listdir(folder_path_str)
    list_new_file_paths = []
    Relax_folder_path = f"{working_directory}/Relax"
    if not os.path.exists(Relax_folder_path):
        os.makedirs(Relax_folder_path)
    for file in files:
        file_name = file
        new_folder_name = file_name.split("_relaxed_")[0]
        new_folder_path = f"{working_directory}/Relax/{new_folder_name}"
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        src = f"{folder_path}/{file}"
        dst = f"{new_folder_path}/{file}"
        list_new_file_paths.append(dst)
        shutil.copy(src, dst)
    return list_new_file_paths

def make_command_list(list_new_file_paths, working_directory):

    for file in list_new_file_paths:
        output_file_path = f"{working_directory}/Relax/relax_command_list.txt"
        command = f"/expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/source/bin/pocket_relax.linuxgccrelease -database  /expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/database -in:file:s {file}  -in:file:fullatom -constrain_relax_to_start_coords -relax:ramp_constraints false -nstruct 20 -out:suffix _Relaxed -out:pdb"
        with open(output_file_path, 'a') as output_file:
            output_file.write(command + '\n')







if __name__ == '__main__':
    args = args()
    folder_path = Path(args.folder_path)
    folder_path_str = args.folder_path
    working_directory = folder_path.parent
    list_new_file_paths =make_folders_and_copy_files(folder_path_str, working_directory)
    make_command_list(list_new_file_paths)


