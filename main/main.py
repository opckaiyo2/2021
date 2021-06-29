from concurrent import futures
import sys
import time
import sys
import serial
import ast
import termios
import os
import configparser
from multiprocessing import Process, Manager, Value

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# arduinoとシリアル通信
from my_ard import get_sen
# gpsのデータ取得
from my_gps import get_gps
# motor制御
from my_motor import Motor
# 姿勢制御
from my_balance import PID_yaw, PID_depth
# カメラ制御
from my_camera import cap_main
# logテキスト作成
from my_log import log_txt

# Teaching
from my_Teaching import Teaching
# 完全自律
from my_Autonomy import Autonomy
# 手動
from my_Manual import Manual

# 設定ファイル読み込み-------------------------------------------

INI_FILE = "/home/pi/2021/main/config/config.ini"
inifile = configparser.SafeConfigParser()
inifile.read(INI_FILE)

operation = inifile.getint("default", "operation")

# 設定ファイル読み込み-------------------------------------------

def main():

    #-----------------------------
    # 軽量化のためのマルチプロセス設定
    #-----------------------------
    
    # Managerオブジェクトの作成
    # with文は終了時に必要な処理を補完してくれる文 今回はprocessの終了をしてくれる
    with Manager() as manager:

        # プロセス間の通信設定
        # gpsデータ格納用
        gps_data = manager.dict()
        # ardデータ格納用
        ard_data = manager.dict()
        # 知能計測チャレンジ フラフープ中心座標
        hoop_Coordinate = manager.dict()

        # 各プロセスオブジェクト作成
        # ardからデータ取得
        ard_process = Process(target=get_sen, daemon=True, args=(ard_data))
        # gpsからデータ取得
        gps_process = Process(target=get_gps, daemon=True, args=(gps_data))
        # カメラ
        camera_process = Process(traget=cap_main, daemon=True, args=(hoop_Coordinate))
        # データログ
        log_process = Process(target=log_txt, daemon=True, args=(ard_data, gps_data))

        # 各プロセススタート
        ard_process.start()
        gps_process.start()
        camera_process.start()
        log_process.start()

        # 必要な機能のオブジェクト作成
        motor = Motor()
        pid_yaw = PID_yaw()
        pid_depth = PID_depth()


        #main loop
        while(True):
            try:
                # どの操作方法で動かすか---------------------------------
                
                if(operation == 1):
                    Teaching()
                elif(operation == 2):
                    Autonomy()
                elif(operation == 3):
                    Manual()
                else:
                    raise ValueError("The operation setting value in config.ini is wrong.")

                # どの操作方法で動かすか---------------------------------


                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print("\n")
                print("main.py main try error : ",e)
                print("\n")




if __name__ == "__main__":
    try:
        main()
    except:
        pass
