#coding: utf-8
import numpy as np
import time
import sys

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

class PID_yaw:
    def __init__(self):
        self.M = 0.00
        self.M1 = 0.00

        self.e = 0.00
        self.e1 = 0.00
        self.e2 = 0.00

        self.Kp = 0.001
        self.Ki = 0.01
        self.Kd = 0.5

    def go_yaw(self, goal, data, MV):

        now_yaw = data

        if now_yaw < 0:
            now_yaw = 360 + now_yaw

        if goal < 0:
            goal = 360 + goal

        self.M1 = self.M
        self.e1 = self.e
        self.e2 = self.e1

        if abs(goal - now_yaw) > 180:
            self.e = 360 - abs(goal - now_yaw)
        else:
            self.e = abs(goal - now_yaw)

        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))
        direction = self.roteto(now_yaw,goal)

        # 上限値
        if self.M > 30:
            self.M = 30
        elif self.M < 0:
            self.M = 0

        MV = self.M * direction
        return MV

    #左周りが近いなら-1右周りなら1を返す
    def roteto(self,yaw,goal):
        direction = 0
        if yaw <= 180:
            if 0 > yaw - goal > -180:
                direction = -1
            else:
                direction = 1
        elif yaw <= 360:
            if 0 < yaw - goal < 180:
                direction = 1
            else:
                direction = -1

        return direction

#PID制御で角度調整---------------------------------------------------------------


#PID制御で水深調整---------------------------------------------------------------

class PID_depth:
    def __init__(self):
        self.M = 20.00
        self.M1 = 0.00

        self.e = 0.00
        self.e1 = 0.00
        self.e2 = 0.00

        # self.Kp = 0.1
        # self.Ki = 0.5
        # self.Kd = 10

        self.Kp = 0.5
        self.Ki = 0.003
        self.Kd = 0.01

        # self.Kp = 0.2
        # self.Ki = 0.05
        # self.Kd = 0.05

    def go_depth(self, goal, data, MV):
        # 初期値
        depth_zero = data

        now_depth = self.map_depth((data - depth_zero))
        # print(now_depth)
        # print("barance2:",data["depth"] - depth_zero)

        self.M1 = self.M
        self.e1 = self.e
        self.e2 = self.e1

        self.e = self.map_depth(goal) - now_depth

        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))
        # print(M)
        if self.M > 15:
            self.M = 15
        elif self.M < 0:
            self.M = 0

        MV = self.M
        return MV

    # 圧力センサーの値を(0 ~ 100)に変換
    def map_depth(self, val):
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



if __name__ == '__main__':
    pass
