# RosettaRelax_andPocketOpening

**#RosettaRelax**
make folder: "Exemplar_Screen_01_17"
1. Use move_files_for_relax.py. To run you must direct the script to the "Input_PDB" folder locaton
   --- python move_files_for_relax.py /expanse/lustre/projects/was136/vmischley/vmischley_04_28/Exemplar_Screen_01_17/Input_PDBs

This script will move files from a home directory "Input_PDB" and copy them into a new directory "Relax" and will name the folders in "Relax" based on file name. After creating the folers and copying the files, the script will make a command list based on the folders in "Relax".

You might have to copy the command_list.txt into the Relax Folder

change into the Relax folder: cd Relax

After running move_files_for_relax.py, use gen_submit_scripts.py from Relax folder. Change the path to the path of the command list and the number of commands per script. Generally, For relaxation you want only one command per script.

Submit scripts need to be moved and submitted from each folder. 

**#Pocket_Opening**
Make a folder with the top exemplars that you want to pocket open. "TopExemplarsForPocketOpening"
1. Use get_residues_for_pocket_opening.py. Change the path within the script
- this script will make a csv file that contains the file name and residues of the exemplar. This is needed to format everything for pocket opening. Check the CSV file, sometimes for single number residues (ie 8). It messes up the formatting. Just edit the CSV file for these files. 
2. Use fromat_pocket_opening.py. Change the path of the working directory within the script.
  - This script will make a folder, Pocket_Opening, and it will go through each of the folders in the Relax folder to find the lowest energy conformation for each AF model. It will then copy this lowest energy conformation into a new folder wihtin the Pocket_Opening folder. Then it will create the constraints file and the pocket.wts.patch file with the correct formatting for each model. Finally the make_command_list module will make the command list for all of the files.
3. Change into the Pocket_Opening directory
4. Copy the command_list into Pocket_Opening directory
5. copy the pocket_opening_batch_submit_gen.py into Pocket_Opening directory
***Make sure memory is set to at least 10GB. Otherwise not all jobs will run. 
6. Submit pocket_opening_batch_submit_gen.py. It is important to keep chunk size in groups of 2 (ie 2, 4, 6) as two commands are neccessary to pocket_open each folder. The first command changes into the folder and the second one submits the command from that folder. This allows the output to be placed into the correct folders. 

**###After Pocket Opening**
After pocket opening, regenerate exemplars with the origional file, relaxed file, and three lowest energy conformations of the pocket opened structure. After generating exemplars those exemplars will be used for druggability
All of the nomenclature for pockets remains the same for the whole pipeline, you just need to change the path of the home directory that contains the folders: Relax, Pocket_Opening, and this script will make another folder within the home directory, Exemplars_after_Pocket_Opening
This script will go thorugh the Pocket Opening folder, make new folders within the Exemplars_after_Pocket_Opening folde and then  will open the .score file to find the conformations with the 3 lowest energy conformation to each folder's respective folder within the Exemplars_after_Pocket_Opening folder. It will then copy the origional file and the corresponding Relaxed folder.
Lastly, it wil make a command list to generate exemplars. 
Step 1: run format_exemplar_screen_after_pocket_opening.py, this will output exemplars_after_pocket_opening_command_list.txt. Copy command_list into Exemplars_after_Pocket_Opening folder
Since there are a total of five models per pocket, it is important to keep the chunk size at 6, so it the slurm submit script will change into the appropriate folder, and then run the exemplars for the five models within the same folder. 
2. Run exemplars_after_pocket_opening_batch_submit_gen.py within the Exemplars_after_Pocket_Opening, just change the path to the command list. 


