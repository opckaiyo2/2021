#coding: utf-8
import math
from pyproj import Geod

def waypoint(s_lat,s_lon,g_lat,g_lon):
    # gpsと現在地の緯度、経度から距離、方位角、反方位角を求める

    g = Geod(ellps='WGS84')
    azimuth, back_azimuth, distance_2d = g.inv(
        s_lat, s_lon, g_lat, g_lon)

    gps = {'azimuth': azimuth, 'back_azimuth': back_azimuth,
        'distance_2d': distance_2d}

    return gps
