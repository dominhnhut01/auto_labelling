import os

def delete_annotated_files(ref_dir,processed_dir):
	'''
	This function will delete all files in the processed folder
	that have different number components from those from the reference folder and delete the rest
	to ensure only files not having annotation yet is being kept for manual annotation
	Param:
	- ref_dir: Directory of the reference folder.
	- processed_dir: Directory of the folder you want to process.
	Return: This function return nothing
	'''

	ref_name_list = os.listdir(ref_dir)
	for i in range(len(ref_name_list)):
		ref_name_list[i] = os.path.splitext(ref_name_list[i])[0]

	for file in os.listdir(processed_dir):
		file, ext = os.path.splitext(file)
		if file in ref_name_list:
			try:
				os.remove('{}/{}'.format(processed_dir, file + ext))
				print('Deleted {}'.format(file))
			except:
				continue
		# #read input file
		# fin = open('{}/{}'.format(processed_dir, file), "rt")
		# #read file contents to string
		# data = fin.read()
		# #replace all occurrences of the required string
		# data = data.replace('0 ', '1 ')
		# #close the input file
		# fin.close()
		# #open the input file in write mode
		# fin = open('{}/{}'.format(processed_dir, file), "wt")
		# #overrite the input file with the resulting data
		# fin.write(data)
		# #close the file
		# fin.close()

def delete(ref_dir,processed_dir):
	'''
	This function will keep all files in the processed folder
	that have different number components from those from the reference folder
	to ensure every file in each folder is in a pair with a file in the another folder.
	Param:
	- ref_dir: Directory of the reference folder.
	- processed_dir: Directory of the folder you want to process.
	Return: This function return nothing
	'''

	ref_name_list = os.listdir(ref_dir)
	for i in range(len(ref_name_list)):
		ref_name_list[i] = os.path.splitext(ref_name_list[i])[0]

	for file in os.listdir(processed_dir):
		file, ext = os.path.splitext(file)
		if file not in ref_name_list:
			try:
				os.remove('{}/{}'.format(processed_dir, file + ext))
				print('Deleted {}'.format(file))
			except:
				continue
if __name__ == '__main__':

	ref_folder = input("Enter reference folder name here: ")
	processed_folder = input("Enter output folder name here: ")
	option = int(input("Choose 1 or 2: "))

	if option == 1: delete(ref_folder,processed_folder)
	if option == 2: delete_annotated_files(ref_folder, processed_folder)
