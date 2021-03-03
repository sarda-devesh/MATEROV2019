import cv2
import threading
import queue
import numpy as np
import time 

error = cv2.imread("brokenCamera.png")
class StreamReader: 
    def start_stream(self): 
        self.vc = cv2.VideoCapture(self.number + cv2.CAP_DSHOW)
        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def __init__(self, src, width = 640, height = 480): 
        self.number = src
        self.width = width
        self.height = height
        self.start_stream()
        self.active = False 
        self.need_to_read = False 
        self.frame = None 
        self.grabbed = False
        self.error = cv2.resize(error, (width, height))

    def start(self): 
        if self.active: 
            print("Already activated thread " + str(self.number))
            return None
        self.active = True 
        self.thread = threading.Thread(target=self.updating, args=())
        self.thread.start()
        return self
    
    def updating(self): 
        while(self.active): 
            self.grabbed, self.frame = self.vc.read()
            time.sleep(0.01)
    
    def restart(self): 
        self.active = False 
        while(True): 
            if not self.thread.is_alive(): 
                break 
        self.vc.release()
        self.start_stream()
        return self.start()
    
    def read(self): 
        if self.grabbed:
            return self.frame
        return self.error 
    
    def stop(self):
        self.active = False
        self.thread.join()
        self.vc.release()

def read_stream(streams, large_index, factor = 1.2): 
    try: 
        num = len(streams)
        top_image = streams[large_index].read()
        large_h, large_w, large_ch = top_image.shape
        if(num > 1): 
            base_image = None 
            for append in range(1, num): 
                new_i = (large_index + append) % num
                new_image = streams[new_i].read()
                new_h, new_w, new_ch = new_image.shape
                if base_image is None: 
                    base_image = new_image
                else: 
                    base_h, base_w, base_ch = base_image.shape
                    if base_h != new_h: 
                        scale = (1.0 * base_h)/new_h
                        new_image = cv2.resize(new_image, None, fx = scale, fy = scale, interpolation= cv2.INTER_NEAREST)
                    base_image = np.hstack((base_image, new_image))
            if not (base_image is None):
                base_h, base_w,base_ch = base_image.shape
                if large_w != base_w: 
                    scale = (1.0 * large_w)/base_w
                    base_image = cv2.resize(base_image, None, fx = scale, fy = scale, interpolation= cv2.INTER_NEAREST)
                base_h, base_w,base_ch = base_image.shape
                top_image = np.vstack((top_image, base_image))
        return top_image
    except Exception as e: 
        print("There was an error: " + str(e))
        return None

if __name__ == "__main__":
    large = 1
    streams = []
    number = 4
    for index in range(0, number):
        current = StreamReader(index)
        streams.append(current.start())
    time_total = 0
    time_count = 0
    while(True): 
        start = time.time()
        dis = read_stream(streams, large)
        if dis is None:
            print("Display is None")
            break 
        cv2.imshow("Display", dis)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'): 
            break
        if k == ord('a'):
            large = (large - 1) % number
        if k == ord('d'):
            large = (large + 1) % number
        time_total += time.time() - start
        time_count += 1
    print(time_count/time_total)
    for item in streams: 
        item.stop()
    cv2.destroyAllWindows()