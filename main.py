import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
import random

from MainFrame import MainFrame


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def test_similar(img1, img2):
    h, w, d = img1.shape
    total = h * w * d
    diff = cv2.absdiff(img1, img2)
    num = (diff < 1).sum()
    return num * 100.0 / total


def get_image_piece(img, i, j):
    # if not (0 < i < 5 | 0 < j < 5): error!
    try:
        image_box = img
        h = image_box.shape[0]
        box_length = int(h / 4)
        return image_box[0 + box_length * i:100 + box_length * i, 0 + box_length * j:100 + box_length * j, :]
    except:
        print("slice error!")


def get_loaction(arr, xy):
    for i in range(0, 4):
        for j in range(0, 4):
            if arr[i][j] == xy:
                return i, j


def main():
    # mantıksal hatalar
    tsetimg = cv2.imread('karisik1.jpg')
    indexes = np.arange(16)
    random.shuffle(indexes)
    j = 0
    suffled_indexes = []
    for i in chunks(indexes, 4):
        suffled_indexes.append(i)
        j = j + 1
    print(suffled_indexes)
    print(get_loaction(suffled_indexes, 11))
    i, j = get_loaction(suffled_indexes, 11)
    get_image_piece(tsetimg, i, j)
    ####

    imageA = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
    imageB = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
    root = Tk()
    app = MainFrame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()

    '''
    https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    https://www.programcreek.com/python/example/89428/cv2.absdiff
    https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
    '''
