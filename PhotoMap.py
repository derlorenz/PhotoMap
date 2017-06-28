import ExifReader
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

if __name__ == '__main__':

    ef = ExifReader.ExifReader()

    initArgparse()

    #Parse the folders so Windows is happy
    if platform.system() == 'Windows':
        correctFolders = []
        for folder in folders:
             correctFolders.append(folder + '\\\\')
        print(correctFolders)
    else:
        correctFolders = folders

    gmap = gmplot.GoogleMapPlotter(0, 0, 1)

    data = ef.get_exif_data_from_folders(correctFolders)

    coords = ef.get_coordinates_for_exifdata(data)
    times = ef.get_recordingtimes_from_exifdata(data)
    images = ef.get_image_paths_from_folders(correctFolders)

    x = 0
    for coord in coords:
        if coord:
            infoContent = times[x] + " <a href=\"file://" + images[x] + "\"> Image </a>"
            gmap.infoWindowMarker(coord[0], coord[1], "Photo", infoWindow=True, infoContent=infoContent)
        x += 1

    gmap.draw("map.html")