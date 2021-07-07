#coding: utf-8
import sys
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor

def Teaching():
    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE)

    # どのデータを読み込むか

    # 設定ファイル読み込み-------------------------------------------


    # log再生------------------------------------------------------
    # log再生------------------------------------------------------