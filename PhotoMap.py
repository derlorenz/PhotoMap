import ExifReader
import ImageTools

import argparse
import gmplot
import os
import platform

folders = []
targetHeight = 150

def initArgparse():
    global folders, targetHeight

    parser = argparse.ArgumentParser(description='Generates a map (website/index.html) with locatiions of your photos. '
                                                 'Photos are compressed and stored in website/resized')
    parser.add_argument('-f', '--folder', help='Folder to search for images in (can be uses multiple times)', action='append')
    parser.add_argument('-s', '--size', help='Spcecify the height the images should have after compression in px', default=150)

    args = parser.parse_args()

    folders = vars(args)['folder']
    targetHeight = vars(args)['size']

def createFolders():
    if not os.path.exists('website'):
        os.makedirs('website')
        os.makedirs('website/resized')

def parse_file_names(paths):
    filenames = []
    for path in paths:
        filenames.extend(path.split('/')[-1:])
    return filenames

if __name__ == '__main__':

    ef = ExifReader.ExifReader()
    im = ImageTools.ImageTools()

    initArgparse()
    createFolders()

    # Parse the folders so Windows is happy
    if platform.system() == 'Windows':
        correctFolders = []
        for folder in folders:
             correctFolders.append(folder + '\\')
        print(correctFolders)
    else:
        correctFolders = folders

    gmap = gmplot.GoogleMapPlotter(0, 0, 1)

    data = ef.get_exif_data_from_folders(correctFolders)

    coords = ef.get_coordinates_for_exifdata(data)
    times = ef.get_recordingtimes_from_exifdata(data)
    images = im.get_image_paths_from_folders(correctFolders)
    filenames = parse_file_names(images)
    im.resize_image(images, "website\\resized\\", targetHeight)

    x = 0
    for coord in coords:
        if coord:
            infoContent = "<p>" + times[x] + "</p> <img src=\"resized/" + filenames[x] + "\" >"
            gmap.infoWindowMarker(coord[0], coord[1], "Photo", infoWindow=True, infoContent=infoContent)
        x += 1

    gmap.draw("website/index.html")