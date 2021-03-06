from PIL import Image
from PIL.ExifTags import TAGS
import io
import urllib
import numpy as np
import cv2

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
    try:
        resp = urllib.urlopen(img_url)
        img_bytes = np.asarray(bytearray(resp.read()), dtype = 'uint8')
        img_data = io.BytesIO(img_bytes)
        img = Image.open(img_data)
    except Exception as e:
        return 401, None, None
    img_cv = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    exif = get_exif(img)
    res_dic = {}
    if exif.has_key('GPSInfo'):
        gps_info = exif['GPSInfo']
        if gps_info.has_key(2) and gps_info.has_key(4):
            longi = str(gps_info[2][0][0]) + '.' + str(gps_info[2][1][0])
            latitu = str(gps_info[4][0][0]) + '.' + str(gps_info[4][1][0])
            res_dic['GPSInfo'] = (longi, latitu)
    if exif.has_key('DateTime'):
        res_dic['DateTime'] = exif['DateTime']
    return 201, res_dic, img_cv

if __name__ == '__main__':
    code, res_dic, img = get_attr_img_from_url('http://pic09.babytreeimg.com/2018/0425/FsePbf1XfJ2ZzjG4uL9t6p4gqp7n')
    if code != 201:
        print code
    else:
        print res_dic['GPSInfo']
        print res_dic['DateTime']
        # cv2.imshow('show', img)
        # cv2.waitKey(0)
    # resp = urllib.urlopen('test.jpg')
    # img_bytes = np.asarray(bytearray(resp.read()), dtype = 'uint8')
    # exif = get_exif_from_bytes(img_bytes)
    # # fileName = 'test.jpg'
    # # exif = get_exif_data(fileName)
    # print exif['GPSInfo']
    # print exif['DateTime']