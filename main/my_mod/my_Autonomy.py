#coding: utf-8
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
# オペレートファンクション-制御関数
from my_operatfunction import OF

def Autonomy(sen_data):

    of = OF()

    # gpsによる初期位置修正----------------------------------------------
    of.gps_position("initial",sen_data)
    # gpsによる初期位置修正----------------------------------------------


    # senser,pidを用いた初期向き設定---------------------------------
    # gpsによる初期位置修正で傾いた角度を修正
    of.rotate_yaw(0,sen_data)
    # senser,pidを用いた初期向き設定---------------------------------


    # gpsによる潜水地点まで----------------------------------------------
    of.gps_position("diving",sen_data)
    # gpsによる潜水地点まで----------------------------------------------


    # 潜水--------------------------------------------------------------
    of.diving(sen_data)
    # 潜水--------------------------------------------------------------


    # motor回転数によって潜航(浮上しgpsで目的地じゃなければ潜水しなおし)----
    for i in range(4):
        rot[i] = int(sen_data["rot"+str(i)])
    
    rot_sum = sum(rot)

    # 潜水しながら深さpid
    while(True):
        for i in range(4):
            rot[i] = int(sen_data["rot"+str(i)])
        
        ava = (sum(rot)-rot_sum) / len(rot)

        if(ava > ava_rot):
            motor.stop_go_back()
            break

        motor.go_back(speed)

        MV = pid_depth.go_depth(depth,sen_data["depth"])
        motor.up_down(MV)

    # 浮上
    while(True):
        MV = pid_depth.go_depth(begin_depth,sen_data["depth"])

        # datasheetの分解能から記入したい(0.2)
        if(abs(begin_depth-sen_data) < 0.2):
            motor.stop_up_down()
            break

        motor.up_down(MV)

    # gpsで位置比較 目的地でないとき再び潜水
    while(True):
        gps = waypoint(sen_data["lat"],sen_data["lon"],gps_ascend["lat"],gps_ascend["lon"])
        if(gps["distance_2d"] < 2):
            break

        while(True):
            MV = pid_depth.go_depth(depth,sen_data("depth"))

            # datasheetの分解能から記入したい(0.2)
            if(abs(depth-sen_data["depth"]) < 0.2):
                break

        for i in range(4):
            rot[i] = int(sen_data["rot"+str(i)])

        rot_sum = sum(rot)

        while(True):
            for i in range(4):
                rot[i] = int(sen_data["rot"+str(i)])

            ava = (sum(rot)-rot_sum) / len(rot)

            if(ava > re_rot):
                motor.stop_go_back()
                break

            motor.go_back(speed)

            MV = pid_depth.go_depth(depth,sen_data["depth"])
            motor.up_down(MV)

        while(True):
            MV = pid_depth.go_depth(begin_depth,sen_data["depth"])

            # datasheetの分解能から記入したい(0.2)
            if(abs(begin_depth-sen_data) < 0.2):
                motor.stop_up_down()
                break

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
