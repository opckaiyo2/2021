#coding: utf-8
import select
import tty
import sys
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor

def Manual():
    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    # key入力かプロボか
    # モータ回転数をteaching用データとして出力するか
    
    # 設定ファイル読み込み-------------------------------------------


    # key入力で制御する場合------------------------------------------
    tty.setcbreak(sys.stdin.fileno())

    motor = Motor()
    power = 10

    while(True):
        if select.select([sys.stdin],[],[],0) == ([sys.stdin],[],[]):
            input_key = sys.stdin.read(1)

            if input_key == "w":
                motor.go_back(power)
            elif input_key == "s":
                motor.go_back(power*-1)
            elif input_key == " ":
                motor.up_down(power)
            elif input_key == "z":
                motor.up_down(power*-1)

    # key入力で制御する場合------------------------------------------


    # プロボで操作する場合--------------------------------------------
    # プロボで操作する場合--------------------------------------------