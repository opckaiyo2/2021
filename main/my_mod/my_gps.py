#coding: utf-8
from typing import Type
from gps3 import gps3

# GPSのデータを取得して還す
def get_gps(sen_data):
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()

    while True:
        try:

            # gps データ取得
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    sen_data['lat'] = data_stream.TPV['lat']
                    sen_data['lon'] = data_stream.TPV['lon']

        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    sen_data = {"x":55}
    get_gps(sen_data)