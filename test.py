from io import BytesIO
from time import sleep
from PIL import Image
import PIL.ImageOps
import pytesseract
import PIL
from picamera import PiCamera
import pyttsx3 as tts
def trim(im):
    from PIL import Image, ImageChops
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)



my_stream = BytesIO()
camera = PiCamera()
camera.start_preview()
sleep(15)
camera.capture(my_stream, 'png')
print("hi")

image=Image.open(my_stream)
image.save("test2.png")

im = image.convert("L")
im.show()
im = PIL.ImageOps.autocontrast(im, 0.8)
th = 150  # the value has to be adjusted for an image of interest

im = im.point(lambda i: i < th and 255)

im = trim(im)
width = im.size[0]
height = im.size[1]
im = im.crop((0, int((height * 0.5) / 2), width, height - int(height * 0.5 / 2)))
im.show()
text = pytesseract.image_to_string(im)
print(text)
engine=tts.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', "german")
engine.say(text)
engine.runAndWait()
#im.save("test.png")
