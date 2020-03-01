import cv2
import sys
import numpy as np
import math
import os 

def nothing(x):
    pass

def determine_bounds(frame, scale = 0.01):
    cv2.namedWindow("Adjustment")
    area = scale * frame.shape[0] * frame.shape[1]
    cv2.createTrackbar('HMin','Adjustment',0,179,nothing) 
    cv2.createTrackbar('SMin','Adjustment',0,255,nothing)
    cv2.createTrackbar('VMin','Adjustment',0,255,nothing)
    cv2.createTrackbar('HMax','Adjustment',0,179,nothing)
    cv2.createTrackbar('SMax','Adjustment',0,255,nothing)
    cv2.createTrackbar('VMax','Adjustment',0,255,nothing)
    cv2.setTrackbarPos('HMax', 'Adjustment', 179)
    cv2.setTrackbarPos('SMax', 'Adjustment', 255)
    cv2.setTrackbarPos('VMax', 'Adjustment', 255)
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0
    wait_time = 1
    while(1):
        image = frame.copy()
        hMin = cv2.getTrackbarPos('HMin','Adjustment')
        sMin = cv2.getTrackbarPos('SMin','Adjustment')
        vMin = cv2.getTrackbarPos('VMin','Adjustment')
        hMax = cv2.getTrackbarPos('HMax','Adjustment')
        sMax = cv2.getTrackbarPos('SMax','Adjustment')
        vMax = cv2.getTrackbarPos('VMax','Adjustment')
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for cnt in contours: 
            if cv2.contourArea(cnt) > scale: 
                cv2.drawContours(image, [cnt], 0, (0, 255, 0), 3)
        if( (phMin != hMin) or (psMin != sMin) or (pvMin != vMin) or (phMax != hMax) or (psMax != sMax) or (pvMax != vMax) ): 
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax
        cv2.imshow('Adjustment',image)
        if cv2.waitKey(wait_time) & 0xFF == ord('o'):
            cv2.destroyWindow('Adjustment' )
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            return None

lower_white = (0,0,222)
upper_white = (180,255,255)

lower_purple = (0, 70, 0)
upper_purple = (179, 255, 255)

def get_general_shape(img, border = 20): 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_white, upper_white)
    mask2 = cv2.inRange(hsv, lower_purple, upper_purple)
    return mask1, mask2

def adjust_originial(originial, changed): 
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(originial,None)
    kp2, des2 = sift.detectAndCompute(changed,None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    ch, cw = changed.shape
    third = cv2.warpPerspective(originial, M, (cw, ch))
    return third, M

def display_countours(second_image, differences, color, coordinates): 
    kernel = np.ones((7,7),np.uint8)
    differences = cv2.erode(differences,kernel,iterations = 1)
    cv2.imshow(str(color), differences)
    area_threshold = 0.005 * differences.shape[1] * differences.shape[0]
    differences, contours, hierarchy = cv2.findContours(differences, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    val = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        val = max(area, val)
        if(area > area_threshold): 
            x,y,w,h = cv2.boundingRect(cnt)
            coordinates.append([x, y, x + w, y + h, color[0], color[1], color[2]])

def non_maximum_supression(boxes, threshold): 
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes, dtype=np.float32)
    pick = []
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]
        idxs = np.delete(idxs, np.concatenate(([last],np.where(overlap > threshold)[0])))
    return boxes[pick].astype("int")

def run_image_recognition(file_1, file_2, border = 5, threshold = 0.9): 
    coordinates = []
    first_image = cv2.imread(file_1)
    second_image = cv2.imread(file_2)
    firstw, firstp = get_general_shape(first_image)
    secondw, secondp = get_general_shape(second_image)
    assert firstw.shape == firstp.shape
    assert secondw.shape == secondp.shape

    fh, fw = firstw.shape
    sh, sw = secondw.shape
    goalh, goalw = max(fh, sh), max(fw, sw)
    secondw = cv2.resize(secondw, None, fx = goalw/sw, fy = goalh/sh) 
    secondp = cv2.resize(secondp, None, fx = goalw/sw, fy = goalh/sh)
    firstw = cv2.resize(firstw, None, fx = goalw/fw, fy = goalh/fh)
    firstp = cv2.resize(firstp, None, fx = goalw/fw, fy = goalh/fh)
    sh, sw, sc = second_image.shape
    second_image = cv2.resize(second_image, None, fx = goalw/sw, fy = goalh/sh)

    first = cv2.add(firstw, firstp)
    second = cv2.add(secondw, secondp)
    third, M = adjust_originial(first, second) 

    sh, sw = secondw.shape
    firstp = cv2.warpPerspective(firstp, M, (sw, sh))
    differences = cv2.subtract(secondp, firstp)
    display_countours(second_image, differences, (255, 0, 0), coordinates)
    differences = cv2.subtract(firstp, secondp)
    display_countours(second_image, differences, (0, 0, 255), coordinates)

    differences = cv2.subtract(second, third)
    display_countours(second_image, differences, (0, 100, 0), coordinates)
    differences = cv2.subtract(third, second)
    display_countours(second, differences, (0, 255, 255), coordinates)

    boxes = non_maximum_supression(coordinates, threshold)
    for box in boxes: 
        removed = box[4:]
        color = tuple([int(x) for x in removed])
        cv2.rectangle(second_image, (box[0] - border, box[1] - border), (box[2] + border, box[3] + border), color, 2)
    cv2.imshow("Final", second_image)

if __name__ == "__main__": 
    run_image_recognition("Comparison.jpg", "Detection2.jpg")
    cv2.waitKey(0)
    #determine_bounds(cv2.imread("Start.jpg"))
    cv2.destroyAllWindows()