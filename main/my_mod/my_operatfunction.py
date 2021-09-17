#coding: utf-8
import sys
import ast
import configparser
from pyproj import Geod
from multiprocessing import Process, Manager, Value

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# motor制御
from my_motor import Motor
# pid制御
from my_balance import PID_yaw,PID_depth
# arduinoとシリアル通信　済
from my_ard import get_sen
# gpsのデータ取得
from my_gps import get_gps


class OF:
    def __init__(self):
        # 設定ファイル読み込み-------------------------------------------
        INI_FILE = "/home/pi/2021/main/config/config.ini"
        inifile = configparser.ConfigParser()
        inifile.read(INI_FILE,encoding="utf-8")

        gps_initial = ast.literal_eval(inifile.get("operation", "gps_initial"))
        gps_diving = ast.literal_eval(inifile.get("operation", "gps_diving"))
        gps_ascend = ast.literal_eval(inifile.get("operation", "gps_ascend"))
        gps_test = ast.literal_eval(inifile.get("operation", "gps_test"))
        
        self.speed = inifile.getfloat("operation", "defalut_speed")
        self.depth = inifile.getint("operation", "depth")

        self.rotate = {"ava_rot":inifile.getint("autonomy","ava_rot"),
                    "re_rot":inifile.getint("autonomy","re_rot")}

        self.gps_maker = {"initial":gps_initial,
                    "diving":gps_diving,
                    "ascend":gps_ascend,
                    "test":gps_test}
        # 設定ファイル読み込み-------------------------------------------

        self.pid_yaw = PID_yaw()
        self.pid_depth = PID_depth()
        self.motor = Motor()

    # コンフィグファイルで設定した初期・潜水・浮上位置に向かう関数
    # 引数 maker:どの位置に向かうかself.gps_maker(辞書型)のkeyの値 sen_data:センサの値(辞書型)
    def gps_position(self,maker,sen_data):
        while(True):
            # gpsとconfig.iniの初期位置比較
            gps = self.waypoint(sen_data["lat"],sen_data["lon"],
                        self.gps_maker[maker]["lat"], self.gps_maker[maker]["lon"])
            
            # 初期位置との誤差が2mいないだったら位置調整終了(gps_datasheetより誤差2m)
            if(gps["distance_2d"] < 2):
                # 初期位置調整のあとはモータがすべて止まってほしいためself.motor.stop_go_back()
                self.motor.stop_go_back()
                break
            
            # まずは角度調整,角度調節せず直進すると明後日の方向に
            self.rotate_yaw(gps["azimuth"],sen_data)

            # 直進 進む強さは電流計の値を見て調整できるようにしたい
            # pidしながら直進
            MV = self.pid_yaw.go_yaw(gps["azimuth"],sen_data["x"])
            self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)

    # 機体の向きを変える関数
    # 引数 goal:向きたい角度 sen_data:センサの値(辞書型)
    def rotate_yaw(self,goal,sen_data):
        while(True):
            # ゴールと誤差が5°以内なら終了
            if(abs(goal-sen_data["x"]) < 5):
                # 角度調節した後はモータが止まってほしいためself.motor.stop()
                self.motor.stop()
                break

            # 方位角とオイラー角を合わせないといけない?
            # pidで角度調整
            MV = self.pid_yaw.go_yaw(goal,sen_data["x"])
            self.motor.spinturn(MV)

    # コンフィグファイルで設定した深さに機体を潜らせる関数
    # 引数 sen_data:センサの値(辞書型)
    def diving(self,sen_data):
        # 潜る前の圧力センサの値を保持(浮上時に使用)
        self.initial_depth = sen_data["depth"]
        while(True):
            # datasheetの分解能から記入したい(0.2)
            # ゴールとの誤差が0.2なら深さ調節終了
            if(abs(self.depth-sen_data["depth"]) < 0.2):
                # 潜水後も潜り続けてほしいためモータはとめない
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
            self.motor.up_down(MV)

    # 水に潜った状態で前に進む関数
    # 引数 rotate:どのくらい進むかself.rotate(辞書型)のkeyの値 yaw:機体に向き(pidの向き) sen_data:センサの値(辞書型) 
    def diving_advance(self,rotate,yaw,sen_data):
        # 潜水して進む前のモータ回転数を記録(合計値)
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]
        
        # モータが一定回転したら終了
        while(True):
            rot = 0
            # 現在のモータ回転数を記録
            for i in range(4):
                rot[i] = sen_data["rot"+str(i)]

            # モータ回転数が規定値を超えていれば終了
            if(rot - rot_ini) >= rotate:
                # 潜水して進み終えたら浮上するから潜っているモータと前進しているモータストップ
                # 機体は浮力で自然に浮かぶため浮上の手助けのため止めている
                self.motor.stop()
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
            self.motor.up_down(MV)

            # 方向pid
            MV = self.pid_yaw.go_yaw(yaw,sen_data["x"])
            self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)

    # 浮上する関数
    # 引数 sen_data:センサの値(辞書型)
    def ascend(self,sen_data):
        while(True):
            # 目標の深さになったら終了
            if(abs(self.initial_depth-sen_data["depth"]) < 0.2):
                # 浮上あとは機体は浮くようになっているためモータストップ
                self.motor.stop_up_down()
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.initial_depth,sen_data["depth"])
            self.motor.up_down(MV)

    # 浮上後設定した浮上位置か比較し、再潜水を行う関数
    # 引数 maker:浮上位置の設定self.gps_maker(辞書型)のkeyの値 yaw:機体の向き(pidの向き) sen_data:センサの値(辞書型)
    def re_diving(self,maker,yaw,sen_data):
        while(True):
            # wapoint関数で距離、方位角、逆方位角もとめる(距離と角度)
            gps = self.waypoint(sen_data["lat"],sen_data["lon"],
                self.gps_maker[maker]["lat"],self.gps_maker[maker]["lon"])
            
            # 目標との距離が2mいないなら(gpsの誤差が2mのため)
            if(gps["distance_2d"] < 2):
                break

            # 潜水
            self.diving(sen_data)
            # 潜水あと進む
            self.diving_advance("re_rot",yaw,sen_data)
            # 浮上
            self.ascend(sen_data)

            # wait gps取れるまで

    # gpsと現在地の緯度、経度から距離、方位角、逆方位角を求める
    # 引数 g_lat:目的地緯度 g_lon:目的地経度 sen_data:センサの値(辞書型)
    def waypoint(self,s_lat,s_lon,g_lat,g_lon):
        g = Geod(ellps='WGS84')
        azimuth, back_azimuth, distance_2d = g.inv(s_lat,s_lon, g_lat, g_lon)
        gps = {'azimuth': azimuth, 'back_azimuth': back_azimuth,'distance_2d': distance_2d}
        return gps

    # モータの回転数合計を見て既定の回転数に達すまでモータ回し続ける
    # 深さを調節するモータはpidで回すので前進後進モータだけ止める
    # 引数 gola:目的の回転回数 sen_data:センサ値(辞書型)
    def rotate_advance(self,rotate,x,sen_data):
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]

        while(True):
            rot = 0
            for i in range(4):
                rot += sen_data["rot"+str(i)]

            if (rot - rot_ini) >= rotate:
                self.motor.stop_go_back()
                break

            MV = self.pid_yaw.go_yaw(x,sen_data["x"])
            self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)


if __name__ == "__main__":
    of = OF()
    motor = Motor()
    with Manager() as manager:
        try:
            sen_sata = manager.dict()
            
            ard_process = Process(target=get_sen, daemon=True, args=(sen_sata,))
            gps_process = Process(target=get_gps, daemon=True, args=(sen_sata,))

            ard_process.start()
            gps_process.start()

            motor.go_back(10)

            # デバック順番---------------
            # azimuth 210.490025 back 30.4546277777778 distance 15,719.204m になるはず
            # print(of.waypoint(sen_sata["lat"],sen_sata["lon"],26.258317,127.736353))
            
            # 設定した方向に回転するはず
            # of.rotate_yaw(180,sen_sata)
            
            # 行きたい方向に自動で行くはず
            # of.gps_position("test",sen_sata)
            
            # あとは適当で可
            # デバック順番---------------

        except KeyboardInterrupt:
            motor.stop()

        except Exception as e:
            motor.stop()