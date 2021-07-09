#coding: utf-8
import sys
import ast
import configparser

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# gpsのデータから目的地までの角度と距離の差異を計算する
from my_waypoint import waypoint
# motor制御
from my_motor import Motor
# pid制御
from my_balance import PID_yaw,PID_depth

class OF:
    def __init__(self):
        # 設定ファイル読み込み-------------------------------------------
        INI_FILE = "/home/pi/2021/main/config/config.ini"
        inifile = configparser.SafeConfigParser()
        inifile.read(INI_FILE)

        self.gps_initial = inifile.get("operation", "gps_initial")
        self.gps_diving = inifile.get("operation", "gps_diving")
        self.gps_ascend = inifile.get("operation", "gps_ascend")
        self.speed = inifile.get("operation", "defalut_speed")
        self.depth = inifile.get("operation", "depth")

        self.ava_rot = inifile.getint("autonomy","ava_rot")
        self.re_rot = inifile.getint("autonomy","re_rot")

        self.gps_initial = ast.literal_eval(gps_initial)
        self.gps_diving = ast.literal_eval(gps_diving)
        self.gps_ascend = ast.literal_eval(gps_ascend)
        # 設定ファイル読み込み-------------------------------------------

        self.pid_yaw = PID_yaw()
        self.pid_depth = PID_depth()
        self.motor = Motor()

    def gps_Initial_position(self,**sen_data):
            while(True):
                # gpsとconfig.iniの初期位置比較
                gps = waypoint(sen_data["lon"],sen_data["lat"],
                            self.gps_initial["lon"], self.gps_initial["lat"])
                
                # 初期位置との誤差が2mいないだったら位置調整終了(gps_datasheetより誤差2m)
                if(gps["distance_2d"] < 2):
                    self.motor.stop_go_back()
                    break
                
                # まずは角度調整,角度調節せず直進すると明後日の方向に
                while(True):
                    if((gps["azimuth"]-sen_data["yaw"]) < 5):
                        self.motor.stop()
                        break

                    # 方位角とオイラー角を合わせないといけない
                    MV = self.pid_yaw.go_yaw(gps["azimuth"],sen_data["yaw"])
                    self.motor.spinturn(MV)

                # 直進 進む強さは電流計の値を見て調整できるようにしたい
                MV = self.pid_yaw.go_yaw(0,sen_data["yaw"])
                self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)

    def rotate_yaw(self,):