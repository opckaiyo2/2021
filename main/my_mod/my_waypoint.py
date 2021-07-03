import math
from pyproj import Geod

def waypoint(**location,**goal):
    # gpsと現在地の緯度、経度から距離、方位角、反方位角を求める
    p1_latitude = location["lat"]
    p1_longitude = location["lon"]

    obj_latitude = goal["lat"]
    obj_longitude = goal["lon"]
    obj_altitude = 1000 # 単位は(m)

    g = Geod(ellps='WGS84')

    azimuth, back_azimuth, distance_2d = g.inv(p1_longitude, p1_latitude, obj_longitude, obj_latitude)

    gps = {'azimuth':azimuth,'back_azimuth':back_azimuth,'distance_2d':distance_2d}

    return gps