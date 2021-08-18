# import necessary libraries
import cv2
import numpy as np
import random


def base(name):
    img = cv2.imread(name)

    # Convert image to gray colored and blur it
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.blur(img_gray, (3, 3))

    # show original image
    cv2.namedWindow("Input")
    cv2.imshow("Input", img)

    # initialize threshold value
    thresh = 100

    # call process method
    process(thresh, img_gray)

    cv2.waitKey()


def process(thresh_val, src_img):
    threshold = thresh_val

    # create canny image to detect edges
    imgThresh = cv2.Canny(src_img, threshold, threshold * 2)

    # draw contours
    contours, extra = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # initialize arrays to store contour details
    contours_poly = [0] * len(contours)
    centers = [0] * len(contours)
    radius = [0] * len(contours)

    for i, c in enumerate(contours):
        # store contour details
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    drawing = np.zeros((imgThresh.shape[0], imgThresh.shape[1], 3), dtype=np.uint8)

    # now we need to check maximum radius from all contours
    max_rad = 0
    color = (255, 0, 0)
    for i in range(len(contours)):
        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        cv2.drawContours(drawing, contours_poly, i, color)

        if int(radius[i]) > int(radius[max_rad]):
            max_rad = i

    # draw circle with maximum radius
    cv2.circle(drawing, (int(centers[max_rad][0]),
                         int(centers[max_rad][1])),
               int(radius[max_rad]), color, 2)

    # convert pixel value to millimeters
    diameter_mm = round(int(radius[max_rad]) * 0.2645833 * 2)

    # call classifier function
    category = classifier(diameter_mm)

    output_img_name = "output.jpg"
    cv2.imwrite(output_img_name, drawing)

    # put details on output image
    txt = "[{cat}] {mm}mm".format(cat=category, mm=diameter_mm)
    cv2.putText(drawing, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow('Output', drawing)

    print("Diameter : " + str(diameter_mm) + " mm")
    print("Category : " + category)


def classifier(diam):
    if diam < 47:
        return "Small"
    elif diam > 64:
        return "Large"
    else:
        return "Medium"


# cam = cv2.VideoCapture(0)
# img_name = ""
# cont = False
#
# while True:
#     ret, frame = cam.read()
#
#     # if there is an issue to open the webcam
#     if not ret:
#         print("failed to grab frame")
#         break
#
#     cv2.imshow("test", frame)
#     k = cv2.waitKey(1)
#
#     # press ESC button to cancel process
#     if k % 256 == 27:
#         print("Escape hit, closing...")
#         break
#
#     # press SPACE button to capture image
#     elif k % 256 == 32:
#         img_name = "input.jpg"
#         cv2.imwrite(img_name, frame)
#         cont = True
#         break
#
# cam.release()
# cv2.destroyAllWindows()
#
# if cont:
#     base(img_name)

base("test1.jpg")
