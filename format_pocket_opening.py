import shutil
import os
from pathlib import Path
import argparse
import pandas as pd

working_directory = "/expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_17"
# working_directory = "/Users/mischlv/Downloads"
relax_folder_home = f"{working_directory}/Relax"
csv_file_location = f"{working_directory}/pocket_opening_residues_missed.csv"
pocket_opening_home = f"{working_directory}/Pocket_Opening_missed"
output_command_list= f"{working_directory}/pocket_opening_command_list_missed.txt"

def move_files_make_files():
    df = pd.read_csv(csv_file_location)
    relax_folder_folder = os.listdir(relax_folder_home)

    for ind in df.index:
        full_name = df['file_name'][ind]
        residue_A = df['residue_A'][ind]
        residue_B = df['residue_B'][ind]
        input_name = full_name.split(".pdb.")[0] + ".pdb"
        folder_name = input_name.split("_relaxed_")[0]
        relax_folder_path = f"{relax_folder_home}/{folder_name}"
        score_file_path = f"{relax_folder_path}/score_Relaxed.sc"
        score_list = []
        if folder_name in relax_folder_folder:
            with open(score_file_path, 'r') as file:
                for line in file:
                    parts = line.split()
                    if parts[0] == "SCORE:":
                        if parts[1] != "total_score":
                            score = float(parts[1])
                            score_list.append(score)
            min_number = min(score_list)
            min_index = score_list.index(min_number)
            file_number = min_index + 1
            file_name_suffix = input_name[:-4]
            if file_number < 10:
                relax_file_name = f"{file_name_suffix}_Relaxed_000{file_number}.pdb"
            if file_number > 9:
                relax_file_name = f"{file_name_suffix}_Relaxed_00{file_number}.pdb"
            Pocket_opening_folder =f"{pocket_opening_home}/{folder_name}_resA{residue_A}_resB{residue_B}"
            if not os.path.exists(Pocket_opening_folder):
                os.makedirs(Pocket_opening_folder)
            ####Copy the lowest energy relaxed structure from Relax folder to pocket opening folder###
            src = f"{relax_folder_path}/{relax_file_name}"
            dst = f"{Pocket_opening_folder}/{relax_file_name}"
            shutil.copy(src, dst)
            ###Make the constraints file
            constraints_file = f"{Pocket_opening_folder}/constraints"
            constraints_input = f"Pocket 0.25 {residue_A}:A,{residue_B}:B"
            with open(constraints_file, "w") as file:
                file.write(constraints_input + '\n')
            pocket_weight_file = f"{Pocket_opening_folder}/pocket.wts.patch"
            with open(pocket_weight_file, "w") as x:
                x.write("pocket_constraint = 1.0" + '\n')

def make_command_list():
    folders = os.listdir(pocket_opening_home)
    for folder in folders:
        if folder != ".DS_Store":
            files = os.listdir(f"{pocket_opening_home}/{folder}")
            print(folder)
            for file in files:
                print(file)
                if file.endswith(".pdb"):
                    file_path = f"{pocket_opening_home}/{folder}/{file}"
                    folder_path = f"{pocket_opening_home}/{folder}"
                    print(folder_path)
                    command1 = f"cd {folder_path}"
                    command2 = f"/expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/source/bin/pocket_relax.linuxgccrelease -database  /expanse/lustre/projects/use300/jpg/rosetta.source.release-362/main/database -in:file:s {file_path} -pocket_num_angles 2 -score:patch pocket.wts.patch -cst_fa_file constraints -nstruct 50 -pocket_zero_derivatives -pocket_filter_by_exemplar"
                    with open(output_command_list, 'a') as output_file:
                        output_file.write(command1 + '\n')
                        output_file.write(command2 + '\n')


if __name__ == '__main__':
    if not os.path.exists(pocket_opening_home):
        os.makedirs(pocket_opening_home)
    move_files_make_files()
    make_command_list()
                    
