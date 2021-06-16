import os
from utils import *
def main(working_dir, h_resize, w_resize,  kernelSize_medianBlur, kernelSize_dilation, areaThreshold):
    for img_folder in os.listdir(working_dir):
        if "." in img_folder or len(os.listdir(working_dir + '/' +img_folder)) == 0:
            continue
        if "_annotation" not in img_folder and "_boundingbox" not in img_folder:
            cv2.namedWindow("Visualizing", cv2.WINDOW_FULLSCREEN)
            cv2.namedWindow("Adjusting params")


            folder_idx = os.path.basename(img_folder[3:])
            img_folder = "{}/{}".format(working_dir, img_folder)
            label_dir = "{}/vid{}_boundingbox".format(working_dir, folder_idx)
            annotation_dir = "{}/vid{}_annotation".format(working_dir, folder_idx)
            binary_mask_dir = "{}/vid{}_binary_mask".format(working_dir, folder_idx)

            img_dir_list = generate_dir_list(img_folder)
            print("Folder: {}".format(folder_idx))
            dir_info = (create_video(img_dir_list, h_resize, w_resize), img_dir_list, label_dir, annotation_dir, binary_mask_dir)
            substract_background(dir_info, kernelSize_medianBlur, kernelSize_dilation, areaThreshold)

if __name__ == '__main__':
    working_dir = "dataset/sub_fox_vid"
    #Global variables
    areaThreshold = 2300
    kernelSize_medianBlur = 21
    kernelSize_dilation = 25
    h_resize = 1480
    w_resize = 2048

    main(working_dir, h_resize, w_resize, kernelSize_medianBlur, kernelSize_dilation, areaThreshold)
