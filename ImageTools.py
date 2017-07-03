import imghdr
import os
from PIL import Image

class ImageTools():

    def __init__(self, debug=False):
        self.debug = debug


    def get_image_paths_from_folders(self, folders):
        images = []
        for folder in folders:
            images.extend(self.get_image_paths_from_folder(folder))
        return images


    def get_image_paths_from_folder(self, folder):
        results = []
        for file in os.listdir(folder):
            try:
                if imghdr.what(folder + file):
                    results.append(str(folder + file).replace('\\', '/').replace('\\', '/'))
            except PermissionError:
                if self.debug:
                    print('Permission to Subfolder denied')
        return results

    def resize_image(self, imagePaths, savePath, imgHeight):
        for imagePath in imagePaths:
            img = Image.open(imagePath)
            rel = imgHeight/img.size[1]
            img = img.resize((int(img.size[0]*rel), int(img.size[1]*rel)), Image.ANTIALIAS)
            filename = imagePath.split('/')[-1:]
            img.save(savePath + filename[0])