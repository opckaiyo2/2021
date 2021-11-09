#coding: utf-8
import configparser
import termios
import tty
import sys
import time

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor
# 
from my_operatfunction import OF

def Manual(sen_data):
    motor = Motor()
    of = OF()

    while(not('endtime' in sen_data)):
        pass

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    log_flag = inifile.getboolean("manual", "log_flag")
    
    # 設定ファイル読み込み-------------------------------------------

    of.Manual_advance(sen_data)