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

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    i = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        i = i + 1
        print(i)

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


def diff_abs(img1, img2):
    diff = cv2.absdiff(img1, img2)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    th = 1
    imask = mask > th

    canvas = np.zeros_like(img2, np.uint8)
    canvas[imask] = img2[imask]
    cv2.imshow("result.png", canvas)
    cv2.waitKey(0)


'''def test_similar():
    from iterto+ols import combinations
    from collections import defaultdict
    from heapq import heappush

    def sim1(img1, img2):
        h, w, d = img1.shape
        total = h * w * d
        diff = cv2.absdiff(img1, img2)
        num = (diff < 10).sum()
        return num * 1.0 / total

    names = [os.path.join('scene', c) for c in os.listdir('scene')]
    imgs = dict(zip(names, map(cv2.imread, names)))
    diffs = defaultdict(list)

    for name1, name2 in combinations(names, 2):
        img1, img2 = imgs[name1], imgs[name2]
        similarity = sim1(img1, img2)
        # print 'diff', name1, name2, 'result is:', similarity
        heappush(diffs[name1], (-similarity, name2))
        heappush(diffs[name2], (-similarity, name1))

    for k, v in diffs.iteritems():
        print(k, v[0][1], -v[0][0])
'''


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
    imageA = cv2.imread('test4.jpg')
    imageB = cv2.imread('test5.jpg')
    print(get_match_confidence(imageA, imageB))

    # diff_abs(imageA, imageB)
    print(diff_rect(imageA, imageB))


if __name__ == "__main__":
    main()

'''
    imageA = cv2.imread('test4.jpg')
    imageB = cv2.imread('test5.jpg')

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    i = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        i = i + 1
        print(i)

    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)

    img1 = cv2.imread("test4.jpg")
    img2 = cv2.imread("test9.jpg")
    diff = cv2.absdiff(img1, img2)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    th = 1
    imask = mask > th

    canvas = np.zeros_like(img2, np.uint8)
    canvas[imask] = img2[imask]
    cv2.imshow("result.png", canvas)
    cv2.waitKey(0)
   '''
