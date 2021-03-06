#coding: utf-8
import configparser

#PID制御で角度調整---------------------------------------------------------------

# M : 与える操作量
# M1 : 一つ前に与えた操作量
# goal : 目的値
# e : 偏差(目的値と現在値の差)
# e1 : 前回に与えた偏差
# e2 : 前々回に与えた偏差
# Kp : 比例制御（P制御)の比例定数
# Ki : 積分制御（I制御)の比例定数
# Kd : 微分制御（D制御)の比例定数

class PID_yaw:
    def __init__(self):
        # 設定ファイル読み込み-------------------------------------------
        INI_FILE = "/home/pi/2021/main/config/config.ini"
        inifile = configparser.SafeConfigParser()
        inifile.read(INI_FILE,encoding="utf-8")

        yaw_pid = inifile['yaw_pid']
        # 設定ファイル読み込み-------------------------------------------

        # インスタンス変数定義
        self.M = 0.00
        self.M1 = 0.00

        self.e = 0.00
        self.e1 = 0.00
        self.e2 = 0.00

        self.Kp = float(yaw_pid.get('Kp'))
        self.Ki = float(yaw_pid.get('Ki'))
        self.Kd = float(yaw_pid.get('Kd'))

    def go_yaw(self, goal, sen_data):

        # センサから得た現在の方向
        now_yaw = sen_data["x"]

        # 計算ように-180~180だったデータを0-359に 現在の方向
        if now_yaw < 0:
            now_yaw = 360 + now_yaw

        # 計算ように-180~180だったデータを0-359に 目標の方向
        if goal < 0:
            goal = 360 + goal

        # pid制御は前回の制御を覚えるため値の更新
        self.M1 = self.M
        self.e1 = self.e
        self.e2 = self.e1

        # 目標と現在の差を計算する。
        self.e = goal - now_yaw

        # pid制御量決定
        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))

        # モータの回転数制限(電流値関係)
        if self.M > 30:
            self.M = 30
        elif self.M < -30:
            self.M = -30

        sen_data["x_dev"] = self.e
        sen_data["x_mov"] = self.M
        sen_data["x_goal"] = goal
        sen_data["x_now_yaw"] = now_yaw

        return self.M

#PID制御で角度調整---------------------------------------------------------------


#PID制御で水深調整---------------------------------------------------------------

class PID_depth:
    def __init__(self):
        # 設定ファイル読み込み-------------------------------------------
        INI_FILE = "/home/pi/2021/main/config/config.ini"
        inifile = configparser.SafeConfigParser()
        inifile.read(INI_FILE,encoding="utf-8")

        depth_pid = inifile['depth_pid']
        # 設定ファイル読み込み-------------------------------------------

        self.M = 0.00
        self.M1 = 0.00

        self.e = 0.00
        self.e1 = 0.00
        self.e2 = 0.00

        self.Kp = float(depth_pid.get('Kp'))
        self.Ki = float(depth_pid.get('Ki'))
        self.Kd = float(depth_pid.get('Kd'))

    def go_depth(self, goal, sen_data):
        # 初期値
        now_depth = sen_data["depth"]

        self.M1 = self.M
        self.e1 = self.e
        self.e2 = self.e1

        self.e = goal - now_depth

        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))

        if self.M > 80:
            self.M = 80
        elif self.M < -80:
            self.M = -80

        sen_data["d_dev"] = self.e
        sen_data["d_mov"] = self.M
        sen_data["d_goal"] = goal
        sen_data["d_now_dep"] = now_depth

        return self.M

#PID制御で水深調整---------------------------------------------------------------



if __name__ == '__main__':
    pass
