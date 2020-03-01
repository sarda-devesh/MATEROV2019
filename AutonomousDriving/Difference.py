from scipy.spatial import distance as dist
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import os

def detect_color(videoinput, lower_bound, higher_bound, axis = 1): 
    lower_bound = np.array(lower_bound)
    higher_bound = np.array(higher_bound)
    hsv = cv2.cvtColor(videoinput, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, higher_bound)
    output = cv2.bitwise_and(videoinput, videoinput, mask = mask)
    cv2.imshow("Result", output)
    points = cv2.findNonZero(mask)
    result = []
    if str(type(points)) == "<class 'NoneType'>": 
        return result
    total = 0
    for point in points: 
        x, y = point[0][0], point[0][1]
        result.append([int(x), int(y)])
    return result

white_lower = (0, 0, 10)
white_higher = (20, 20, 100)
pink_lower = (135,150,20)
pink_higher = (155, 255, 255)

def runner(file_name): 
    frame = cv2.imread(file_name)
    white_points = detect_color(frame, white_lower, white_higher)
    print("The size of white is " + str(len(white_points)))
    pink_points = detect_color(frame, pink_lower, pink_higher)
    print("The size of pink points is " + str(len(pink_points)))
    for index in range(max(len(white_points), len(pink_points))): 
        if(index < len(white_points)): 
            cv2.circle(frame, (white_points[index][0], white_points[index][1]), 4, (255, 255, 255), -1)
        if(index < len(pink_points)): 
            cv2.circle(frame, (pink_points[index][0], pink_points[index][1]), 4, (0, 0, 255), -1)
    cv2.imshow("Display", frame)
    cv2.waitKey(0)

def color_determination(frame, scale = 1.0): 
    frame = cv2.resize(frame, None, fx = scale, fy = scale)
    points = []
    values = []
    count = 0

    def clicking(event, x, y, flags, param): 
        if event == cv2.cv2.EVENT_FLAG_MBUTTON:
            points.append((int(x), int(y)))

    cv2.namedWindow("Display")
    cv2.setMouseCallback("Display", clicking)

    while(True): 
        cv2.imshow("Display", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'): 
            break
        while(len(points) > 0): 
            count += 1
            x, y = points.pop(0)
            part = str(frame[y][x])
            #print("The color at point " + str(count) + " is " + part)
            values.append(part[1:len(part) - 1])
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
    
    sums = [0, 0, 0]

    for point in values: 
        broken = point.split(" ")
        broken = [x for x in broken if len(x) != 0]
        for index in range(len(broken)): 
            sums[index] += int(broken[index])
    
    sums = [item/len(values) for item in sums]
    total = 0
    for item in sums: 
        total += (255 - item) ** 2
    total = total ** 0.5
    print(str(sums) + "  " + str(total))

colors = [[245,240,235], #White
          [155, 95, 180], #Purple
          [125, 135, 137]] #Brown

def get_distance(color1, color2): 
    total = 0.0
    for index in range(len(color1)): 
        total += (color1[index] - color2[index]) ** 2.0
    return total ** 0.5

def nearest_color_method(videoinput): 
    height, width, channel = videoinput.shape
    points = [[] for item in colors]
    for y in range(height - 1, 0, -1): 
        for x in range(width): 
            current = videoinput[y][x]
            min_index = 0
            min_dist = get_distance(colors[0], current)
            for index in range(1, len(colors)): 
                c_dist = get_distance(colors[index], current)
                if c_dist < min_dist:
                    min_dist = c_dist
                    min_index = index
            points[min_index].append((int(x), int(y)))
    return points

def generate_histogram(frame, n_bins = 20): 
    height, width, channel = frame.shape
    points_one = []
    points_two = []
    for y in range(int(height)): 
        for x in range(int(width)): 
            values = frame[y][x]
            total = 0
            other = 0
            for item in values: 
                total += (255 - item) ** 2
                other += item ** 2
            total = total ** 0.5
            other = other ** 0.5
            points_one.append(total)
            points_two.append(other)
    print(len(points_one))
    print(len(points_two))
    
def display_result(videoinput, breakdown, file_name): 
    height, width, channels = videoinput.shape
    count = 0
    names = ["Whites", "Purple"]
    for item in breakdown: 
        image = np.zeros([height, width, channels], dtype= np.uint8)
        for point in item:
            cv2.circle(image, point, 1, (255, 255, 255), -1)
        #path = os.path.join(os.getcwd(), str(file_name) + "_Binary" + str(count) + ".jpg")
        #cv2.imwrite(path, image)
        cv2.imshow(names[count], image)
        count += 1
        cv2.waitKey(0)

def compare_points(p1, p2): 
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    bigger_x = x2 >= x1
    bigger_y = y2 >= y1
    if(bigger_x and bigger_y): 
        return (255, 0, 0)
    if (bigger_x and not bigger_y): 
        return (0, 255, 0)
    if (not bigger_x and bigger_y): 
        return (0, 0,255)
    return (0, 149, 255)

def perform_countour_detction(file_name): 
    im = cv2.imread(file_name)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if(cv2.contourArea(c) > 100): 
            points = list(c)
            n = len(points) 
            for index in range(n): 
                next_p = (index + 1) % n 
                p1 = points[index][0]
                p2 = points[next_p][0]
                val = compare_points(p1, p2)
                cv2.circle(im, (p1[0], p1[1]), 3, val, -1)
            #cv2.drawContours(im, [c], 0, (255, 0, 0), 2)
    cv2.imshow(file_name, im)
    cv2.waitKey(0)

def run_shape_detection(file_name): 
    image = cv2.imread(file_name)
    countours, heirarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, countours, -1, (0,255,0), 3)
    cv2.imshow('Contours', img)
    cv2.waitKey(0)

def compare_images(image1_name, image2_name, dis = 50): 
    im1 = cv2.imread(image1_name)
    cop = im1.copy()
    im2 = cv2.imread(image2_name)
    assert im1.shape == im2.shape
    h, w, c = im1.shape
    data = []
    for y in range(h): 
        for x in range(w): 
            first = im1[y][x]
            second = im2[y][x]
            distance = np.sqrt(np.sum((first - second)**2))
            data.append([(x,y), distance, first, second])
    data.sort(key = lambda tup: tup[1], reverse = True)
    #data = data[:min(len(data), dis)]
    for point in data: 
        cv2.circle(cop, point[0], 1, (255, 0, 255), -1)
        #print(str(point[1]) + " " + str(point[2]) + " " + str(point[3]))
    cv2.imshow("Differences", cop)
    cv2.waitKey(0)


if __name__ == "__main__": 
    file_name = "Comparison.jpg"
    img = cv2.imread(file_name)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_determination(hsv)
    #print(get_distance([249, 249, 249], [250, 250, 250]))
    cv2.destroyAllWindows()