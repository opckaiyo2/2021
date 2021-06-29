# sudo pip install pyserial
import serial
import ast
import time
import sys
from datetime import datetime
from multiprocessing import Manager, Process
# from multiprocessing import Manager, Process, Queue, Lock
sys.path.append("/kaiyo/my_mod")

# ArduinoMEGAとpinで接続
# ser = serial.Serial('/dev/ttyS0', 115200,timeout=3)
# ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0', 115200,timeout=3)

# def get_data():
#     while True:
#         # Arduino から一行取得
#         data = ser.readline()
#         # 受信エラー確認
#         try:
#             return data
#
#         except SyntaxError:
#             # 受信エラー
#             print("Reception Error!!")

def get_data(data):
    while True:
        # Arduino から一行取得
        val = ser.readline()
        # print("data")
        # print(val)
        # 受信エラー確認
        try:
            # print("でーただよー")

            # dictに変換
            val = ast.literal_eval(val.decode('unicode-escape'))
            # print(val)
            for i in val:
                data[i] = val[i]

            # print(data,"\n")
        except SyntaxError:
            # 受信エラー
            print("Reception Error!!")

# q = Queue()
# lc = Lock()
#
# def get_read_data():
#     # Arduino から一行取得
#     data = ser.readline()
#     # 受信エラー確認
#     try:
#         # dictに変換
#         data = ast.literal_eval(data.decode('unicode-escape'))
#         q.put(data) #共有メモリに格納
#
#
#     except SyntaxError:
#         # 受信エラー
#         print("Reception Error!!")
#
# def get_data(val="all"):
#     while True:
#         try:
#             print('ロック')
#             lc.acquire()    # ロック
#             get_read_data()
#             lc.release()    # ロック解除
#             print('ロック解除','\n')
#             data = q.get()
#             # print(data)
#             break
#         except Exception as e:
#             print("れいがい")
#             pass
#
#     if val == "all": return data
#     if val == "yaw": return data["yaw"]
#     if val == "state": return data["state"]
#     if val == "average_go": return (data["rot0"] + data["rot1"]) / 2
#     if val == "average_up": return (data["rot2"] + data["rot3"]) / 2
#     return data[val]

#ArduinoMEGAにコマンド送信---------------------------------------------

#("  'run':'シリアル通信を開始する。', ");
#("  'stop':'シリアル通信を停止する。', ");
#("  'reboot':'Arduinoを再起動する。', ");
#("  'reset xxx':'curまたはrotの値をリセットする。', ");
#("  'debug':'デバッグモードに移行offをつけると通常モードに戻る。', ");
#("  'time XXXX':'無限ループ時の待機時間をXXXXミリ秒にする。', ");
#("  'yaw_zero off':'yawの初期リセット値を無効化', ");
#("  'remove error':'状態を確認し問題なかったらstateをnormalにする', ");

#主に通信開始時に動機をとるために再起動する val = reboot

def send_data(val):
    ser.write(val.encode('unicode-escape'))

#ArduinoMEGAにコマンド送信---------------------------------------------


"""
# yawの値変換
def my_map(val):
    in_min = 0
    in_max = 360
    out_min = 0
    out_max = 100
    val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    # 少数切り捨ての為intに変換
    return int(val)
"""


if __name__ == '__main__':
    # send_data("reboot")
    # data = ser.readline()
    # print("data:",data)
    # print(data.decode('unicode-escape'))
    # str = ast.literal_eval(data.decode('unicode-escape'))
    # print(str)

    print("wait:reboot now")
    while True:
        try:
            send_data("reboot")
            # time.sleep(1)
            val = ser.readline() #.decode('unicode-escape') *#
            print("val1",val)
            val = ast.literal_eval(val.decode('unicode-escape'))
            print("val2",val)

            if val["time"] <= 10.0:
                print("Nice")
                # time.sleep(1)
                break

        except SyntaxError:
            # 受信エラー
            print("\nserial : Reception Error!!\n")
        except TimeoutError:
            print("serial : timeout Error!\n")
        # except ValueError:
        #     print("serial : Value Error!\n")


    while True:
        print("OK")
        # print type(get_data("all"))
        # get_read_data()
        # print("b   ",data)
        # get_read_data()
        # print(get_data())
        get_data(val)
        # print(data)
        # get_data("depth")
        # print("str")
        # print(str)

    ser.close()
