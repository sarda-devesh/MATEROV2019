from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init(self): 
        colors = OrderedDict({"white": (245, 240, 235),"purple": (155, 95, 180),"brown": (125, 135, 137)})
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        for (i, (name, rgb)) in enumerate(colors.items()):
            