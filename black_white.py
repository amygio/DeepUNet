import cv2
from os import walk

paths = ["dataset/test/gt/0", "dataset/train/gt/0", "dataset/val/gt/0"]

for path in paths:

    images_name = []
    for (dirpath, dirnames, filenames) in walk(path):
        images_name.extend(filenames)
        
    for file_name in images_name:
        img = cv2.imread(path + "/" + file_name, cv2.IMREAD_GRAYSCALE)
        height, width = img.shape[:2]

        for x in range(0, width):
            for y in range(0, height):
                if img[x,y] < 127:
                    img[x,y] = 0
                else:
                    img[x,y] = 255
        
        cv2.imwrite(path + "/" + file_name, img)
        print("Immagine " + file_name + " salvata in " + path)
