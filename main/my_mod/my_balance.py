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

        # 目標と現在の差を180未満にする処理(右回り左回りに関係する)
        if abs(goal - now_yaw) > 180:
            self.e = 360 - abs(goal - now_yaw)
        else:
            self.e = abs(goal - now_yaw)

        # pid制御量決定
        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))
        # 右回り左回り決定
        direction = self.roteto(now_yaw,goal)

        # モータの回転数制限(電流値関係)
        if self.M > 30:
            self.M = 30
        elif self.M < 0:
            self.M = 0

        # 制御量と制御方向を決定
        MV = self.M * direction

        sen_data["x_dev"] = self.e
        sen_data["x_mov"] = self.M
        sen_data["x_dir"] = direction
        sen_data["x_goal"] = goal
        sen_data["x_now_yaw"] = now_yaw

        return MV

    #左周りが近いなら-1右周りなら1を返す
    def roteto(self,yaw,goal):
        direction = 0
        if yaw <= 180:
            if 0 > yaw - goal > -180:
                direction = -1
            else:
                direction = 1
        elif yaw <= 360:
            if 0 < yaw - goal < 180:
                direction = 1
            else:
                direction = -1

        return direction

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
        depth_zero = sen_data["depth"]

        now_depth = self.map_depth((sen_data["depth"] - depth_zero))
        # print(now_depth)
        # print("barance2:",sen_data["depth"] - depth_zero)

        self.M1 = self.M
        self.e1 = self.e
        self.e2 = self.e1

        self.e = self.map_depth(goal) - now_depth

        self.M = self.M1 + self.Kp * (self.e-self.e1) + self.Ki * self.e + self.Kd * ((self.e-self.e1) - (self.e1-self.e2))

        if self.M > 80:
            self.M = 80
        elif self.M < 0:
            self.M = 0

        MV = self.M

        sen_data["d_dev"] = now_depth
        sen_data["d_mov"] = self.M

        return MV

    # 圧力センサーの値を(0 ~ 100)に変換
    def map_depth(self, val):
        """
        2018年のパラメータ参考になるか分からん
        # # 海での値(波の上)
        # # in_min = 0.6
        # # in_max = 10
        # # 宜野湾
        # # in_min = 0.6
        # # in_max = 7.6
        # # 小学校プール
        # in_min = 1.5
        # in_max = 6

        """
        # ポリテクプール
        # in_min = 0.0
        # in_max = 0.3

        # 海
        in_min = 0.0
        in_max = 3.0

        # プールでの値
        # in_min = 2
        # in_max = 7

        if val <= in_min: val = in_min
        if val >= in_max: val = in_max

        in_min = in_min
        in_max = in_max
        out_min = 0
        out_max = 100
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        # print("map",val)
        return int(val)

#PID制御で水深調整---------------------------------------------------------------



if __name__ == '__main__':
    pass
