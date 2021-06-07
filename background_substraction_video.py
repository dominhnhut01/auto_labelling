import cv2
import numpy as np
import os

#Global variables
areaThreshold = 100
h_resize = 1480
w_resize = 2048
img_folder ="dataset/sub_fox_vid/vid1"
img_dir_list = os.listdir(img_folder)
for file in img_dir_list:
    if "background" in file:
        background_img = file
        break
#10 first frames will be the background
for i in range(10):
    img_dir_list.insert(0, background_img)

for i in range(len(img_dir_list)):
    img_dir_list[i] = img_folder + '/' + img_dir_list[i]

label_dir = "dataset/sub_fox_vid/vid1_mask"
annotation_dir = "dataset/sub_fox_vid/vid1_annotation"

def crop(img, new_h = 1480, new_w = 2048):
    """
    Crop the image about the center to eliminate the heading part of the photos

    Args:
    img: cv2 image object
    new_h, new_w: new height and weight

    Returns:
    cropped: cropped image
    """

    h = img.shape[0]
    w = img.shape[1]
    center = (h/2, w/2)
    new_A = (int(center[0] - new_h/2), int(center[1] - new_w/2))
    new_C = (int(center[0] + new_h/2), int(center[1] + new_w/2))

    cropped = img[new_A[0]:new_C[0], new_A[1]:new_C[1]]

    return cropped

def create_video():
    """
    Combine the available images (with the same background) to use in the background substration algorithm

    Returns:
    vid_dir: the path to the exported video
    """
    height = cv2.imread(img_dir_list[0]).shape[0]
    width = cv2.imread(img_dir_list[0]).shape[1]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vid_dir = "out_vid.avi"
    new_size = (1480, 2048)
    vid = cv2.VideoWriter(vid_dir, fourcc, 20.0, (new_size[1], new_size[0]))
    for img_dir in img_dir_list:
        frame = cv2.imread(img_dir)
        frame = crop(frame, new_size[0], new_size[1])
        vid.write(frame)
    return vid_dir
def drawBoundingBox(mask, img, areaThreshold = 100):
    """
    Draw the bounding box around the object using its binary mask.

    Args:
    mask: binary mask of the object
    img: the original (cropped) image that we will draw the bounding box on
    areaThreshold: every contours have the area smaller this value will be eliminated (to eliminate noise)

    Returns:

    img: the original image with the bounding box drawn on
    (min_x, max_x, min_y, max_y): coordinates of the vertex of the bounding box
    """

    img = np.copy(img)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    min_x = 500000
    min_y = 500000
    max_x = 0
    max_y = 0
    for cnt in contours:
        if cv2.contourArea(cnt) < areaThreshold:
            continue
        x,y,w,h = cv2.boundingRect(cnt)
        x2 = x + w
        y2 = y + h
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x2 > max_x:
            max_x = x2
        if y2 > max_y:
            max_y = y2
    #If no contour, return blank
    if max_x == 500000 and max_y == 500000 and min_x ==0 and min_y == 0:
        return img, (0,0,0,0)

    img = cv2.rectangle(img,(min_x,min_y),(max_x,max_y),(0,255,0),2)

    return img, (min_x, max_x, min_y, max_y)

def save_result(img, orig_img_name, label_dir):
    """
    Save the resulted images with the bounding box for later investigation
    """

    cv2.imwrite(label_dir + "/" + orig_img_name, img)

def writeLabel(coordinates, label_dir, filename):

    x1,x2,y1,y2 = coordinates
    filename = filename[:-4]
    File = open(label_dir  + "/" +  filename + ".txt", "w")
    File.write("{} {} {} {}".format(x1,x2,y1,y2))
    File.close()

def substract_background(vid_dir):
    """
    Substracting the background and draw the bounding box around the desired animal

    Args:
    vid_dir: the video directory (the return of the function create_video)

    Return:
    None
    """

    cap = cv2.VideoCapture(vid_dir)
    if cap.isOpened() == False:
        print("Unable to open the video")
        exit(0)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    num = 0
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        fgMask = fgbg.apply(frame)

        #Blur the binary mask to reduce noise
        fgMask = cv2.medianBlur(fgMask,  ksize = 21)

        #Draw bounding box
        label, (x1,x2,y1,y2) = drawBoundingBox(fgMask, frame, areaThreshold = areaThreshold)

        filename = os.path.basename(img_dir_list[num])
        save_result(label, filename, label_dir)
        writeLabel((x1,x2,y1,y2), annotation_dir, filename)
        num+=1

    cap.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    substract_background(create_video())
