import sys
import glob
import os
import time
import threading
import cv2
import rgb2lab
import configurator
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from PIL import Image


def colorAnalysis(reference_mass, reference_delta_mass, stand, img):
    result_mass = []
    stand = LabColor(stand[0]/100, stand[1], stand[2])
    im = Image.open(img)
    total_count = 0
    count_of_suitable = []
    for i in range(len(reference_mass)):
        count_of_suitable.append(0)
    for pix in im.getdata():
        for i in range(len(reference_mass)):
            reference = reference_mass[i]
            reference_delta = reference_delta_mass[i]
            reference = LabColor(reference[0]/100, reference[1], reference[2])
            lab = rgb2lab.rgb2lab(pix)
            lab_color = LabColor(lab[0]/100, lab[1], lab[2])
            delta_s = delta_e_cie2000(lab_color, stand)
            if(delta_s < 10):
                continue
            delta_r = delta_e_cie2000(lab_color, reference)
            if(delta_r < reference_delta):
                count_of_suitable[i] += 1
                break
    for count in count_of_suitable:
        total_count += count
    for i in range(len(count_of_suitable)):
        count_of_suitable[i] = round(count_of_suitable[i]/total_count, 4)*100
        print(count_of_suitable[i])
    return count_of_suitable


if __name__ == "__main__":
    print(colorAnalysis([(74, 3, 70)], [80], (35, 30, 38), 'src\\src.jpg'))
