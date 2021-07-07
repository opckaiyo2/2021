#coding: utf-8
import math
from pyproj import Geod

def waypoint(s_lat,s_lon,g_lat,g_lon):
    # gps�ƌ��ݒn�̈ܓx�A�o�x���狗���A���ʊp�A�����ʊp�����߂�

    g = Geod(ellps='WGS84')
    azimuth, back_azimuth, distance_2d = g.inv(
        s_lat, s_lon, g_lat, g_lon)

    gps = {'azimuth': azimuth, 'back_azimuth': back_azimuth,
        'distance_2d': distance_2d}

    return gps
