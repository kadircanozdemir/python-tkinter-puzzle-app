import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
import random

from MainFrame import MainFrame


def chunks(l, n):
    new_array = []
    for i in range(n):
        k = l[0 + i * n:4 + i * n]
        new_array.append(k)
    return new_array


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


def get_ij(arr, ij):
    for i in range(0, 4):
        for j in range(0, 4):
            if arr[i][j] == ij:
                return i, j


def get_shuffled_image(orj_img, indexes):
    shuffle_indexes = np.arange(16)
    random.shuffle(shuffle_indexes)
    shuffled_indexes = chunks(shuffle_indexes, 4)
    orginal_indexes = chunks(indexes, 4)
    # original_image = list()
    for i in range(0, 4):
        for j in range(0, 4):
            point = shuffled_indexes[i][j]
            r, c = get_ij(orginal_indexes, point)
            img_box = get_image_piece(orj_img, r, c)
            # original_image.append(img_box)
            cv2.imshow("aa", img_box)
            cv2.waitKey(0)
    # print(original_image)
    # cv2.imshow("aa", original_image)
    # cv2.waitKey(0)


def main():
    # mantıksal hatalar
    test_image = cv2.imread('karisik1.jpg')
    indexes = np.arange(16)

    print(chunks(indexes, 4))
    get_shuffled_image(test_image, indexes)
    # indexes = np.arange(16)
    # random.shuffle(indexes)
    # j = 0
    # suffled_indexes = []
    # for i in chunks(indexes, 4):
    #     suffled_indexes.append(i)
    #     j = j + 1
    # print(suffled_indexes)
    # print(get_loaction(suffled_indexes, 11))
    # i, j = get_loaction(suffled_indexes, 11)
    # get_image_piece(tsetimg, i, j)
    ####

    # imageA = cv2.imread("karisik1.jpg")
    # imageB = cv2.imread("karisik2.jpg")
    # root = Tk()
    # app = MainFrame(root)
    # app.pack(fill="both", expand=True)
    # root.mainloop()
    # print(test_similar(imageA, imageB))


if __name__ == "__main__":
    main()

    '''
    https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    https://www.programcreek.com/python/example/89428/cv2.absdiff
    https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
    '''
