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


# from picamera import PiCamera

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


# def computehash(image_stream):
#    dimage = imagehash.dhash(image_stream)
#    return dimage


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


def blur_test():
    lis = os.listdir("motomed_live")
    for i in range(len(lis)):
        lis[i] = "motomed_live/" + lis[i]
    star1 = time.clock()
    for i in range(len(lis)):
        start = time.clock()
        result = blurr_ratio(cv2.imread(lis[i]))
        end = time.clock()
        print(end - start, "s", "result:", result)
    end1 = time.clock()
    print(len(lis), end1 - star1, len(lis) / (end1 - star1))


def tts_init():
    from time import sleep
    engin = tts.init()
    engin.setProperty('voice', "german")
    sleep(1)
    return engin


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


def testing_pictures(camera):
    import time
    camera.start_preview()
    time.sleep(20)
    camera.stop_preview()


def image_to_text(image):
    return pytesseract.image_to_string(image)


def text_to_sound(text):
    engine.say(text)
    engine.runAndWait()


def preview(camera, engine):
    image = take_picture(camera)
    image = image_opt(image, 1, 1, 1, 1)
    output = image_to_text(image)
    print(output)
    text_to_sound(output)


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


if __name__ == "__main__":
    cv2.UMat
    # camera = initialize_cam()
    engine = tts_init()
    hash_test()
    # blur_test()
