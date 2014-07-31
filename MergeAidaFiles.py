import glob
import os
from Aux_Functions import *

dataset_names = GetListDataset('dataset_names')
dataset_number = GetListDataset('dataset_number')
powheg_list = ['000001','000002','000003','000004','000005','000006','000007']
powheg_dict = dict(zip(dataset_number, dataset_names))

# Make a list of Aida files available in the current directory
for folder in dataset_names:
	current_dir = folder+"/"
	if os.path.exists(current_dir) != True: continue
    file_name = folder.split('.')[0]
    
	os.chdir(current_dir)
	Aida_Files = glob.glob("*.aida*")
	i = len(Aida_Files)
	print "There were {0} in the directory: {1}".format(i,current_dir)
    
    if file_name in powheg_list:
        dest_Wpm = file_name
        source_Wm = str(int(file_name) + 185695)
        source_Wp = str(int(source_Wm) + 7)
        source_Wm_dir = dataset_names[source_Wm]
        source_Wp_dir = dataset_names[source_Wp]
        cmd = "cp ../{0}/merged_add.save ./merged_add_Wm.aida".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged_avg.save ./merged_avg_Wm.aida".format(source_Wm_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged_add.save ./merged_add_Wp.aida".format(source_Wp_dir)
        os.system(cmd)
        cmd = "cp ../{0}/merged_avg.save ./merged_avg_Wp.aida".format(source_Wp_dir)
        os.system(cmd)
        os.system("python ../aidamerge.py -c -o merged_avg.aida merged_avg_Wm.aida merged_avg_Wp.aida")
        os.system("python ../aidamerge.py -c -o merged_add.aida merged_add_Wm.aida merged_add_Wp.aida")
        # convert to root, rename root and *.aida files
    else:
        if not Aida_Files: continue
    	# Run aidamerge.py over every file in the Aida_Files list.
    	arguments = "%s" % " ".join(map(str, Aida_Files))
    	cmd = "python ../aidamerge.py -o merged_avg.aida "+arguments
    	os.system(cmd)
    	cmd = "python ../aidamerge.py -s -o merged_add.aida "+arguments
    	os.system(cmd)
		
	# Convert merged.aida file to merged.root file and rename to dataset
	# run number (found from the folder name).
	os.system("aida2root merged_avg.aida")
	os.system("aida2root merged_add.aida")
	#if "Powheg" in file_name: file_name = folder.replace('.','_')
	cmd = "mv merged_avg.root "+file_name+".root"
	os.system(cmd)
	cmd = "mv merged_add.root "+file_name+"_add.root"
	os.system(cmd)
		
	# Remove the merged.aida file in case the script fails.
	# This keeps you from having to delete them by hand before re-running script.
	os.system("mv merged_add.aida merged_add.save")
	os.system("mv merged_avg.aida merged_avg.save")
	
	# Prepare for next folder
	os.chdir("..")
	Aida_Files = []
