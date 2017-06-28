from PIL import Image
from PIL.ExifTags import TAGS
import os, imghdr
import gmplot

debug  = False

def get_exifdata(file):
    try:
        img = Image.open(file)
        info = img._getexif()
        ret = {}
        useless = ['MakerNote']
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded not in useless:
                ret[decoded] = value
        return ret
    except(OSError):
        print("Wrong file format. Must be an image file.")
    return {'Error': True}


def get_coordinates(exifdata):
    if 'GPSInfo' in exifdata and len(exifdata['GPSInfo']) > 4:
        #print(exifdata['GPSInfo'])
        nsdeg = exifdata['GPSInfo'][2][0][0]
        nsmin = exifdata['GPSInfo'][2][1][0]
        nssec = exifdata['GPSInfo'][2][2][0] / 1000
        if exifdata['GPSInfo'][1] == 'S':
            south = True
        else:
            south = False

        ewdeg = exifdata['GPSInfo'][4][0][0]
        ewmin = exifdata['GPSInfo'][4][1][0]
        ewsec = exifdata['GPSInfo'][4][2][0] / 1000
        if exifdata['GPSInfo'][3] == 'W':
            west = True
        else:
            west = False

        #print(str(nsdeg) + '°' + str(nsmin) + '\'' + str(nssec) + '\"' + exifdata['GPSInfo'][1])
        #print(str(ewdeg) + '°' + str(ewmin) + '\'' + str(ewsec) + '\"' + exifdata['GPSInfo'][3])

        long = ewdeg + ewmin/60 + ewsec/3600
        lat = nsdeg + nsmin/60 + nssec/3600
        if west:
            long *= -1
        if south:
            lat *= -1

        return[lat, long]
    else:
        return None

def get_reording_times(exifdata):
    if 'DateTime' in exifdata:
        return exifdata['DateTime']
    else:
        return 'Kein Datum'

def get_recordingtimes_for_file(file):
    return get_reording_times(get_exifdata(file))

def get_recordingtimes_for_folder(folder):
    results = []
    for file in os.listdir(folder):
        tmp = get_recordingtimes_for_file(folder + file)
        if tmp:
            results.append(tmp)
    return results

def get_recordingtimes_for_exifdata(data):
    results = []
    for set in data:
        results.append(get_reording_times(set))
    return results

def get_coordinates_for_file(file):
    return get_coordinates(get_exifdata(file))


def get_coordinates_for_folder(folder):
    results = []
    for file in os.listdir(folder):
        try:
            if imghdr.what(folder + file):
                tmp = get_coordinates_for_file(folder + file)
        except(PermissionError):
            if debug:
                print('Permission to Subfolder denied')
        if tmp:
            results.append(tmp)
    return results

def get_coordinates_for_exifdata(data):
    results = []
    for set in data:
        results.append(get_coordinates(set))
    return results

def get_exif_data_for_folder(folder):
    results = []
    for file in os.listdir(folder):
        try:
            if imghdr.what(folder + file):
                tmp = get_exifdata(folder + file)
                if tmp:
                    results.append(tmp)
        except(PermissionError):
            if debug:
                print('Permission to Subfolder denied')
    return results

def get_image_paths_from_folder(folder):
    results = []
    for file in os.listdir(folder):
        try:
            if imghdr.what(folder + file):
                results.append(str(folder+file).replace('\\', '/').replace('\\', '/'))
        except(PermissionError):
            if debug:
                print('Permission to Subfolder denied')
    return results

def get_data_from_folders(folders):
    data = []
    for folder in folders:
        data.extend(get_exif_data_for_folder(folder))
    return data

def get_image_paths_from_folders(folders):
    images = []
    for folder in folders:
        images.extend(get_image_paths_from_folder(folder))
    return images



if __name__ == '__main__':
    gmap = gmplot.GoogleMapPlotter(0, 0, 1)

    folders =['D:\\Bilder\\Bilder Xperia Z2\\2016_Jan-Okt\\']

    data = get_data_from_folders(folders)

    coords = get_coordinates_for_exifdata(data)
    times = get_recordingtimes_for_exifdata(data)
    images = get_image_paths_from_folders(folders)

    x = 0
    for coord in coords:
        if coord:
            infoContent = times[x] + " <a href=\"file://" + images[x] + "\"> Image </a>"
            gmap.infoWindowMarker(coord[0], coord[1], "Hallo Welt!", infoWindow=True, infoContent=infoContent)
        x += 1

    gmap.infoWindowMarker(0, 0, title='Test', infoWindow=True, infoContent="<img src=\"https://upload.wikimedia.org/wikipedia/commons/5/53/Landshut_Kirche_St_Martin.jpg\" alt=\"Smiley face\" height=\"60\" width=\"60\">")

    gmap.draw("map.html")