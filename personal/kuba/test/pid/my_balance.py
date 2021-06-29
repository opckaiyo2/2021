#coding: utf-8
import numpy as np
import time
import sys
sys.path.append("/kaiyo/my_mod")
from my_get_serial import get_data, send_data
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each


# 単体で実行するために必要(mainから呼ばれたときは関係ない)---------
import serial
import ast
from multiprocessing import Manager, Process
# ArduinoMEGAとpinで接続---------
# ArduinoMEGAとpinで接続
# ser = serial.Serial('/dev/ttyS0',  115200, timeout=3)
# ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0',  9600, timeout=3)
# ArduinoMEGAとpinで接続---------
# 単体で実行するために必要(mainから呼ばれたときは関係ない)---------

#PID制御で角度調整---------------------------------------------------------------

# M : 与える操作量
# M1 : 一つ前に与えた操作量
# goal : 目的値
# e : 偏差(目的値と現在値の差)
# e1 : 前回に与えた偏差
# e2 : 前々回に与えた偏差
# Kp : 比例制御（P制御)の比例定数
# Ki : 積分制御（I制御)の比例定数
# Kd : 微分制御（D制御)の比例定数

def go_yaw(goal,data,MV):
    while True:
        M = 0.00
        M1 = 0.00

        e = 0.00
        e1 = 0.00
        e2 = 0.00

        Kp = 0.001
        Ki = 0.01
        Kd = 0.5

        now_yaw = data["yaw"]

        if now_yaw < 0:
            now_yaw = 360 + now_yaw

        if goal.value < 0:
            goal.value = 360 + goal.value

        while True:

            now_yaw = data["yaw"]

            M1 = M
            e1 = e
            e2 = e1

            if now_yaw < 0:
                now_yaw = 360 + now_yaw

            if abs(goal.value - now_yaw) > 180:
                e = 360 - abs(goal.value - now_yaw)
            else:
                e = abs(goal.value - now_yaw)

            M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
            direction = roteto(now_yaw,goal)

            # 上限値
            if M > 30:
                M = 30
            elif M < 0:
                M = 0

            # PIDの値を降りてくるようにしてないから落とす(この場合3度以内なので許容誤差1度)
            if goal.value != 0:
                if now_yaw - 1 < goal.value < now_yaw + 1:
                    MV.value = 0
                    break
            else:
                if now_yaw > 359 or now_yaw < 1:
                    MV.value = 0
                    break

            MV.value = M * direction
            time.sleep(0.4)
    # stop()

#左周りが近いなら-1右周りなら1を返す
def roteto(yaw,goal):
    direction = 0
    if yaw <= 180:
        if 0 > yaw - goal.value > -180:
            direction = -1
        else:
            direction = 1
    elif yaw <= 360:
        if 0 < yaw - goal.value < 180:
            direction = 1
        else:
            direction = -1

    return direction

#PID制御で角度調整---------------------------------------------------------------


#PID制御で水深調整---------------------------------------------------------------

def go_depth(goal,data,depth_mv):
    # 初期値
    depth_zero = data["depth"]
    # print("depth_zero:",depth_zero)
    while True:
        M = 20.00
        M1 = 0.00

        e = 0.00
        e1 = 0.00
        e2 = 0.00

        # Kp = 0.1
        # Ki = 0.5
        # Kd = 10

        Kp = 0.5
        Ki = 0.003
        Kd = 0.01

        # Kp = 0.2
        # Ki = 0.05
        # Kd = 0.05


        # now_depth = map_depth(data["depth"])

        while True:

            now_depth = map_depth((data["depth"] - depth_zero))
            # print(now_depth)
            # print("barance2:",data["depth"] - depth_zero)

            M1 = M
            e1 = e
            e2 = e1

            e = map_depth(goal.value) - now_depth

            M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
            # print(M)
            if M > 15:
                M = 15
            elif M < 0:
                M = 0

            # if now_depth + 0.2 < goal.value < now_depth - 0.2:
            #     break
            depth_mv.value = M
            time.sleep(0.2)
    # stop()

# 圧力センサーの値を(0 ~ 100)に変換
def map_depth(val):
    """
    2018年のパラメータ参考になるか分からん
    # # 海での値(波の上)
    # # in_min = 0.6
    # # in_max = 10
    # # 宜野湾
    # # in_min = 0.6
    # # in_max = 7.6
    # # 小学校プール
    # in_min = 1.5
    # in_max = 6

    """
    # ポリテクプール
    # in_min = 0.0
    # in_max = 0.3

    # 海
    in_min = 0.0
    in_max = 3.0

    # プールでの値
    # in_min = 2
    # in_max = 7

    if val <= in_min: val = in_min
    if val >= in_max: val = in_max

    in_min = in_min
    in_max = in_max
    out_min = 0
    out_max = 100
    val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    # print("map",val)
    return int(val)

#PID制御で水深調整---------------------------------------------------------------

# 単体で実行するためにサブプロセスでデータ通信を行っている(mainから呼ばれたときは関係ない)
if __name__ == '__main__':
    while True:
        try:
            print("send:reboot")
            send_data("reboot")
            # time.sleep(1)
            val = ser.readline()
            # print(val)
            val = ast.literal_eval(val.decode('unicode-escape'))
            if val["time"] <= 10.0:
                # time.sleep(1)
                break

        except SyntaxError:
            print("barance : Reception Error!!\n")
        except TimeoutError:
            print("barance : timeout Error!\n")

    with Manager() as manager:
        print("OK")
        #センサーのdata
        data = manager.dict()
        #yawの操作量
        yaw_MV = manager.Value("d", 0.0)
        # goal_yawの目標値
        goal_yaw = manager.Value("i", 0)

        try:
            val = ser.readline()
            val = ast.literal_eval(val.decode('unicode-escape'))
            # print (val)
        except SyntaxError:
            # 受信エラー
            print("main : Reception Error!!")

        # 受信データの大きさに合わせる
        for i in val:
            data[i] = val[i]

        get_data = Process(target=get_data, args=[data])
        go_yaw = Process(target=go_yaw,  args=[goal_yaw, data, yaw_MV])

        get_data.start()
        go_yaw.start()

        m_val = 15

        while True:
            try:
                # t1 = time.time()

                # go_yaw確認用-------------------------------

                print(data["time"], data["yaw"],"yaw_MV :",  yaw_MV.value,  "\n")
                # その場で補正
                # spinturn(yaw_MV.value)

                # 前進しながら補正
                if ( yaw_MV.value >= 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)
                elif ( yaw_MV.value < 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)

                # go_yaw確認用-------------------------------

                # t2 = time.time()
                # print("time : ",t2 - t1)
                # print("何もない")
                time.sleep(0.2)
                pass
            except KeyboardInterrupt as e:
                stop()
                break
