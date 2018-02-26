from PIL import Image, ImageChops
import os


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

i=0
width=0
height=0
root_old=""

for root, directories, filenames in os.walk('buch'):
    for filename in filenames:
        try:
            if root_old!=root:
                root_old=root
                print(root)
            im=Image.open(os.path.join(root, filename))
            im=trim(im)
            wi=im.size[0]
            he=im.size[1]
            if he>height:
                height=he
            if wi>width:
                width=wi
            i+=1
        except:
            pass

for root, directories, filenames in os.walk('buch'):
    for filename in filenames:
        try:
            if root_old!=root:
                root_old=root
                print("size_changed :"+root)
            im=Image.open(os.path.join(root, filename))
            im=trim(im)
            img_w, img_h = im.size
            background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            background.paste(im, offset)
            background.save("buch2"+os.path.join(root, filename)[4:])
            i+=1
        except:
            pass

print(width)
print(height)
print(i)

im=Image.open("ACaslonPro-Bold.otf.png")
im = trim(im)
im.show()
print(im.size)
img_w, img_h = im.size
background=Image.new('RGBA', (width, height), (255, 255, 255, 255))
bg_w, bg_h = background.size
offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
background.paste(im, offset)
background.save('out.png')
