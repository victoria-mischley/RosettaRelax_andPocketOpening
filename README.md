# RosettaRelax_andPocketOpening

#RosettaRelax
make folder: "Exemplar_Screen_01_17"
1. Use move_files_for_relax.py. To run you must direct the script to the "Input_PDB" folder locaton
   --- python move_files_for_relax.py /expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_17/Input_PDBs

This script will move files from a home directory "Input_PDB" and copy them into a new directory "Relax" and will name the folders in "Relax" based on file name. After creating the folers and copying the files, the script will make a command list based on the folders in "Relax".

You might have to copy the command_list.txt into the Relax Folder

change into the Relax folder: cd Relax

After running move_files_for_relax.py, use gen_submit_scripts.py from Relax folder. Change the path to the path of the command list and the number of commands per script. Generally, For relaxation you want only one command per script.

Submit scripts need to be moved and submitted from each folder. 

#
