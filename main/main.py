#coding: utf-8
# 自作関数読み込みのためのライブラリ
import sys
# エラー検出用のライブラリ
import traceback
# コンフィグファイル使用のライブラリ
import configparser
# マルチプロセスのためのライブラリ
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

# コンフィグファイルの場所
INI_FILE = "/home/pi/2021/main/config/config.ini"
# クラスをインスタンス化
inifile = configparser.ConfigParser()
#  コンフィグファイルの場所 文字コードを指定しコンフィグ読み込み
inifile.read(INI_FILE,encoding="utf-8")

# コンフィグのmain項目のoperationを読み込み(実行するプログラムの種類)
operation = inifile.getint("main", "operation")
# コンフィグのmain項目のlog_flagを読み込み(ログ生成するかのフラグ)
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
        # カメラで認識した物体の状態格納用
        X = Value('i',0)
        Y = Value('i',0)
        S = Value('i',0)

        # 各プロセスのインスタンス作成
        # ardからデータ取得
        ard_process = Process(target=get_sen, daemon=True, args=(sen_data,))
        # gpsからデータ取得
        gps_process = Process(target=get_gps, daemon=True, args=(sen_data,))
        # カメラ
        camera_process = Process(target=cap_main, daemon=True, args=(cap_flag,X,Y,S,))
        # データログ
        log_process = Process(target=log_txt, daemon=True, args=(sen_data,))

        # 各プロセススタート
        # ardからデータ取得
        ard_process.start()
        # gpsからデータ取得
        gps_process.start()
        # カメラ
        camera_process.start()
        # データログ(データフラグを使用することでON/OFF切り替え)
        if log_flag:
            log_process.start()

        # 必要な機能のインスタンス作成
        # main.pyの中でモータは制御しないつもりだが緊急停止用
        motor = Motor()

        # try文はexceptとセットで使われエラーが発生した際にエラーによって実行する処理を変えることができる。
        # 特にエラーでプログラムが終了した際にモータをストップできるように使用している。
        try:
            # どの操作方法で動かすか---------------------------------
            
            if(operation == 1):
                # 2021/my_mod/my_Teaching.pyの関数Teachingを呼び出す。sen_data(センサデータ)を渡す。
                Teaching(sen_data)
            elif(operation == 2):
                # 2021/my_mod/my_Autonomy.pyの関数Autonomyを呼び出す。sen_data(センサデータ)を渡す。
                Autonomy(sen_data)
            elif(operation == 3):
                # 2021/my_mod/my_Manual.pyの関数Manualを呼び出す。sen_data(センサデータ)を渡す。
                Manual(sen_data)
            elif(operation == 4):
                # 2021/my_mod/my_Test.pyの関数Tinouを呼び出す。sen_data(センサデータ)などを渡す。
                Tinou(sen_data,cap_flag,X,Y,S)
            else:
                #例外発生分except Exception as eでエラーが検出される
                raise ValueError("The operation setting value in config.ini is wrong.")

            # どの操作方法で動かすか---------------------------------

        except KeyboardInterrupt:
            # キーボードエラー(Ctrl+Cなどでプログラムを終了させた)時モータストップ
            motor.stop()

        except Exception as e:
            # その他すべてのエラー時モータストップ
            motor.stop()
            # 詳細エラー内容を表示
            print(traceback.format_exc())
            # 見やすさ改善改行
            print("\n")
            # 簡易エラー内容を表示
            print("main.py main try error : ",e)
            # 見やすさ改善改行
            print("\n")

        finally:
            # プログラム終了時　サブプロセスkill
            # サブプロセスがまだ生きていればkillする
            if(ard_process.is_alive()):
                ard_process.kill()
            
            if(gps_process.is_alive()):
                gps_process.kill()

            if(camera_process.is_alive()):
                camera_process.kill()

            if(log_process.is_alive()):
                log_process.kill()

# ここはこのファイルを単体で実行するとここからプログラムがスタートする。
if __name__ == "__main__":
    main()
