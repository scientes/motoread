import os
import time
from io import BytesIO
from time import sleep

import PIL
import PIL.ImageOps
import cv2
import imagehash
import numpy as np
import pytesseract
from PIL import Image
from imutils.object_detection import non_max_suppression


def image_opt(my_stream, cropxt, cropyt, cropxb, cropyb):
    image = Image.open(my_stream)
    # image.save("test2.png")

    im = image.convert("L")
    # im.show()
    im = PIL.ImageOps.autocontrast(im, 0.6)
    th = 170  # the value has to be adjusted for an image of interest

    im = im.point(lambda i: i < th and 255)

    im = trim(im)

    width = im.size[0]
    height = im.size[1]
    a = (int((width * cropyt) / 2), int((height * cropxt) / 2), width - int((width * cropyb) / 2),
         height - int((height * cropxb) / 2))
    return im.crop(a)
    # im.show()


def pil_to_cv2_gray(image):
    image = np.array(image)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def pre_cv2(image_src):
    image = cv2.GaussianBlur(image_src, (5, 5), 0)
    cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return image


def blurr_ratio(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def trim(im):
    from PIL import Image, ImageChops
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def hash_test():
    lis = os.listdir("motomed_live")
    for i in range(len(lis)):
        lis[i] = "motomed_live/" + lis[i]
    hashlist = []
    star1 = time.clock()
    for i in range(len(lis)):
        start = time.clock()
        image = image_opt(lis[i], 0.2, 0.5, 0.3, 0.5)
        ihash = imagehash.dhash(image, hash_size=32)

        end = time.clock()
        if i > 0:
            distance = ihash - oldhash
            hashlist.append((distance, lis[i], ihash))

            if distance > 67:
                # sleep(0.5)
                star2 = time.clock()
                cv_image = np.array(image)
                result = blurr_ratio(cv_image)
                # result=0
                end2 = time.clock()
                print(i, " time taken: ", end - start, "s fps:", 25 / (end - start), " distance:", distance, "result",
                      result, "time", end2 - star2)
                oldhash = ihash

        else:
            oldhash = ihash

    end1 = time.clock()
    print(len(lis), end1 - star1, len(lis) / (end1 - star1))


"""
def initialize_cam():
    from picamera import PiCamera
    import time
    camera = PiCamera()
    camera.color_effects = (128, 128)
    time.sleep(2)
    return camera
"""


def take_picture(camera):
    my_stream = BytesIO()
    camera.capture(my_stream, 'png')
    return Image.open(my_stream)


def save_image(image, name):
    image.save(name)


def controllout(camera):
    import time
    i = 0
    while True:
        start = time.clock()
        image = take_picture(camera)
        save_image(image, "testpicture/" + str(i) + ".png")
        stop = time.clock()
        if 0.06 - stop - start > 0:
            sleep(0.06 - stop - start)


def splitter(image, net, resize_w=320, resize_h=320, min_confidence=0.3):
    orig = image.copy()
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    (H, W) = image.shape[:2]
    rW = W / float(resize_w)
    rH = H / float(resize_h)
    image = cv2.resize(image, (resize_w, resize_h))
    (H, W) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)  # (123.68, 116.78, 103.94)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    return_image = []
    for (b_startX, b_startY, b_endX, b_endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        a_startX = int(b_startX * rW * 0.97)
        a_startY = int(b_startY * rH * 0.97)
        a_endX = int(b_endX * rW * 1.03)
        a_endY = int(b_endY * rH * 1.03)

        # draw the bounding box on the image

        cv2.rectangle(orig, (a_startX, a_startY), (a_endX, a_endY), (0, 255, 0), 2)
        return_image.append((a_startX, a_endX, a_startY, a_endY))

    return return_image


def ocr(insert):
    image, y1, y2, x1, x2 = insert
    return pytesseract.image_to_string(image,
                                       config="--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz:[] --oem 3"), y1, y2, x1, x2


if __name__ == "__main__":
    from multiprocessing import Pool
    from spellchecker import SpellChecker

    # https://github.com/barrust/pyspellchecker
    spell = SpellChecker()
    lis = os.listdir("motomed_live")
    east = cv2.dnn.readNet("frozen_east_text_detection.pb")
    p = Pool(4)
    for i in range(len(lis)):
        start = time.clock()
        print(lis[i])
        image = cv2.imread("motomed_live\\" + lis[i])
        # u_image = cv2.UMat(image)

        h, w, d = image.shape
        crop = 0.2
        y2_new = int(h - (h * crop))
        y1_new = int(h * crop)
        x1_new = 0
        x2_new = w
        image = image[y1_new:y2_new, 1:-1]
        # cv2.imshow("hi3",image)

        # print("start")
        pre_gray = pre_cv2(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        # cv2.imshow("pregray",pre_gray)
        pre = cv2.cvtColor(pre_gray, cv2.COLOR_GRAY2RGB)
        # cv2.imshow("pre",pre)

        rect = splitter(pre, east, 32 * 16, 32 * 9)  # 1920//4,1056//4
        # cv2.imshow("test", cv2.resize(rect,(0,0),fx=0.5,fy=0.5))
        n = 0

        q = []
        for i in rect:
            # print(i[0],i[1],i[2],i[3])
            roi = image[i[2]:i[3], i[0]:i[1]]

            # cv2.imshow("result"+str(n),roi)
            n += 1
            q.append((roi, i[2], i[3], i[0], i[1]))
        print(p.map(ocr, q))
        q = []
        end = time.clock()
        print(end - start, "s")
        # prepro=pre_cv2(cv2.cvtColor(u_image, cv2.COLOR_BGR2GRAY))
        # cv2.imshow("hi_pre",prepro)
        # text=pytesseract.image_to_string(cv2.UMat.get(image),config="--psm 1")
        # cv2.waitKey(0)

    print("hi")
