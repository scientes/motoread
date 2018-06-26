from io import BytesIO
from time import sleep
from PIL import Image
import PIL.ImageOps
import pytesseract
import PIL
import os
import imagehash
import time
#from picamera import PiCamera
import pyttsx3 as tts
def trim(im):
    from PIL import Image, ImageChops
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


"""
my_stream = BytesIO()
camera = PiCamera()
camera.start_preview()
sleep(15)
camera.capture(my_stream, 'png')
print("hi")
"""
def computehash(image_stream):
    dimage=imagehash.dhash(image_stream)
def image_opt(my_stream):
    image=Image.open(my_stream)
    #image.save("test2.png")

    im = image.convert("L")
    #im.show()
    im = PIL.ImageOps.autocontrast(im, 0.8)
    th = 120  # the value has to be adjusted for an image of interest

    im = im.point(lambda i: i < th and 255)

    im= trim(im)

    width = im.size[0]
    height = im.size[1]
    a=(int((width * 0.2) / 2), int((height * 0.5) / 2), width-int((height * 0.3) / 2), height - int((height * 0.5) / 2))
    return im.crop(a)
    #im.show()
    """text = pytesseract.image_to_string(im)
    print(text)
    engine=tts.init()
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', "german")
    engine.say(text)
    engine.runAndWait()
    #im.save("test.png")
    """
if __name__=="__main__":
    lis=os.listdir("motomed_live")
    for i in range(len(lis)):
        lis[i]="motomed_live/"+lis[i]
    hashlist=[]
    star1=time.clock()
    for i in range(len(lis)):
        start=time.clock()
        image=image_opt(lis[i])
        ihash=imagehash.dhash(image,hash_size=32)
        hashlist.append(ihash)
        end=time.clock()
        if i>0:
            distance=ihash-oldhash
            print(i, " time taken: ", end - start, "s fps:", 25 / (end - start), " distance:", distance)
            if distance>30:
                #image.show()
                #sleep(0.5)
                oldhash = ihash

        else:
            oldhash=ihash

    end1=time.clock()
    print(len(lis),end1-star1,len(lis)/(end1-star1))