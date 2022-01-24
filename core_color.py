import rgb2lab
from PIL import Image, ImageCms
import numpy as np

# поиск среднего цвета на изображении(для настройки эталона)


def coreColor(img):

    im = Image.open(img)
    total_lab = [0, 0, 0]
    l, a, b = 0, 0, 0
    count = 0
    for i in im.getdata():
        lab = rgb2lab.rgb2lab(i)
        total_lab[0] += lab[0]
        total_lab[1] += lab[1]
        total_lab[2] += lab[2]
        count += 1
    resultint = [int(total_lab[0]/count), int(total_lab[1]/count),
              int(total_lab[2]/count)]
    result=str(resultint[0])+" "+str(resultint[1])+" "+str(resultint[2])
    return result


if __name__ == "__main__":
    coreColor("resrv/out.jpg")
