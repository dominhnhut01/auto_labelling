import cv2
import numpy as np
import os
from functools import partial

def create_trackbar(img_cache, mask_cache):
    cv2.createTrackbar("AreaThreshold", "Adjusting params", 100, 20000, partial(visualizeParams, img_cache = img_cache, mask_cache = mask_cache))
    cv2.createTrackbar("medianBlur_kSize", "Adjusting params", 0, 70, partial(visualizeParams, img_cache = img_cache, mask_cache = mask_cache))
    cv2.createTrackbar("dilation_kSize", "Adjusting params", 0, 40, partial(visualizeParams, img_cache = img_cache, mask_cache = mask_cache))

def visualizeParams(x, img_cache ,mask_cache):
    areaThreshold, kernelSize_medianBlur, kernelSize_dilation = getTrackbarValue()
    img_cache_copy = np.copy(img_cache)
    mask_cache_copy = np.copy(mask_cache)
    for idx in range(len(img_cache)):
        img_cache_copy[idx], (x1,x2,y1,y2), mask_cache_copy[idx] = process_img(mask_cache[idx], img_cache[idx], areaThreshold, kernelSize_medianBlur, kernelSize_dilation)
    #stack result
    prevStack = None
    scale = 0.1
    width = int(img_cache[0].shape[1] * scale)
    height = int(img_cache[0].shape[0] * scale)
    dim = (width, height)
    img_num = len(img_cache)

    for idx in range(img_num - 5, img_num):
        temp_img = np.copy(img_cache_copy[idx])
        temp_mask = cv2.cvtColor(np.copy(mask_cache_copy[idx]), cv2.COLOR_GRAY2BGR)
        temp_img = cv2.resize(temp_img, dim, interpolation = cv2.INTER_AREA)
        temp_mask = cv2.resize(temp_mask, dim, interpolation = cv2.INTER_AREA)

        tempHStack = np.hstack((temp_img, temp_mask))
        if idx == img_num - 5:
            vStack = tempHStack
        else:
            vStack = np.vstack((tempHStack, prevStack))
        prevStack = vStack
    cv2.imshow("Visualizing", vStack)

def getTrackbarValue():
    areaThreshold = cv2.getTrackbarPos("AreaThreshold", "Adjusting params")
    kernelSize_medianBlur = cv2.getTrackbarPos("medianBlur_kSize", "Adjusting params") * 2 + 1
    kernelSize_dilation = cv2.getTrackbarPos("dilation_kSize", "Adjusting params") * 2 + 1
    return areaThreshold, kernelSize_medianBlur, kernelSize_dilation

def generate_dir_list(img_folder):
    img_dir_list = os.listdir(img_folder)

    #Add absolute path
    for i in range(len(img_dir_list)):
        img_dir_list[i] = img_folder + '/' + img_dir_list[i]

    #divide the images into many sub-groups
    batch_size = 30
    img_dir_list_chunks = [img_dir_list[x:x+batch_size] for x in range(0, len(img_dir_list), batch_size)]

    background = None
    for i in range(len(img_dir_list)):
        if "background" in img_dir_list[i]:
            background = img_dir_list.pop(i)
            break

    #Add background frames to the video
    for sub_group in img_dir_list_chunks:
        sub_group.insert(0, background)
    return img_dir_list_chunks

def crop(img, h_resize = 1480, w_resize = 2048):
    """
    Crop the image about the center to eliminate the heading part of the photos
    Args:
    img: cv2 image object
    h_resize, w_resize: new height and weight
    Returns:
    cropped: cropped image
    """

    h = img.shape[0]
    w = img.shape[1]
    center = (h/2, w/2)
    new_A = (int(center[0] - h_resize/2), int(center[1] - w_resize/2))
    new_C = (int(center[0] + h_resize/2), int(center[1] + w_resize/2))

    cropped = img[new_A[0]:new_C[0], new_A[1]:new_C[1]]

    return cropped

def create_video(img_dir_list_chunks, h_resize, w_resize):
    """
    Combine the available images (with the same background) to use in the background substration algorithm
    Returns:
    vid_dir: the path to the exported video
    """
    height = cv2.imread(img_dir_list_chunks[0][0]).shape[0]
    width = cv2.imread(img_dir_list_chunks[0][0]).shape[1]
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')

    vid_dir_list = []
    for i, img_dir_group in enumerate(img_dir_list_chunks):
        vid_dir = "out_vid_{}.avi".format(i+1)
        vid_dir_list.append(vid_dir)
        #vid = cv2.VideoWriter(vid_dir, fourcc, 20.0, (w_resize, h_resize))
        for img_dir in img_dir_group:
            frame = cv2.imread(img_dir)
            frame = crop(frame, h_resize, w_resize)
            #vid.write(frame)
        print("Written {}".format(vid_dir))
    return vid_dir_list

def process_img(mask, img, areaThreshold, kernelSize_medianBlur, kernelSize_dilation):
    #Blur the binary mask to reduce noise
    mask = cv2.medianBlur(mask,  ksize = kernelSize_medianBlur)

    #Draw bounding box
    label, (x1,x2,y1,y2), mask = drawBoundingBox(mask, img, kernelSize_dilation = kernelSize_dilation, areaThreshold = areaThreshold)

    return label, (x1,x2,y1,y2), mask

def filter_mask(fgMask, contours, kernelSize, areaThreshold):
    #Deleting environment noises
    for cnt_idx in range(len(contours)):
        if cnt_idx >= len(contours):
            break
        if cv2.contourArea(contours[cnt_idx]) < areaThreshold or cv2.contourArea(contours[cnt_idx]) < 0:
            contours.pop(cnt_idx)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))

    # Fill any small holes
    closing = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    # Dilate to merge adjacent blobs
    dilation = cv2.dilate(opening, kernel, iterations = 2)

    return dilation, contours

def drawBoundingBox(mask, img, kernelSize_dilation ,areaThreshold = 100):
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

    mask, contours = filter_mask(mask, contours, kernelSize_dilation, areaThreshold)
    min_x = 500000
    min_y = 500000
    max_x = 0
    max_y = 0

    #Drawing the big box containing all small boxes (due to noises)
    for cnt in contours:
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

    img = cv2.rectangle(img,(min_x,min_y),(max_x,max_y),(0,255,0),8)

    return img, (min_x, max_x, min_y, max_y), mask

def save_result(img, orig_img_name, bb_dir):
    """
    Save the resulted images with the bounding box for later investigation
    """

    cv2.imwrite(bb_dir + "/" + orig_img_name, img)

def writeLabel(img_dim, coordinates, bb_dir, filename):
    img_height, img_width = img_dim
    x1,x2,y1,y2 = coordinates

    center_x = ((x1 + x2) / 2) / img_width
    center_y = ((y1 + y2) / 2) / img_height

    width = (x2 - x1)/img_width
    height = (y2 - y1)/img_height

    filename = filename[:-4]
    File = open(bb_dir  + "/" +  filename + ".txt", "w")
    if filename == "background":
        File.write("")
    else:
        File.write("1 {} {} {} {}".format(center_x,center_y,width,height))
    File.close()

def substract_background(dir_info, kernelSize_medianBlur, kernelSize_dilation, areaThreshold):
    """
    Substracting the background and draw the bounding box around the desired animal
    Args:
    vid_dir: the video directory (the return of the function create_video)
    Return:
    None
    """

    vid_dir_list, img_dir_list_chunks, bb_dir, annotation_dir = dir_info

    for vid_idx, vid_dir in enumerate(vid_dir_list):
        cap = cv2.VideoCapture(vid_dir)
        if cap.isOpened() == False:
            print("Unable to open the video")
            exit(0)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        img_cache = []
        mask_cache = []

        count = 0
        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            if count == 0:
                fgMask = fgbg.apply(frame, None, 1.0)
            else:
                fgMask = fgbg.apply(frame, None, 0.01)
            img_cache.append(frame)
            mask_cache.append(fgMask)
            count += 1

        label_cache = np.copy(img_cache)

        if vid_idx == 0:
            cv2.namedWindow("Visualizing", cv2.WINDOW_FULLSCREEN)
            cv2.namedWindow("Adjusting params")
            create_trackbar(label_cache, mask_cache)
            key = cv2.waitKey(0)

        for idx in range(len(img_cache)):
            areaThreshold, kernelSize_medianBlur, kernelSize_dilation = getTrackbarValue()
            label_cache[idx], (x1,x2,y1,y2), mask_cache[idx]= process_img(mask_cache[idx], img_cache[idx], areaThreshold, kernelSize_medianBlur, kernelSize_dilation)

            filename = os.path.basename(img_dir_list_chunks[vid_idx][idx])
            save_result(label_cache[idx], filename, bb_dir)
            print("Saving " + bb_dir + "/" + filename)
            img_dim = (img_cache[0].shape[0], img_cache[0].shape[1])
            writeLabel(img_dim, (x1,x2,y1,y2), annotation_dir, filename)
        cap.release()
    cv2.destroyAllWindows()
