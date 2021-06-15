import os
import shutil
from utils import crop
import cv2

parent_dir = "dataset"
dest_dir = (parent_dir + "/" + "Result_Dataset/orig_img", parent_dir + "/" + "Result_Dataset/boundingbox", parent_dir + "/" + "Result_Dataset/annotation")
try:
    os.mkdir(parent_dir + "/" + "Result_Dataset")
    os.mkdir(parent_dir + "/" + "Result_Dataset/boundingbox")
    os.mkdir(parent_dir + "/" + "Result_Dataset/orig_img")
    os.mkdir(parent_dir + "/" + "Result_Dataset/annotation")
except:
    print("Folder already exists!" )

folder_idx_list = []
source_dir = parent_dir + "/" + "sub_fox_vid"
for folder in os.listdir(source_dir):
    if "." in folder or len(os.listdir(source_dir)) == 0:
        continue
    if "_" not in folder:
        folder_idx = os.path.basename(folder[3:])
        folder_idx_list.append(folder_idx)

for folder_idx in folder_idx_list:
    img_folder = "{}/vid{}".format(source_dir, folder_idx)
    boundingbox_dir = "{}/vid{}_boundingbox".format(source_dir, folder_idx)
    annotation_dir = "{}/vid{}_annotation".format(source_dir, folder_idx)
    for file in os.listdir(img_folder):
        img = cv2.imread(img_folder + "/" + file)
        img = crop(img)
        cv2.imwrite(dest_dir[0] + "/" + file, img)
    for file in os.listdir(boundingbox_dir):
        shutil.move(boundingbox_dir + "/" + file, dest_dir[1] + "/" + file)
    for file in os.listdir(annotation_dir):
        shutil.move(annotation_dir + "/" + file, dest_dir[2] + "/" + file)
