#coding: utf-8
import sys
import time
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor
from my_operatfunction import OF

def Teaching(sen_data):

    of = OF()
    motor = Motor()

    # データがすべて揃うまでループ endtimeはデータの一番後列
    while(not('endtime' in sen_data)):
        pass

    # 初期向きの暗記
    while(True):
        ini_x = sen_data["x"]
        if(abs(ini_x) > 0.1):
            break

    # 初期向きの反対(Uターンなどで使う)
    ini_opx = 0

    if ini_x < 180:
        ini_opx = ini_x+180
    else:
        ini_opx = ini_x-180

    print("初期方位 : "+str(ini_x))
    print("Uターン後PID方位 : "+str(ini_opx))
    print("\n")

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.ConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    # どのデータを読み込むか
    rotate = eval(inifile.get("teaching","rotate"))
    print("モータ(前進後進に関係ある4つ)の回転数合計")
    print("潜水位置まで\t"+str(rotate[0])+"回転")
    print("潜水中　途中浮上位置まで\t"+str(rotate[1])+"回転")
    print("潜水中　Uターン場所まで\t"+str(rotate[2])+"回転")
    print("潜水中　途中浮上位置まで\t"+str(rotate[3])+"回転")
    print("スタート位置まで\t"+str(rotate[4])+"回転\n\n")

    # 設定ファイル読み込み-------------------------------------------


    # log再生------------------------------------------------------


    # 潜水位置まで-------------------------------------------------
    print("\n\n潜水位置まで")
    of.rotate_advance(rotate[0],ini_x,sen_data)
    # 潜水位置まで-------------------------------------------------

    # 潜水位置まで潜水---------------------------------------------
    print("\n\n潜水")
    of.diving(sen_data)
    # 潜水位置まで潜水---------------------------------------------

    # 潜航　途中浮上位置まで--------------------------------------
    print("\n途中浮上位置まで")
    of.diving_advance(rotate[1],ini_x,sen_data)
    # 潜航　途中浮上位置まで--------------------------------------

    # 途中浮上---------------------------------------------------
    print("\n\n途中浮上")
    of.ascend(sen_data)
    time.sleep(5)
    # 途中浮上---------------------------------------------------

    # 潜水位置まで潜水---------------------------------------------
    print("\n潜水")
    of.diving(sen_data)
    # 潜水位置まで潜水---------------------------------------------

    # 浮上位置まで------------------------------------------------
    print("\n浮上位置まで")
    of.diving_advance(rotate[2],ini_x,sen_data)
    # 浮上位置まで------------------------------------------------

    # 浮上-------------------------------------------------------
    print("\n\n浮上")
    of.ascend(sen_data)
    time.sleep(5)
    # 浮上-------------------------------------------------------

    # Uターン----------------------------------------------------
    print("\nUターン")
    #of.rotate_yaw(ini_opx,sen_data)
    # Uターン----------------------------------------------------

    ini_opx = sen_data["x"]

    # 潜水位置まで-------------------------------------------------
    print("\n潜水位置まで")
    of.rotate_advance(rotate[3],ini_opx,sen_data)
    # 潜水位置まで-------------------------------------------------

    # 潜水位置まで潜水---------------------------------------------
    print("\n\n潜水")
    of.diving(sen_data)
    # 潜水位置まで潜水---------------------------------------------

    # 浮上位置まで------------------------------------------------
    print("\n浮上位置まで")
    of.diving_advance(rotate[4],ini_opx,sen_data)
    # 浮上位置まで------------------------------------------------

    # 浮上-------------------------------------------------------
    print("\n\n浮上")
    of.ascend(sen_data)
    time.sleep(5)
    # 浮上-------------------------------------------------------

    # スタート位置まで--------------------------------------------
    print("\nスタート位置まで")
    of.rotate_advance(rotate[5],ini_opx,sen_data)
    print("\n")
    # スタート位置まで--------------------------------------------

    # すべてのモータstop
    motor.stop()

    # log再生------------------------------------------------------

if __name__ == "__main__":
    Teaching()
