import os
import pandas as pd

input_folder = "/expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_29/TopExemplarsForPocketOpening"

files = os.listdir(input_folder)
file_name_list = []
resA_list = []
resB_list = []
for file in files:
    name = file.split(".pdb")[0]
    res_numbers = file.split(".")[2]
    file_name = f"{name}.pdb"
    # print(res_numbers)
    residue_A = res_numbers.split(":A")[0]
    residue_B_prefix = res_numbers.split("-")[1]
    residue_B = residue_B_prefix.split(":")[0]
    file_name_list.append(file)
    resA_list.append(residue_A)
    resB_list.append(residue_B)
print(len(files))

df = pd.DataFrame({'file_name': file_name_list, 'residue_A': resA_list, 'residue_B': resB_list})
df.to_csv(f"{input_folder}/pocket_opening_residues_updated.csv")
   
