#coding: utf-8
import configparser
#from personal.kuba.test.serial.my_get_serial import String_data
import select
import serial
import tty
import sys
import ast
import gps

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor

def Manual():
    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    # key入力かプロボか
    # モータ回転数をteaching用データとして出力するか
    
    # 設定ファイル読み込み-------------------------------------------


    # key入力で制御する場合------------------------------------------
    tty.setcbreak(sys.stdin.fileno())

    ser = serial.Serial('/dev/ttyACM0', 9600)

    motor = Motor()
    power = 10

    while(True):
        String_data = ser.readline().decode('utf-8').rstrip()
        dict_data = ast.literal_eval(String_data)

        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        lat = ""
        lon = ""
        alt = ""

        report = next(session)
        if report['class'] == 'TPV':
            if hasattr(report, 'lat'):
                lat = float(report.lat)
            if hasattr(report, 'lon'):
                lon = float(report.lon)
            if hasattr(report, 'alt'):
                alt = float(report.alt)
            if( lat!=""and lon!="" and alt!="" ):
                gps_data_dict = {"lat":lat, "lng":lon, "alt":alt}
                dict_data.update(gps_data_dict)

        if select.select([sys.stdin],[],[],0) == ([sys.stdin],[],[]):
            input_key = sys.stdin.read(1)

            if input_key == "w":
                motor.go_back(power)
                print("motor.go_back : ",power)
            elif input_key == "s":
                motor.go_back(power*-1)
                print("motor.go_back : ",power*-1)
            elif input_key == "u":
                motor.up_down(power)
                print("motor.up_down : ",power)
            elif input_key == "d":
                motor.up_down(power*-1)
                print("motor.up_down : ",power*-1)
            elif input_key == "q":
                motor.spinturn(power)
                print("motor.spinturn : ",power)
            elif input_key == "e":
                motor.spinturn(power*-1)
                print("motor.spinturn : ",power*-1)
            elif input_key == "+":
                power += 10
                print("motor power up: ",power)
            elif input_key == "-":
                power -= 10
                print("motor power down: ",power)
            elif input_key == "p":
                print(dict_data)

    # key入力で制御する場合------------------------------------------


    # プロボで操作する場合--------------------------------------------
    # プロボで操作する場合--------------------------------------------