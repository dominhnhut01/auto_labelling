import os
from utils import *
def main(working_dir, h_resize, w_resize,  kernelSize_medianBlur, kernelSize_dilation, areaThreshold):
    for img_folder in os.listdir(working_dir):
        if "." in img_folder or len(os.listdir(working_dir + '/' +img_folder)) == 0:
            continue
        if "_annotation" not in img_folder and "_boundingbox" not in img_folder:
            basename = os.path.basename(img_folder)
            img_folder = "{}/{}".format(working_dir, img_folder)
            bb_dir = "{}/{}_bounding_box".format(working_dir, basename)
            annotation_dir = "{}/{}_annotation".format(working_dir, basename)

            try:os.mkdir(bb_dir)
            except:pass
            try:os.mkdir(annotation_dir)
            except:pass
            img_dir_list_chunks = generate_dir_list(img_folder)
            print("Folder: {}".format(basename))
            dir_info = (create_video(img_dir_list_chunks, h_resize, w_resize), img_dir_list_chunks, bb_dir, annotation_dir)
            print("Reading the file...")
            substract_background(dir_info, kernelSize_medianBlur, kernelSize_dilation, areaThreshold)

if __name__ == '__main__':
    working_dir = "dataset/process"
    #Global variables
    areaThreshold = 2300
    kernelSize_medianBlur = 21
    kernelSize_dilation = 25
    h_resize = 1480
    w_resize = 2048

    main(working_dir, h_resize, w_resize, kernelSize_medianBlur, kernelSize_dilation, areaThreshold)
