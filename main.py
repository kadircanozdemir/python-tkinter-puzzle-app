import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils


def diff_skit(img1, img2):
    imageA = img1
    imageB = img2

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    print("grey: ")
    print(compare_ssim(grayA, grayB, full=True))
    print("orj: ")
    # print(compare_ssim(imageA, imageB, full=True))

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print(score, diff)
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    j = 0
    num = (diff == 255).count()
    print(num, diff.size)

    print("j", j)
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)


def diff_rect(img1, img2, pos=None):
    """find counters include pos in differences between img1 & img2 (cv2 images)"""
    diff = cv2.absdiff(img1, img2)
    diff = cv2.GaussianBlur(diff, (3, 3), 0)
    print(diff)
    cv2.imshow("diff", diff)
    cv2.waitKey(0)
    edges = cv2.Canny(diff, 100, 200)
    _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return None
    contours.sort(key=lambda c: len(c))
    # no pos provide, just return the largest different area rect
    if pos is None:
        cnt = contours[-1]
        x0, y0, w, h = cv2.boundingRect(cnt)
        x1, y1 = x0 + w, y0 + h
        return (x0, y0, x1, y1)
    # else the rect should contain the pos
    x, y = pos
    for i in range(len(contours)):
        cnt = contours[-1 - i]
        x0, y0, w, h = cv2.boundingRect(cnt)
        x1, y1 = x0 + w, y0 + h
        if x0 <= x <= x1 and y0 <= y <= y1:
            return (x0, y0, x1, y1)
    cv2.imshow("contours", contours)
    cv2.waitKey(0)


def diff_abs(img1, img2):
    diff = cv2.absdiff(img1, img2)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    print(diff)
    th = 1
    imask = mask > th

    canvas = np.zeros_like(img2, np.uint8)
    canvas[imask] = img2[imask]
    cv2.imshow("result.png", canvas)
    cv2.waitKey(0)


def test_similar(img1, img2):
    h, w, d = img1.shape
    total = h * w * d

    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    # diff = cv2.absdiff(img1, img2)
    print(diff)
    num = (diff < 255).sum()
    return num * 1.0 / total


def get_match_confidence(img1, img2, mask=None):
    if img1.shape != img2.shape:
        return False
    ## first try, using absdiff
    # diff = cv2.absdiff(img1, img2)
    # h, w, d = diff.shape
    # total = h*w*d
    # num = (diff<20).sum()
    # print 'is_match', total, num
    # return num > total*0.90
    if mask is not None:
        img1 = img1.copy()
        img1[mask != 0] = 0
        img2 = img2.copy()
        img2[mask != 0] = 0
    ## using match
    match = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF)
    _, confidence, _, _ = cv2.minMaxLoc(match)
    # print confidence
    return confidence


def main():
    imageA = cv2.imread('karisik1.jpg')
    imageB = cv2.imread('karisik3.jpg')
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
