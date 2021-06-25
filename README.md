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
1/ COPY (NOT MOVE) the images which have the same background and paste them into separate folder in "/dataset/process" directory. This can only be used on images which have separate background images and have no snowy or rainy weather! If they don't, we have to label them manually!

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

7/ Run the script "delete_unfit_files.py". Enter the reference folder and target folder into the command line as requested and choose option 1. This script is used to delete all files in the target folder which don't have the same filename with any files in the reference folder. I'll use this to delete the images and annotation files which haves their bounding box deleted in step 6

8/ Run the script "delete_unfit_files.py". Enter the reference folder (should be the `dataset\result\boundingbox`) and target folder (should be the folder where you place all your original images) into the command line as requested and choose option 2. This script will help delete all the already annotated images and keep the unannotated images

## Video demo:
  
<!DOCTYPE html>
<html>
<body>
  
  <iframe src="<iframe src="https://drive.google.com/file/d/16nRJH1tiV8aQ5crkMXnRbXkVg9JoApBY/preview" width="1280" height="720" allow="autoplay"></iframe>" ></iframe>
  
  <!--aloow full screen add tag -->
  
<iframe allowfullscreen="allowfullscreen" src="your_page_url/preview" ></iframe>

</body>
</html>


## Disadvantages:
1/ Unfortunately, I cannot find the way to detect >=2 animals in the images. Therefore, if there are two foxes in the images, we have to label them by ourselves.
2/ Currently, this program can only work for a set of images with very similar lighting conditions (different times in a day (even only 1-2 hours) will cause different lighting conditions). Therefore, even if a large set of images is taken from the same camera (same background), we have to divide them into smaller groups based on the time. I tried using histogram equalization but no luck. It would be great if someone can help me neutralize all the lighting conditions in the input photos. 
  Therefore, please use the background images having the timestamp near those of the images you wish to annotate so we can ensure the lighting condition is the same
3/ Some images (20% - 30%) cannot be annotated properly with my script so we have to delete the error files and annotate them manually
4/ Images having snowy or rainy weather or having no background images cannot be annotated well. So please don't add the in the first place

