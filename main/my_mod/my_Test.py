#coding: utf-8
import sys
import time
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor
from my_operatfunction import OF

def Test(sen_data):

    of = OF()
    motor = Motor()
    
    # データがすべて揃うまでループ endtimeはデータの一番後列
    while(not('endtime' in sen_data)):
        pass

    # センサの値が落ち着くまでまつ
    time.sleep(2)

    # 初期向きの暗記
    ini_x = sen_data["x"]

    # 初期向きの反対(Uターンなどで使う)
    ini_opx = 0

    if ini_x < 180:
        ini_opx = ini_x+150
    elif ini_x > 180:
        ini_opx = ini_x-150
    else:
        ini_opx = (ini_x+180) % 360

    print("PID目標方位 : " + str(ini_x))
    print("Uターン後 PID目標 : " + str(ini_opx))
    print("\n")

    of.rotate_advance(100000000,ini_x,sen_data)


if __name__ == "__main__":
    pass
