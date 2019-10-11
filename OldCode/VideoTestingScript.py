import cv2
count = 0
cam = 4
values = []
for i in range(0,cam):
   cap = cv2.VideoCapture(i)
   test,frame = cap.read()
   if(test):
      count += 1
      values.append(frame)
   print("Camera number: " + str(i) + " works: " + str(test))
for i in range(0,len(values)):
   cv2.imshow(str(i),values[i])
k = cv2.waitKey(0)
cv2.destroyAllWindows()
