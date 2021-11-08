#coding: utf-8
import sys
import time
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/tinou/main/my_mod")
# motor制御
from my_motor import Motor
from my_operatfunction import OF

def Teaching(sen_data,cap_flag,X,Y,S):

    of = OF()
    motor = Motor()
    
    # データがすべて揃うまでループ endtimeはデータの一番後列
    while(not('endtime' in sen_data)):
        pass

    # 初期向きの暗記
    ini_x = sen_data["x"]

    # 初期向きの反対(Uターンなどで使う)
    ini_opx = 0

    if ini_x < 180:
        ini_opx = ini_x+180
    elif ini_x > 180:
        ini_opx = ini_x-180
    else:
        ini_opx = (ini_x+180) % 360

    print(ini_x)
    print(ini_opx)
    print("\n")

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/tinou/main/config/config.ini"
    inifile = configparser.ConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    # どのデータを読み込むか
    rotate = eval(inifile.get("teaching","rotate"))
    print("モータ(前進後進に関係ある4つ)の回転数合計")
    print("潜水位置まで\t"+str(rotate[0])+"回転")
    print("潜水中　浮上位置まで\t"+str(rotate[1])+"回転")
    print("Uターンあと　潜水位置まで\t"+str(rotate[2])+"回転")
    print("潜水中　浮上位置まで\t"+str(rotate[3])+"回転")
    print("スタート位置まで\t"+str(rotate[4])+"回転\n\n")

    # 設定ファイル読み込み-------------------------------------------


    # log再生------------------------------------------------------
    
    # 潜水位置まで潜水(1m)---------------------------------------------
    print("潜水 1m")
    of.diving2(0,sen_data)
    # -------------------------------------------------------------- 

    # 潜航　15m------------------------------------------------------
    print("潜航　15m")
    of.diving_advance(rotate[0],ini_opx,sen_data)
    # --------------------------------------------------------------  
    
    # 潜水位置まで潜水(2m)---------------------------------------------
    print("潜水 2m")
    of.diving2(0,sen_data)
    # -------------------------------------------------------------- 
    
    # 潜航　30m------------------------------------------------------
    print("潜航　30m")
    of.diving_advance2(rotate[1],ini_opx,sen_data,cap_flag)
    # -------------------------------------------------------------- 

    #画像処理を使った潜航---------------------------------------------
    print("カメラ潜航")
    of.camera_advance(sen_data,X,Y,S)
    #---------------------------------------------------------------

    #ランドマークで5秒停止--------------------------------------------
    print("sleep")
    time.sleep(4)
    #---------------------------------------------------------------

    # Uターン----------------------------------------------------
    print("Uターン")
    of.rotate_yaw(ini_opx,sen_data)
    # -----------------------------------------------------------
    
    # 潜航　30m------------------------------------------------------
    print("潜航　30m")
    of.diving_advance(rotate[2],ini_opx,sen_data)
    # -------------------------------------------------------------- 

    # 浮上 2m-------------------------------------------------------
    print("浮上 2m")
    of.ascend(sen_data)
    # 浮上-------------------------------------------------------

    # すべてのモータstop
    motor.stop()

    # log再生------------------------------------------------------

if __name__ == "__main__":
    Teaching()
