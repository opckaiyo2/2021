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

    gps_initial = inifile.get("operation", "gps_initial")
    gps_diving = inifile.get("operation", "gps_diving")
    gps_ascend = inifile.get("operation", "gps_ascend")
    speed = inifile.get("operation", "defalut_speed")
    depth = inifile.get("operation", "depth")

    ava_rot = inifile.get("autonomy","ava_rot")

    gps_initial = ast.literal_eval(gps_initial)
    gps_diving = ast.literal_eval(gps_diving)
    gps_ascend = ast.literal_eval(gps_ascend)
    # 設定ファイル読み込み-------------------------------------------


    pid_yaw = PID_yaw()
    pid_depth = PID_depth()
    motor = Motor()


    # gpsによる初期位置修正----------------------------------------------
    while(True):
        # gpsとconfig.iniの初期位置比較
        gps = waypoint(sen_data["lat"], sen_data["lon"],
                    gps_initial["lat"], gps_initial["lon"])
        
        # 初期位置との誤差が2mいないだったら位置調整終了(gps_datasheetより誤差2m)
        if(gps["distance_2d"] < 2):
            motor.stop_go_back()
            break
        
        # まずは角度調整,角度調節せず直進すると明後日の方向に
        while(True):
            if((gps["azimuth"]-sen_data["yaw"]) < 5):
                motor.stop()
                break

            # 方位角とオイラー角を合わせないといけない
            MV = pid_yaw.go_yaw(gps["azimuth"],sen_data["yaw"])
            motor.spinturn(MV)

        # 直進 進む強さは電流計の値を見て調整できるようにしたい
        MV = pid_yaw.go_yaw(0,sen_data["yaw"])
        motor.go_back_each(speed-MV,speed+MV,speed,speed)
    # gpsによる初期位置修正----------------------------------------------


    # senser,pidを用いた初期向き設定---------------------------------
    # gpsによる初期位置修正で傾いた角度を修正
    while(True):
        MV = pid_yaw.go_yaw(0,sen_data["yaw"])

        if(sen_data["yaw"] < 5):
            motor.stop()
            break

        motor.spinturn(MV)
    # senser,pidを用いた初期向き設定---------------------------------


    # gpsによる潜水地点まで----------------------------------------------
    while(True):
        # gpsとconfig.iniの潜水位置比較
        gps = waypoint(sen_data["lat"], sen_data["lon"],
                    gps_diving["lat"], gps_diving["lon"])
        
        # 潜水位置との誤差が2mいないだったら位置調整終了(gps_datasheetより誤差2m)
        if(gps["distance_2d"] < 2):
            motor.stop_go_back()
            break
        
        # まずは角度調整,角度調節せず直進すると明後日の方向に
        while(True):
            if((gps["azimuth"]-sen_data["yaw"]) < 5):
                motor.stop()
                break

            MV = pid_yaw.go_yaw(gps["azimuth"],sen_data["yaw"])
            motor.spinturn(MV)

        # 直進 進む強さは電流計の値を見て調整できるようにしたい
        MV = pid_yaw.go_yaw(0,sen_data["yaw"])
        motor.go_back_each(speed-MV,speed+MV,speed,speed)
    # gpsによる潜水地点まで----------------------------------------------


    # 潜水--------------------------------------------------------------
    while(True):
        MV = pid_depth.go_depth(depth,sen_data("depth"))

        # datasheetの分解能から記入したい(0.2)
        if(abs(depth-sen_data) < 0.2):
            break
    # 潜水--------------------------------------------------------------


    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----
    while(True):
        for i in range(4):
            rot[i] = int(sen_data["rot"+str(i)])
        
        ava = sum(rot) / len(rot)

        if(ava > ava_rot):
            motor.stop_go_back()
            break

        MV = pid_depth.go_depth(depth,sen_data["depth"])
        motor.up_down(MV)
    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----


    # Uターン-----------------------------------------------------------
    # Uターン-----------------------------------------------------------


    # 潜水--------------------------------------------------------------
    # 潜水--------------------------------------------------------------


    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----
    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----


    # gpsによって初期位置へ----------------------------------------------
    # gpsによって初期位置へ----------------------------------------------
