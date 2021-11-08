#coding: utf-8
from concurrent import futures
import sys
import time
import traceback
import configparser
from multiprocessing import Process, Manager, Value

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# arduinoとシリアル通信　済
from my_ard import get_sen
# gpsのデータ取得
from my_gps import get_gps
# motor制御　済
from my_motor import Motor
# カメラ制御　済
from my_camera import cap_main
# logテキスト作成　済
from my_log import log_txt

# Teaching
from my_Teaching import Teaching
# 完全自律
from my_Autonomy import Autonomy
# 手動
from my_Manual import Manual
#潜水テスト
from my_Test import Tinou

# 設定ファイル読み込み-------------------------------------------

INI_FILE = "/home/pi/2021/main/config/config.ini"
inifile = configparser.ConfigParser()
inifile.read(INI_FILE,encoding="utf-8")

operation = inifile.getint("main", "operation")
log_flag = inifile.getboolean("main", "log_flag")

# 設定ファイル読み込み-------------------------------------------

def main():

    #-----------------------------
    # 軽量化のためのマルチプロセス設定
    #-----------------------------
    
    # Managerオブジェクトの作成
    # with文は終了時に必要な処理を補完してくれる文 今回はprocessの終了をしてくれる
    with Manager() as manager:

        # プロセス間の通信設定
        # ard_senser,gpsデータ格納用
        sen_data = manager.dict()
        # 知能計測チャレンジカメラフラグ
        cap_flag = Value('i',0)
        X = Value('i',0)
        Y = Value('i',0)
        S = Value('i',0)

        # 各プロセスオブジェクト作成
        # ardからデータ取得
        ard_process = Process(target=get_sen, daemon=True, args=(sen_data,))
        # gpsからデータ取得
        gps_process = Process(target=get_gps, daemon=True, args=(sen_data,))
        # カメラ
        #camera_process = Process(target=cap_main, daemon=True, args=(cap_flag,X,Y,S,))
        # データログ
        log_process = Process(target=log_txt, daemon=True, args=(sen_data,))

        # 各プロセススタート
        ard_process.start()
        gps_process.start()
        #camera_process.start()
        if log_flag:
            log_process.start()

        # 必要な機能のインスタンス作成
        # main.pyの中でモータは制御しないつもりだが緊急停止用
        motor = Motor()

        try:
            # どの操作方法で動かすか---------------------------------
            
            if(operation == 1):
                Teaching(sen_data)
            elif(operation == 2):
                Autonomy(sen_data)
            elif(operation == 3):
                Manual(sen_data)
            elif(operation == 4):
                Tinou(sen_data,cap_flag,X,Y,S)
            else:
                #例外発生分except Exception as eでエラーが検出される
                raise ValueError("The operation setting value in config.ini is wrong.")

            # どの操作方法で動かすか---------------------------------
            
        except KeyboardInterrupt:
            motor.stop()
        except Exception as e:
            motor.stop()
            print(traceback.format_exc())
            print("\n")
            print("main.py main try error : ",e)
            print("\n")




if __name__ == "__main__":
    main()
