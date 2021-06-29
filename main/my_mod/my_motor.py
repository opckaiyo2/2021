#coding: utf-8
#! /usr/bin/env python3

import time
import Adafruit_PCA9685
import sys
import configparser

class Motor:

    def __init__(self):
        # コマンド----------------------------------------------
        # set_pwm_freq(周波数Hz)
        # set_pwm(チャンネル番号, パルスのスタート, パルスの終了)　※パルスは1~4000の値を指定することで正転逆転を指定できる
        # ------------------------------------------------------
        # **_pwm　pwmのピン設定
        # **_dir　dirのピン設定
        # **_cor　補正値
        # ------------------------

        self.pwm = Adafruit_PCA9685.PCA9685()
        # pwm周波数設定
        # pwm.set_pwm_freq(66)
        # pwm.set_pwm_freq(500)
        self.pwm.set_pwm_freq(1000)

        # HAT-MDD10ピン設定(チャンネル設定)--------------
        # 新規追加は後ろ側[b]のやつ
        self.xrf_pwm = 7
        self.xrf_dir = 13
        self.xrf_cor = 0.96
        # ---------------
        self.xrb_pwm = 8
        self.xrb_dir = 4
        self.xrb_cor = 0.95
        # ---------------
        self.xlf_pwm = 12
        self.xlf_dir = 6
        self.xlf_cor = 0.99
        # ---------------
        self.xlb_pwm = 11
        self.xlb_dir = 15
        self.xlb_cor = 0.80
        # ---------------
        self.yr_pwm = 9
        self.yr_dir = 14
        self.yr_cor = 1.00
        # ---------------
        self.yl_pwm = 10
        self.yl_dir = 5
        self.yl_cor = 1.00
        # HAT-MDD10ピン設定(チャンネル設定)--------------


    # モータ1個の関数------------------------
    #xx_pwm モータ出力 0~4000
    #xx_dir 回転方向 0 or 4000

    def xrf(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.xrf_pwm, 0, int(val * self.xrf_cor))
        self.pwm.set_pwm(self.xrf_dir, 0, pone)
        # print("xrf:",int(val * xrf_cor),pone)

    def xrb(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.xrb_pwm, 0, int(val * self.xrb_cor))
        self.pwm.set_pwm(self.xrb_dir, 0, pone)
        # print("xrb:",int(val * xrb_cor),pone)

    def xlf(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.xlf_pwm, 0, int(val * self.xlf_cor))
        self.pwm.set_pwm(self.xlf_dir, 0, pone)
        # print("xlf:",int(val * xlf_cor),pone)

    def xlb(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.xlb_pwm, 0, int(val * self.xlb_cor))
        self.pwm.set_pwm(self.xlb_dir, 0, pone)
        # print("xlb:",int(val * xlb_cor),pone)

    def yr(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.yr_pwm, 0, int(val * self.yr_cor))
        self.pwm.set_pwm(self.yr_dir, 0, pone)
        # print("yr:",int(val * yr_cor),pone)

    def yl(self, val):
        val, pone = self.my_map(val)
        self.pwm.set_pwm(self.yl_pwm, 0, int(val * self.yl_cor))
        self.pwm.set_pwm(self.yl_dir, 0, pone)
        # print("yl:",int(val * yl_cor),pone)

    # モータ1個の関数-----------------------------



    # 航行---------------------------------------

    # 前進_後進(go_back)
    def go_back(self, val):
        self.xlf(val)
        self.xrf(-val)
        self.xlb(val)
        self.xrb(-val)

    # 前進_後進(それぞれの出力を指定）
    def go_back_each(self, lf, rf, lb, rb):
        self.xlf(lf)
        self.xrf(-rf)
        self.xlb(lb)
        self.xrb(-rb)

    # 上昇_下降(up_down)  新機体は反転
    def up_down(self, val):
        self.yl(-val)
        self.yr(val)

    # 上昇_下降(それぞれの出力を指定)
    def up_down_each(self, l, r):
        self.yl(l)
        self.yr(-r)

    # 右回り_左回り(spinturn)
    def spinturn(self, val):
        self.xlf(val)
        self.xrf(val)
        self.xlb(val)
        self.xrb(val)


    # 右回り_左回り(それぞれの出力を指定)
    def spinturn_each(self, lf, rf, lb, rb):
        self.xlf(lf)
        self.xrf(rf)
        self.xlb(lb)
        self.xrb(rb)


    # 右傾き_左傾き
    def roll(self, val):
        self.yl(val)
        self.yr(val)

    # 航行---------------------------------------


    # 停止---------------------------------------
    def stop(self):
        # print"\nSTOP"
        self.pwm.set_pwm(self.xrf_pwm, 0, 0)
        self.pwm.set_pwm(self.xrb_pwm, 0, 0)
        self.pwm.set_pwm(self.xlf_pwm, 0, 0)
        self.pwm.set_pwm(self.xlb_pwm, 0, 0)
        self.pwm.set_pwm(self.yr_pwm, 0, 0)
        self.pwm.set_pwm(self.yl_pwm, 0, 0)

    def stop_go_back(self):
        # print"\nSTOP_GO_BACK"
        self.pwm.set_pwm(self.xrf_pwm, 0, 0)
        self.pwm.set_pwm(self.xrb_pwm, 0, 0)
        self.pwm.set_pwm(self.xlf_pwm, 0, 0)
        self.pwm.set_pwm(self.xlb_pwm, 0, 0)

    def stop_up_down(self):
        # print"\nSTOP_UP_DOWN"
        self.pwm.set_pwm(self.yr_pwm, 0, 0)
        self.pwm.set_pwm(self.yl_pwm, 0, 0)
    # 停止---------------------------------------

    # 値変換関数----------------------------------
    # 値変換関数(入力0-100, 出力0-4000)
    def my_map(self, val):
        # val = my_map_half(val)
        if val == 0:
            val = 0
            pone = 1
        elif val >= 0:
            pone = 4000
            in_min = 0
            in_max = 100
            out_min = 0
            out_max = 4000
            val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        else:
            pone = 1
            in_min = 0
            in_max = -100
            out_min = 0
            out_max = 4000
            val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        return val, pone

    # 値変換関数----------------------------------


if __name__ == '__main__':
    pass
