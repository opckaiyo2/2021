#coding: utf-8
from datetime import datetime
import gps
import ast
import time

# GPSのデータを取得して還す
def get_gps(sen_data):
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    lat = ""
    lon = ""
    alt = ""
    while True:
        try:

            # gps データ取得
            report = next(session)
            # print(report)
            if report['class'] == 'TPV':
                if hasattr(report, 'lat'):
                    lat = float(report.lat)
                if hasattr(report, 'lon'):
                    lon = float(report.lon)
                if hasattr(report, 'alt'):
                    alt = float(report.alt)
                if( lat!=""and lon!="" and alt!="" ):
                    gps_data_dict = {"lat":lat, "lng":lon, "alt":alt}
                    sen_data.update(gps_data_dict)
        except KeyError:
                pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print("\n")
            print("my_gps.py get_gps try error : GPSD has terminated!!")
            print("\n")