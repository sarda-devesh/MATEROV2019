import cv2
import numpy as np
import imutils
import os 
from Testing import determine_bounds

def detect_color(videoinput, lower_bound, higher_bound, axis = 1): 
    lower_bound = np.array(lower_bound)
    higher_bound = np.array(higher_bound)
    hsv = cv2.cvtColor(videoinput, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, higher_bound)
    points = cv2.findNonZero(mask)
    result = []
    if str(type(points)) == "<class 'NoneType'>": 
        return result
    total = 0
    for point in points: 
        x, y = point[0][0], point[0][1]
        result.append([int(x), int(y)])
    return result

def detect_blue_lines(videoinput, axis = 0): 
    bluelower = (100, 200, 20)
    bluehigher = (140, 255, 255)
    points = detect_color(videoinput, bluelower, bluehigher)
    if(len(points) == 0):
        return -1
    total = 0
    for point in points:
        total += point[axis]
        cv2.circle(videoinput, (point[0], point[1]), 2, (255, 0, 255), -1)
    avg_axis = int(total/len(points))
    height, width, channel = videoinput.shape
    pt1 = (avg_axis, int(height/2))
    if(axis == 1): 
        pt1 = (int(width/2), avg_axis)
    pt2 = (int(width/2), int(height/2))
    cv2.circle(videoinput, pt1, 15, (255, 0, 0,), -1) #Blue:Points
    cv2.circle(videoinput, pt2, 15, (0, 0, 255), -1) #Red:Overall
    return (avg_axis - videoinput.shape[1 - axis]/2)/(videoinput.shape[1-axis])

def can_detect_black(videoinput, axis = 1, threshold = 0.0015): 
    blacklower = (0,0,0)
    blackhigher = (170, 238, 40) 
    min_area = threshold * videoinput.shape[0] * videoinput.shape[1]
    lower_bound = np.array(blacklower)
    higher_bound = np.array(blackhigher)
    hsv = cv2.cvtColor(videoinput.copy(), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, higher_bound)
    mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    values = [0, 0, 0, 0, 0]
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if (w * h > values[0]): 
            values[0] = w * h
            values[1] = x
            values[2] = y
            values[3] = x + w
            values[4] = y + h
    return values, mask

def blueVideo(file_name, scale = 1.3, count = 15): 
    stream = cv2.VideoCapture(file_name)
    paused = True
    ending_found = False
    starting = cv2.imread("Ending.jpg")
    cv2.imshow("Display", starting)
    frame_count = 0
    original = None 

    countour_areas = [0 for number in range(count)]
    index = 0 

    while(stream.isOpened() and not ending_found): 
        if not paused:
            ret, frame = stream.read() 
            if not ret:
                print("End of video")
                break
            original = frame.copy()
            value = detect_blue_lines(frame)
            biggest_countour, mask = can_detect_black(frame)
            countour_areas[index] = biggest_countour[0] 
            average = np.average(countour_areas)
            index = (index + 1) % count 
            cv2.rectangle(frame, (biggest_countour[1], biggest_countour[2]), (biggest_countour[3], biggest_countour[4]), (0, 100, 0), 2)
            frame = cv2.copyMakeBorder(frame, 0, 200, 0, 0, cv2.BORDER_CONSTANT)
            height, width, ch = frame.shape
            frame = cv2.putText(frame, "Difference is " + str(value), (10, int(height) - 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            frame = cv2.putText(frame, "Running average is " + str(average), (10, int(height) - 75), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Display", mask)
            cv2.imshow("Actual", frame)
        k = cv2.waitKey(30) & 0xFF
        if k == ord('q'): 
            print("User quit")
            break 
        elif k == ord('p'): 
            paused =  not paused
        elif k == ord('a'): 
            if not (original is None):
                determine_bounds(original)
            else:
                print("Originial is None")
        frame_count += 1
    stream.release()

min_number_of_points = 35
max_iqr_value = 0.05


if __name__=='__main__': 
    name = "Transect 2.MOV"
    blueVideo(name)
    cv2.destroyAllWindows()