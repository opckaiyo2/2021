#coding: utf-8
#! /usr/bin/env python3


import time
import Adafruit_PCA9685
import sys
import configparser

sys.path.append("/kaiyo/test")

INI_FILE = '/kaiyo/my_config/my_config.ini'
# from my_state_write import state_write

# ArduinoMegaとシリアル通信してセンサデータをもらう関数
from my_get_serial import get_data, send_data

#設定ファイル読み込み(モータ補正値)------------------
inifile = configparser.SafeConfigParser()
inifile.read(INI_FILE)

rot0_cor = inifile.getfloat('set_mode', 'rot0_cor')
rot1_cor = inifile.getfloat('set_mode', 'rot1_cor')
rot2_cor = inifile.getfloat('set_mode', 'rot2_cor')
rot3_cor = inifile.getfloat('set_mode', 'rot3_cor')
# ---------------------------------------------

# コマンド----------------------------------------------
# set_pwm_freq(周波数Hz)
# set_pwm(チャンネル番号, パルスのスタート, パルスの終了)　※パルスは1~4000の値を指定することで正転逆転を指定できる
# ------------------------------------------------------
# **_pwm　pwmのピン設定
# **_dir　dirのピン設定
# **_cor　補正値
# ------------------------



pwm = Adafruit_PCA9685.PCA9685()
# pwm周波数設定
# pwm.set_pwm_freq(66)
# pwm.set_pwm_freq(500)
pwm.set_pwm_freq(1000)

# HAT-MDD10ピン設定(チャンネル設定)--------------
# 新規追加は後ろ側[b]のやつ
xrf_pwm = 7
xrf_dir = 13
xrf_cor = 0.96
# ---------------
xrb_pwm = 8
xrb_dir = 4
xrb_cor = 0.95
# ---------------
xlf_pwm = 12
xlf_dir = 6
xlf_cor = 0.99
# ---------------
xlb_pwm = 11
xlb_dir = 15
xlb_cor = 0.80
# ---------------
yr_pwm = 9
yr_dir = 14
yr_cor = 1.00
# ---------------
yl_pwm = 10
yl_dir = 5
yl_cor = 1.00
# HAT-MDD10ピン設定(チャンネル設定)--------------


# モータ1個の関数------------------------
#xx_pwm モータ出力 0~4000
#xx_dir 回転方向 0 or 4000

def xrf( val ):
    val, pone = my_map(val)
    pwm.set_pwm(xrf_pwm, 0, int(val * xrf_cor))
    pwm.set_pwm(xrf_dir, 0, pone)
    # print("xrf:",int(val * xrf_cor),pone)

def xrb( val ):
    val, pone = my_map(val)
    pwm.set_pwm(xrb_pwm, 0, int(val * xrb_cor))
    pwm.set_pwm(xrb_dir, 0, pone)
    # print("xrb:",int(val * xrb_cor),pone)

def xlf( val ):
    val, pone = my_map(val)
    pwm.set_pwm(xlf_pwm, 0, int(val * xlf_cor))
    pwm.set_pwm(xlf_dir, 0, pone)
    # print("xlf:",int(val * xlf_cor),pone)

def xlb( val ):
    val, pone = my_map(val)
    pwm.set_pwm(xlb_pwm, 0, int(val * xlb_cor))
    pwm.set_pwm(xlb_dir, 0, pone)
    # print("xlb:",int(val * xlb_cor),pone)

def yr( val ):
    val, pone = my_map(val)
    pwm.set_pwm(yr_pwm, 0, int(val * yr_cor))
    pwm.set_pwm(yr_dir, 0, pone)
    # print("yr:",int(val * yr_cor),pone)

def yl( val ):
    val, pone = my_map(val)
    pwm.set_pwm(yl_pwm, 0, int(val * yl_cor))
    pwm.set_pwm(yl_dir, 0, pone)
    # print("yl:",int(val * yl_cor),pone)

# モータ1個の関数-----------------------------



# 航行---------------------------------------

# 前進_後進(go_back)
def go_back( val ):
    xlf(val)
    xrf(-val)
    xlb(val)
    xrb(-val)

# 前進_後進(それぞれの出力を指定）
def go_back_each( lf, rf, lb, rb ):
    xlf(lf)
    xrf(-rf)
    xlb(lb)
    xrb(-rb)

# 上昇_下降(up_down)  新機体は反転
def up_down( val ):
    yl(-val)
    yr(val)

# 上昇_下降(それぞれの出力を指定)
def up_down_each( l, r ):
    yl(l)
    yr(-r)

# 右回り_左回り(spinturn)
def spinturn( val ):
    xlf(val)
    xrf(val)
    xlb(val)
    xrb(val)


# 右回り_左回り(それぞれの出力を指定)
def spinturn_each( lf, rf, lb, rb ):
    xlf(lf)
    xrf(rf)
    xlb(lb)
    xrb(rb)


# 右傾き_左傾き
def roll( val ):
    yl(val)
    yr(val)

#全て回す
def allspin(val);
    xlf(val)
    xrf(val)
    xlb(val)
    xrb(val)
    yl(val)
    yr(val)

# 航行---------------------------------------


# 停止---------------------------------------
def stop():
    # print"\nSTOP"
    pwm.set_pwm(xrf_pwm, 0, 0)
    pwm.set_pwm(xrb_pwm, 0, 0)
    pwm.set_pwm(xlf_pwm, 0, 0)
    pwm.set_pwm(xlb_pwm, 0, 0)
    pwm.set_pwm(yr_pwm, 0, 0)
    pwm.set_pwm(yl_pwm, 0, 0)

def stop_go_back():
    # print"\nSTOP_GO_BACK"
    pwm.set_pwm(xrf_pwm, 0, 0)
    pwm.set_pwm(xrb_pwm, 0, 0)
    pwm.set_pwm(xlf_pwm, 0, 0)
    pwm.set_pwm(xlb_pwm, 0, 0)

def stop_up_down():
    # print"\nSTOP_UP_DOWN"
    pwm.set_pwm(yr_pwm, 0, 0)
    pwm.set_pwm(yl_pwm, 0, 0)


# 停止---------------------------------------

# 値変換関数----------------------------------
# 値変換関数(入力0-100, 出力0-4000)
def my_map(val):
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


# 設定ファイルの特定の項目を書き換える---------------
def ini_set(section, key, value):
    global INI_FILE
    inifile.set(section, key, value)
    f = open(INI_FILE, "w")
    inifile.write(f)
    f.close()

# 設定ファイルの特定の項目を書き換える---------------


# ---LOG-----モータ----チューニング--------
#   rot0   :   XR   :   xr_time
#   rot1   :   XL   :   xl_time
#   rot2   :   YL   :   yl_time
#   rot3   :   YR   :   yr_time
# --------------------------------------


# ロータリーエンコーダの値を基準に1000回転したときの終了時間が「左右・上下」の組み合わせで同じになるよう(0.02以下)に補正パラメータを変更する
# iniのコメントとか改行消えるので注意
def motor_tuning():
    global xr_cor, xl_cor, yr_cor, yl_cor   # 各モータに対応する補正値
    flag = [True] * 7   # 一回だけ実行するためのフラグ
    fix_flag = True     # 出力の強いモータを調べるために使うフラグ
    rool = 100          # 回転数
    val = 30            # dety比(モータ出力)
    eta = 0.02          # 学習率
    goal = 0.02         # 目標誤差
    t0 = time.perf_counter()    # スタート時間

    while(True):

        if flag[0] == True:
        # 値のリセットが完了するまで待機--------------------------------
            while True:
                stop()
                send_data("reboot")
                time.sleep(1)

                data = get_data("all")
                rot0 = data["rot0"]
                rot1 = data["rot1"]
                rot2 = data["rot2"]
                rot3 = data["rot3"]
                print(t0,rot0,rot1,rot2,rot3)
                if(rot0 == 0 and rot1 == 0 and rot2 == 0 and rot3 == 0):
                    print("start")
                    flag[0] = False
                    start_time = time.perf_counter()    # スタート時間
                    xl(val)
                    xr(-val)
                    yl(val)
                    yr(-val)
                    break
                else:
                    print("reboot")
        # 値のリセットが完了するまで待機-------------------------------

        data = get_data("all")
        rot0 = data["rot0"]
        rot1 = data["rot1"]
        rot2 = data["rot2"]
        rot3 = data["rot3"]

        # 各モータごとに指定の回転回数を超えたか判定-----------------
        if rot0 >= rool:
            if flag[1] == True:
                xr(0)
                xr_time = time.perf_counter()
                print("rot0_time : ",xr_time - start_time)
                flag[1] = False
            else:
                pass

        if rot1 >= rool:
            if flag[2] == True:
                xl(0)
                xl_time = time.perf_counter()
                print("rot1_time : ",xl_time - start_time)
                flag[2] = False
            else:
                pass

        if rot2 >= rool:
            if flag[3] == True:
                yl(0)
                yl_time = time.perf_counter()
                print("rot2_time : ",yl_time - start_time)
                flag[3] = False
            else:
                pass

        if rot3 >= rool:
            if flag[4] == True:
                yr(0)
                yr_time = time.perf_counter()
                print("rot3_time : ",yr_time - start_time)
                flag[4] = False
            else:
                pass

        # 各モータごとに指定の回転回数を超えたか判定-----------------

        # すべてのモータ回転終了
        if(rot0 >= rool and rot1 >= rool and rot2 >= rool and rot3 >= rool):
            print(rot0, rot1, rot2, rot3)
            print("time_dif go: ",XR_time-t3)
            print("time_dif up: ",yl_time-yr_time)

            # モータをひとつ固定してもう一方を調整(今のままだと補正値1.0超える)----
            if (XR_time - xl_time) >= goal: # 0.02以上
                xr_cor += eta
            elif (XR_time - xl_time) <= -goal: # -0.02以下
                xr_cor -= eta
            else:
                print("go_back_OK")
                flag[5] = False

            if (yl_time - yr_time) >= goal:
                yl_cor += eta
            elif (yl_time - yr_time) <= -goal:
                yl_cor -= eta
            else:
                print("up_down_OK")
                flag[6] = False
            # モータをひとつ固定してもう一方を調整(今のままだと補正値1.0超える)----

            print(xr_cor, xl_cor, yl_cor, yr_cor)
            # モータ終了時間の差が指定時間(0.02)以内
            if (flag[5] == False and flag[6] == False):
                print("end")
                break
            else:   #もう一度
                flag = [True] * 7

    t6 = time.perf_counter()
    print("all_time : ",t6 - t0)
    ini_set('set_mode', 'rot0_cor' , str(xr_cor))
    ini_set('set_mode', 'rot1_cor' , str(xl_cor))
    ini_set('set_mode', 'rot2_cor' , str(yl_cor))
    ini_set('set_mode', 'rot3_cor' , str(yr_cor))
    print(xr_cor, xl_cor, yl_cor, yr_cor)
    return True

if __name__ == '__main__':
    end = False

    while True:
        try:
            end = motor_tuning()
            if end == True:break

        except KeyboardInterrupt as e:
            stop()
            break
