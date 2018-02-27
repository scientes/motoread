from glob import glob                                                           
import cv2
import os
for i in range(161,224):
    pngs = glob('buch2/char_'+str(i)+'/*.png')
    print(i)
    for j in pngs:
        img = cv2.imread(j)
        cv2.imwrite(j[:-3] + 'jpg', img)
        os.remove(j)

