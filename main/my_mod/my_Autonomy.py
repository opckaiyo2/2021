import sys
import ast
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor

def Autonomy(ard_data, gps_data):

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE)

    gps_flag = inifile.get("operation", "gps_flag")
    gps_initial = inifile.get("operation", "gps_initial")

    gps_initial = ast.literal_eval(gps_initial)

    # 設定ファイル読み込み-------------------------------------------


    motor = Motor()


    # gpsによる初期位置修正----------------------------------------------

    gps_error = 10

    if(gps_flag == 1):
        while(abs(gps_data["lat"]-gps_initial["lat"]) > gps_error or abs(gps_data["lon"]-gps_initial["lon"]) > gps_error):
            if(gps_data["lat"] < (gps_initial["lat"] - gps_error)):
                pass

            elif(gps_data["lat"] > (gps_initial["lat"] + gps_error)):
                pass

            if(gps_data["lon"] < (gps_initial["lon"] - gps_error)):
                pass

            elif(gps_data["lon"] > (gps_data["lon"] + gps_error)):
                pass

    # gpsによる初期位置修正----------------------------------------------


    # gpsによる潜水地点まで----------------------------------------------
    # gpsによる潜水地点まで----------------------------------------------


    # 潜水--------------------------------------------------------------
    # 潜水--------------------------------------------------------------


    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----
    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----


    # Uターン-----------------------------------------------------------
    # Uターン-----------------------------------------------------------


    # 潜水--------------------------------------------------------------
    # 潜水--------------------------------------------------------------


    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----
    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----


    # gpsによって初期位置へ----------------------------------------------
    # gpsによって初期位置へ----------------------------------------------