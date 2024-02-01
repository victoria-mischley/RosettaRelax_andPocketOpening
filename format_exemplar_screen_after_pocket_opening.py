import shutil
import os
from pathlib import Path
import argparse
import pandas as pd

# working_directory = "/expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_17"
working_directory = "/Users/mischlv/Downloads"
relax_folder_home = f"{working_directory}/Relax"
csv_file_location = f"{working_directory}/pocket_opening_residues.csv"
pocket_opening_home = f"{working_directory}/Pocket_Opening"
exemplar_after_PO_home = f"{working_directory}/Exemplars_after_Pocket_Opening"
input_PDB_home = f"{working_directory}/Input_PDBs"
output_command_list= f"{working_directory}/exemplars_after_pocket_opening_command_list.txt"

###takes score list and number from minimum, so 1 is the most minimum, 2 is second most minimum, 3 is third most minimum
def get_file_number(score_list, number):
    sorted_score_list = sorted(score_list)
    print(sorted_score_list)
    score = sorted_score_list[int(number)] 
    print(score)
    file_number = score_list.index(score) +1
    return file_number

def get_file_name(relaxed_file_name_suffix, file_number):
    if file_number < 10:
        pocket_opening_name = f"{relaxed_file_name_suffix}_000{file_number}.pdb"
    if file_number > 9:
        pocket_opening_name = f"{relaxed_file_name_suffix}_00{file_number}.pdb"
    return pocket_opening_name

def get_res_numbers(folder_name):
    folder_name_prefix_A = folder_name.split("_resA")[1]
    resA = folder_name_prefix_A.split("_resB")[0]
    folder_name_prefix_B = folder_name.split("_resB")[1]
    resB = folder_name_prefix_B.split("_Exemplars")[0]
    return resA, resB

def make_folders(pocket_opening_path):
    ###Make new folders with same name as pocket_opening but put into the folder Exemplars_after_Pocket_Opening
    pocket_opening_folders = os.listdir(pocket_opening_home)
    for folder in pocket_opening_path.iterdir():
        if folder.is_dir():
            folder_name = folder.name
            new_folder = Path(f"{exemplar_after_PO_home}/{folder_name}_Exemplars_after_Pocket_Opening")
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            ###Folders are created, now we need to copy over files for which we want to generate exemplars for
            pocket_opening_score_file = f"{pocket_opening_home}/{folder_name}/score.sc"
            if folder_name in pocket_opening_folders:
                print(folder_name)
                score_list = []
                name_suffix_list = []
                ###get file name of origional relaxed file for naming purposes
                for file in folder.iterdir():
                    file_name = file.name
                    if file_name.endswith(".pdb"):
                        name_suffix_list.append(file_name)
                sorted_name_suffix_list = sorted(name_suffix_list)
                relax_file = sorted_name_suffix_list[0]
                relaxed_file_name_suffix = relax_file[:-4]
                input_file_name = relax_file.split("_Relaxed_")[0] + ".pdb"
                #### open score file and get the file numbers of the 3 lowest energy pockets
                with open(pocket_opening_score_file, 'r') as file:
                    for line in file:
                        parts = line.split()
                        if parts[0] == "SCORE:":
                            if parts[1] != "total_score":
                                score = float(parts[1])
                                score_list.append(score)
                min_file_number = get_file_number(score_list, 0)
                print(min_file_number)
                second_min_file_number = get_file_number(score_list, 1)
                third_min_file_number = get_file_number(score_list, 2)
                
                min_file_name = get_file_name(relaxed_file_name_suffix, min_file_number)
                second_min_file_name = get_file_name(relaxed_file_name_suffix, second_min_file_number)
                third_min_file_name = get_file_name(relaxed_file_name_suffix, third_min_file_number)

                ####Now copy all of the files over to Exemplars_after_Pocket_Opening"
                shutil.copy(f"{folder}/{relax_file}", f"{new_folder}/{relax_file}")
                shutil.copy(f"{folder}/{min_file_name}", f"{new_folder}/{min_file_name}")
                shutil.copy(f"{folder}/{second_min_file_name}", f"{new_folder}/{second_min_file_name}")
                shutil.copy(f"{folder}/{third_min_file_name}", f"{new_folder}/{third_min_file_name}")
                shutil.copy(f"{input_PDB_home}/{input_file_name}", f"{new_folder}/{input_file_name}")

###Make commands and then later will split into groups of 5
def make_command_list():
    if os.path.exists(output_command_list):
        os.remove(output_command_list)
    folders = os.listdir(exemplar_after_PO_home)
    for folder in folders:
        if folder != ".DS_Store":
            files = os.listdir(f"{exemplar_after_PO_home}/{folder}")
            folder_path = Path(f"{exemplar_after_PO_home}/{folder}")
            folder_name = folder_path.name
            command1 = f"cd {folder_path}"
            with open(output_command_list, 'a') as output_file:
                output_file.write(command1 + '\n')
            for file in files:
                if file.endswith(".pdb"):
                    file_path = f"{exemplar_after_PO_home}/{folder}/{file}"
                    chainAres, chainBres = get_res_numbers(folder_name)
                    command2 = f"/expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/source/bin/make_exemplar.linuxgccrelease -database  /expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/database -s {file_path} -pocket_num_angles 100 -pocket_psp -pocket_grid_size 10 -pocket_max_spacing 12 -central_relax_pdb_num {chainAres}:A,{chainBres}:B -pocket_filter_by_exemplar -pocket_static_grid -pocket_limit_exemplar_color -pocket_dump_exemplars -min_atoms 1 -max_atoms 65"
                    with open(output_command_list, 'a') as output_file:
                        output_file.write(command2 + '\n')
                    


if __name__ == '__main__':
    if not os.path.exists(exemplar_after_PO_home):
        os.makedirs(exemplar_after_PO_home)
    pocket_opening_path = Path(pocket_opening_home)
    make_folders(pocket_opening_path)
    # make_command_list()
