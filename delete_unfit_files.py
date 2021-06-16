import os

def delete(ref_dir,processed_dir):
	'''
	This function will delete all files in the processed folder
	that have different number components from those from the reference folder,
	to ensure every file in each folder is in a pair with a file in the another folder.
	Param:
	- ref_dir: Directory of the reference folder.
	- processed_dir: Directory of the folder you want to process.
	Return: This function return nothing
	'''

	ref_files = os.listdir(ref_dir)
	for i in range(len(ref_files)):
		ref_files[i] = os.path.splitext(ref_files[i])[0]
	print(ref_files)
	for file in os.listdir(processed_dir):
		file, ext = os.path.splitext(file)
		if file not in ref_files:
			try:
				os.remove('{}/{}'.format(processed_dir, file + ext))
				print('Done')
			except:
				continue

if __name__ == '__main__':

	ref_folder = input("Enter reference folder name here: ")
	processed_folder = input("Enter output folder name here: ")

	delete(ref_folder,processed_folder)
