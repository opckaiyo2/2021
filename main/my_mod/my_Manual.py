#coding: utf-8
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
    inifile.read(INI_FILE)

    # key入力かプロボか
    # モータ回転数をteaching用データとして出力するか
    
    # 設定ファイル読み込み-------------------------------------------


    # key入力で制御する場合------------------------------------------
    # key入力で制御する場合------------------------------------------


    # プロボで操作する場合--------------------------------------------
    # プロボで操作する場合--------------------------------------------