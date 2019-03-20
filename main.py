import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils

from tkinter import *
from tkinter import filedialog

from MainFrame import MainFrame


def test_similar(img1, img2):
    h, w, d = img1.shape
    total = h * w * d
    '''
    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    '''
    diff = cv2.absdiff(img1, img2)
    print(diff)
    num = (diff < 1).sum()
    return num * 1.0 / total



def main():
    root = Tk()
    app = MainFrame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

    imageA = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
    imageB = cv2.imread("/Users/burakcokyildirim/Desktop/Screen Shot 2019-03-15 at 17.53.51.png")
    k = test_similar(imageA, imageB)
    print(k)


if __name__ == "__main__":
    main()

    '''
    https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
    https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    https://www.programcreek.com/python/example/89428/cv2.absdiff
    https://docs.opencv.org/2.4.13.7/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
    '''
