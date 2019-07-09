from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import os
import argparse
import imutils
import cv2
import sys

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def process(part):
    # gray = cv2.cvtColor(part2, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (7, 7), 0)
    orig = part

    gray = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
    # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 355, 5)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(binary, 50, 100)
    edged = cv2.dilate(edged, None, iterations=2)
    edged = cv2.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None

    
    for c in cnts:
        # if the contour is not sufficiently large, ignore it

        if cv2.contourArea(c) < 2000:
            continue

        # compute the rotated bounding box of the contour
        orig = part.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            (255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        #if pixelsPerMetric is None:
            #pixelsPerMetric = dB / args["width"]
            #pixelsPerMetric = dB / 1

        # compute the size of the object
        pixelsPerMetric = 1633 / 20
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}cm".format(dimA),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}cm".format(dimB),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        # show the output image

        #cv2.imshow("Image", orig)
        #savname = "/home/zyf/PycharmProjects/bioproj/output_image/" +  filename
        #cv2.imwrite(savname, orig)
        #cv2.waitKey(0)
        return orig
    return orig

# ap = argparse.ArgumentParser()
# ap.add_argument("-w", "--width", type=float, required=True,
#     help="width of the left-most object in the image (in inches)")
# args = vars(ap.parse_args())

for filename in os.listdir("/home/zyf/PycharmProjects/bioproj/test/"):
    print(filename)
    imgname =  "/home/zyf/PycharmProjects/bioproj/test/" + filename
    image = cv2.imread(imgname)

    part1 = image[180:950, 550:1320]
    part2 = image[180:950, 1350:2120]
    part3 = image[980:1750, 550:1320]
    part4 = image[980:1750, 1350:2120]

    proce1 = process(part1)
    proce2 = process(part2)
    proce3 = process(part3)
    proce4 = process(part4)

    image[180:950, 550:1320] = proce1
    image[180:950, 1350:2120] = proce2
    image[980:1750, 550:1320] = proce3
    image[980:1750, 1350:2120] = proce4

    #cv2.namedWindow("1",cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("1", 1000, 1000)
    # cv2.imshow("1", image)
    savname = "/home/zyf/PycharmProjects/bioproj/output_image/" + filename
    cv2.imwrite(savname, image)

    #cv2.imshow("1", image)
    #cv2.waitKey()
sys.exit()

# src = "image/IMG00002.jpg"
# image = cv2.imread(src)
# part1 = image[180:950, 550:1320]
# part2 = image[180:950, 1350:2120]
# part3 = image[980:1750, 550:1320]
# part4 = image[980:1750, 1350:2120]
#
# proce1 = process(part1)
# proce2 = process(part2)
# proce3 = process(part3)
# proce4 = process(part4)
#
# image[180:950, 550:1320] = proce1
# image[180:950, 1350:2120] = proce2
# image[980:1750, 550:1320] = proce3
# image[980:1750, 1350:2120] = proce4
#
# cv2.namedWindow("1",cv2.WINDOW_NORMAL)
# cv2.resizeWindow("1", 1000, 1000)
# cv2.imshow("1", image)
# savname = "/home/zyf/PycharmProjects/bioproj/output_image/" +  "1231231.jpg"
# cv2.imwrite(savname, image)
#
# cv2.waitKey()