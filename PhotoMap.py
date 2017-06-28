import ExifReader
import argparse
import gmplot

def initArgparse():
    parser = argparse.ArgumentParser(description='Generates a map with photo locations')
    parser.add_argument('-f', '--folders', help='Folder(s) to search for images in', required=True, nargs='+')

    args = parser.parse_args()

    folders = vars(args)['folders']
    print(folders)

if __name__ == '__main__':
    ef = ExifReader.ExifReader()

    #initArgparse()

    gmap = gmplot.GoogleMapPlotter(0, 0, 1)

    folders =['D:\\Bilder\\Bilder Xperia Z2\\2016_Jan-Okt\\']

    data = ef.get_exif_data_from_folders(folders)

    coords = ef.get_coordinates_for_exifdata(data)
    times = ef.get_recordingtimes_from_exifdata(data)
    images = ef.get_image_paths_from_folders(folders)

    x = 0
    for coord in coords:
        if coord:
            infoContent = times[x] + " <a href=\"file://" + images[x] + "\"> Image </a>"
            gmap.infoWindowMarker(coord[0], coord[1], "Hallo Welt!", infoWindow=True, infoContent=infoContent)
        x += 1

    gmap.infoWindowMarker(0, 0, title='Test', infoWindow=True, infoContent="<img src=\"https://upload.wikimedia.org/wikipedia/commons/5/53/Landshut_Kirche_St_Martin.jpg\" alt=\"Smiley face\" height=\"60\" width=\"60\">")

    gmap.draw("map.html")