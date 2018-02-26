import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
s=0
import os

for file in os.listdir(".\\ttf"):
    if file.endswith(".ttc"):
        print(os.path.join("\\.ttf", file))
    try:
        font = ImageFont.truetype(file,150)
        '''for j in range(0,9):
            try:
                img=Image.new("RGBA", (400,400),(255,255,255))
                draw = ImageDraw.Draw(img)
                draw.text((150, 150),str(j).lower(),(0,0,0),font=font)
                draw = ImageDraw.Draw(img)
                if not os.path.exists("buch"+"\\"+str(j).lower()):
                    os.makedirs("buch"+"\\"+str(j).lower())
                img.save("buch"+"\\"+str(j).lower()+"\\"+file+".png")
            except:
                pass
                #print(str(j))'''
        for i in range(0,224):
            if chr(i)!="" or chr(i)!="" or chr(i)!="": 
                try:
                    img=Image.new("RGBA", (400,400),(255,255,255))
                    draw = ImageDraw.Draw(img)
                    draw.text((150, 150),chr(i).lower(),(0,0,0),font=font)
                    draw = ImageDraw.Draw(img)
                    if not os.path.exists("buch"+"\\char_"+str(i)):
                        os.makedirs("buch"+"\\char_"+str(i))
                    img.save(".\\"+"buch"+"\\char_"+str(i)+"\\"+file+".png")
                except:
                    pass
                    #print(chr(i))
        for i in range(0,224):
            if chr(i)!="" or chr(i)!="" or chr(i)!="":
                try:
                    img=Image.new("RGBA", (400,400),(255,255,255))
                    draw = ImageDraw.Draw(img)
                    draw.text((150, 150),chr(i).upper(),(0,0,0),font=font)
                    draw = ImageDraw.Draw(img)
                    if not os.path.exists("buch"+"\\char_"+str(i)):
                        os.makedirs("buch"+"\\char_"+str(i))
                    img.save(".\\"+"buch"+"\\char_"+str(i)+"\\"+file+"upper"+".png")
                except:
                    pass
                    #print(chr(i))
    except:
        pass
