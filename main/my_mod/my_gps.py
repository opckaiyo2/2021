#coding: utf-8
import serial
import gps
import ast
import time

# GPSのデータを取得して還す
def get_gps(sen_data):
    ser = serial.Serial("/dev/ttyACM0",115200,timeout=1)
    lat = ""
    lon = ""
    alt = ""
    while True:
        try:

            # gps データ取得
            str = ser.readline().decode('unicode-escape')
            print(str)
            print(type(str))

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