from PIL import Image
from PIL.ExifTags import TAGS
import io
import urllib
import numpy as np

def get_exif_from_bytes(img_bytes):
    img_data = io.BytesIO(img_bytes)
    ret = {}
    try:
        img = Image.open(img_data)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + img_data
    return ret

def get_exif(img):
    ret = {}
    if hasattr(img, '_getexif' ):
        exifinfo = img._getexif()
        if exifinfo != None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    return ret

def get_attr_img_from_url(img_url):
    resp = urllib.urlopen('test.jpg')
    img_bytes = np.asarray(bytearray(resp.read()), dtype = 'uint8')
    img_data = io.BytesIO(img_bytes)
    img = Image.open(img_data)
    exif = get_exif(img)

    print exif['GPSInfo']
    print exif['DateTime']

if __name__ == '__main__':
    get_attr_img_from_url('test.jpg')
    # resp = urllib.urlopen('test.jpg')
    # img_bytes = np.asarray(bytearray(resp.read()), dtype = 'uint8')
    # exif = get_exif_from_bytes(img_bytes)
    # # fileName = 'test.jpg'
    # # exif = get_exif_data(fileName)
    # print exif['GPSInfo']
    # print exif['DateTime']