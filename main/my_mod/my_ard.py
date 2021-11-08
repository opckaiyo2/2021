#coding: utf-8

# Arduinoのsensordataを変換するためのライブラリ
import ast
# Arduinoとserial通信するためのライブラリ
import serial
# サブプロセス運用のため必要？(要検証)
import multiprocessing 

def get_sen(sen_data):
    # arduinoのピン通信速度設定(115200は通信最高速度)
    ser = serial.Serial('/dev/ttyACM0', 115200)
    
    # メインプロセスが終了するまで無限ループ
    while True:
        # try文はexceptとセットで使われエラーが発生した際にエラーによって実行する処理を変えることができる。
        # 特にエラーでプログラムが終了した際にモータをストップできるように使用している。
        try:
            # arduinoから送られてきたデータを一行取得&デコード
            String_data = ser.readline().decode('utf-8').rstrip()
            # 文字型から辞書型に変換
            dic_date = ast.literal_eval(String_data)
            # multiprocessでprocess間値共有(sen_data) main.pyで設定
            for key in dic_date.keys():
                sen_data[key] = dic_date[key]

        except KeyboardInterrupt as key:
            # キーボードエラー(Ctrl+Cなどでプログラムを終了させた)時モータストップ
            break

        except Exception as e:
            # 見やすさ改善改行
            print("\n")
            # 簡易エラー内容を表示
            print("my_ard.py get_sen try error : ",e)
            # 見やすさ重視改行
            print("\n")

# ここはこのファイルを単体で実行するとここからプログラムがスタートする。
if __name__ == "__main__":
    sen_data = {}
    get_sen(sen_data)
