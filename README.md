# Auto labelling using Background Substractor

## Table of Contents
1. [Main idea]
2. [Prerequisite]
3. [How to use]
4. [Disadvantages]

## Main idea
The main idea of this script is because our dataset is collected by a static camera, we can use the background frames as a base to detect new object appearing in the frame. Moreover, because each animal in our dataset is already put in a different folder, we can label different classes only by detecting the object in the frames. For example, if we detect an object in folder fox, it must be a fox.

## Prerequisite
- Clone this repository
- Create the virtual environment and activate it
- cd into this repository and run `pip install -r requirement.txt`
## How to use
1/ COPY (NOT MOVE) the images which have the same background and paste them into separate folder in "/dataset/process" directory. This can only be used on images which have separate background images! If they don't, we have to label them manually!
2/ Find an image containing only background and set its name to "background.<extension>"
3/ Run the script "background_substraction_video_multifile.py"
4/ When two windows pop up, there will be trackbar for us to adjust the parameters. List of parameters in order:
- medianblur_kernelSize:
  Kernel size used in median blur - used to eliminate salt-peper noise on the binary mask image. Increase this if you see small, unexpected dots on the binary mask
- dilation_kernelSize:
  Kernel size use in morphological dilation algorithm - used to join broken parts of the mask by increase the blob's size. Increase this if you see the expected mask is broken or too small.
- areaThreshold:
  The extra step to use if median blur cannot eliminate all the noise. Increase this will eliminate the white pixel whose area is smaller than this threshold.
  
If the program runs too slow or have the sign of not responding, please reduce the batch_size which is located on line 53 in generate_dir_list function in the utils.py file

5/ After finishing applying the script on all images, run the merge_into_folder.py to merge all files into one folder inside "/dataset/result" for further manipulation.
6/ Go into folder "/dataset/result/..._boundingbox", delete all files which have wrong bounding box because the script cannot annotate 100% right
7/ Run the script "delete_unfit_files.py". Enter the reference folder and target folder into the command line as requested. This script is used to delete all files in the target folder which don't have the same filename with any files in the reference folder. I'll use this to delete the images and annotation files having their bounding box delete in step 6
  
## Disadvantages:

