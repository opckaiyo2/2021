import math
from pyproj import Geod

def waypoint(**gps):
    # gpsと現在地の緯度、経度から距離、方位角、反方位角を求める
    p1_latitude = gps["s_lat"]
    p1_longitude = gps["s_lon"]

    obj_latitude = gps["g_lat"]
    obj_longitude = gps["g_lon"]

    g = Geod(ellps='WGS84')

    azimuth, back_azimuth, distance_2d = g.inv(p1_longitude, p1_latitude, obj_longitude, obj_latitude)

    gps = {'azimuth':azimuth,'back_azimuth':back_azimuth,'distance_2d':distance_2d}

    return gps