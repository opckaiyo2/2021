import sys
import ast
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor
# gpsのデータから目的地までの角度と距離の差異を計算する
from my_waypoint import waypoint
# pid制御
from my_balance import PID_yaw,PID_depth

def Autonomy(sen_data):

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE)

    gps_flag = inifile.get("operation", "gps_flag")
    gps_initial = inifile.get("operation", "gps_initial")

    gps_initial = ast.literal_eval(gps_initial)

    pid_flag = inifile.get("operation", "pid_flag")

    # 設定ファイル読み込み-------------------------------------------


    pid_yaw = PID_yaw()
    pid_depth = PID_depth()
    motor = Motor()


    # gpsによる初期位置修正----------------------------------------------

    if(gps_flag):
        while(True):
            gps = waypoint(sen_data["lat"], sen_data["lon"],
                        gps_initial["lat"], gps_initial["lon"])
            if(gps["distance_2d"] < 10):
                break

    # gpsによる初期位置修正----------------------------------------------


    # senser,pidを用いた初期向き設定---------------------------------

    if(pid_flag):
        while(True):
            pid_yaw.go_yaw()

    # senser,pidを用いた初期向き設定---------------------------------


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
