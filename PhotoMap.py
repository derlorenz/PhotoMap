import ExifReader
import ImageTools

import argparse
import gmplot
import os
import platform

folders = []

def initArgparse():
    global folders

    parser = argparse.ArgumentParser(description='Generates a map with photo locations')
    parser.add_argument('-f', '--folder', help='Folder to search for images in (can be uses multiple times)', action='append')

    args = parser.parse_args()

    folders = vars(args)['folder']

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
    im.resize_image(images, "website\\resized\\", 150)

    x = 0
    for coord in coords:
        if coord:
            infoContent = "<p>" + times[x] + "</p> <img src=\"resized/" + filenames[x] + "\" >"
            gmap.infoWindowMarker(coord[0], coord[1], "Photo", infoWindow=True, infoContent=infoContent)
        x += 1

    gmap.draw("website/index.html")