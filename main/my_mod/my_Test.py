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

    while(True):
        try:
            # 潜水---------------------------------------------
            print("潜水")
            motor.up_down(20)

            time.sleep(3)

            # 浮上-------------------------------------------------------
            print("浮上")
            motor.up_down(-20)

            time.sleep(3)
            # すべてのモータstop
        except KeyboardInterrupt as e:
            motor.stop()
