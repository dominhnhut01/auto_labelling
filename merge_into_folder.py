import os
import shutil
from utils import crop
import cv2

parent_dir = "dataset"
dest_dir = (parent_dir + "/" + "result/orig_img", parent_dir + "/" + "result/bounding_box", parent_dir + "/" + "result/annotation")
try:
    os.mkdir(parent_dir + "/" + "result")
except:
    pass
try:
    os.mkdir(parent_dir + "/" + "result/bounding_box")
except:
    pass
try:
    os.mkdir(parent_dir + "/" + "result/orig_img")
except:
    pass
try:
    os.mkdir(parent_dir + "/" + "result/annotation")
except:
    pass

folder_name_list = []
source_dir = parent_dir + "/" + "process"
for folder in os.listdir(source_dir):
    if "." in folder or len(os.listdir(source_dir)) == 0:
        continue
    if "_" not in folder:
        folder_name_list.append(folder)

for folder in folder_name_list:
    img_folder = "{}/{}".format(source_dir, folder)
    boundingbox_dir = "{}/{}_bounding_box".format(source_dir, folder)
    annotation_dir = "{}/{}_annotation".format(source_dir, folder)
    for file in os.listdir(img_folder):
        img = cv2.imread(img_folder + "/" + file)
        img = crop(img)
        cv2.imwrite(dest_dir[0] + "/" + file, img)
    for file in os.listdir(boundingbox_dir):
        shutil.move(boundingbox_dir + "/" + file, dest_dir[1] + "/" + file)
    for file in os.listdir(annotation_dir):
        shutil.move(annotation_dir + "/" + file, dest_dir[2] + "/" + file)
