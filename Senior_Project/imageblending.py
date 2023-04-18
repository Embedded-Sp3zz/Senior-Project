import cv2
import os
from wand.image import Image

images_path = "images"
blends_path = "blends"

if(not(os.path.exists(blends_path))):
    os.makedirs("blends")
else:
    for f in os.listdir(blends_path):
        os.remove(os.path.join(blends_path, f))

for f in range(len(os.listdir(images_path)) - 1):
    for g in range(25):
        img1 = cv2.imread(f'images/image{f+1}.jpg')
        img2 = cv2.imread(f'images/image{f+2}.jpg')

        img1_blend = 1 - (g/25)
        img2_blend = g/25

        dist = cv2.addWeighted(img1, img1_blend, img2, img2_blend, 0)

        filename = blends_path + f'/blend_{f}_{g}.png'

        cv2.imwrite(filename, dist)


