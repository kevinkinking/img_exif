import requests
import exif

def re_geo_coding(gps_info):
    url = 'http://restapi.amap.com/v3/geocode/regeo'
    gps_str = gps_info[1] + ',' + gps_info[0]
    params = {
        'output': 'json',
        'location': gps_str,
        'key': 'c7e65f2e70187ea9a2d7dc3bd08fe752',
        'radius': 5000
    }
    try:
        res_json = requests.post(url, params=params, timeout=3).json()
    except:
        return 402, None, None, None
    if res_json['status'] == '1':
        country = res_json['regeocode']['addressComponent']['country'].encode("UTF-8")
        province = res_json['regeocode']['addressComponent']['province'].encode("UTF-8")
        city = res_json['regeocode']['addressComponent']['city']
        if len(city) > 0:
            city = city.encode("UTF-8")
        else:
            city = province
        return 202, country, province, city

if __name__ == "__main__":
    code, res_dic, img = exif.get_attr_img_from_url('ios.jpg')
    if code == 201:
        gps_info = res_dic['GPSInfo']
        code, country, province, city = re_geo_coding(gps_info)
        if code == 202:
            print country
            print province
            print city
