#coding: utf-8
import sys
import ast
import configparser
from multiprocessing import Process, Manager, Value

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/main/my_mod")
# gpsのデータから目的地までの角度と距離の差異を計算する
from my_waypoint import waypoint
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
        inifile = configparser.SafeConfigParser()
        inifile.read(INI_FILE,encoding="utf-8")

        gps_initial = inifile.get("operation", "gps_initial")
        gps_diving = inifile.get("operation", "gps_diving")
        gps_ascend = inifile.get("operation", "gps_ascend")
        gps_test = inifile.get("operation", "gps_test")
        
        self.speed = inifile.getfloat("operation", "defalut_speed")
        self.depth = inifile.getint("operation", "depth")

        self.rotate = {"ava_rot":inifile.getint("autonomy","ava_rot"),
                    "re_rot":inifile.getint("autonomy","re_rot")}

        self.gps_maker = {"initial":ast.literal_eval(gps_initial),
                    "diving":ast.literal_eval(gps_diving),
                    "ascend":ast.literal_eval(gps_ascend),
                    "test":ast.literal_eval(gps_test)}
        # 設定ファイル読み込み-------------------------------------------

        self.pid_yaw = PID_yaw()
        self.pid_depth = PID_depth()
        self.motor = Motor()

    # コンフィグファイルで設定した初期・潜水・浮上位置に向かう関数
    # 引数 maker:どの位置に向かうかself.gps_maker(辞書型)のkeyの値 **sen_data:センサの値(辞書型)
    def gps_position(self,maker,**sen_data):
        while(True):
            # gpsとconfig.iniの初期位置比較
            gps = waypoint(sen_data["lon"],sen_data["lat"],
                        self.gps_maker[maker]["lon"], self.gps_maker[maker]["lat"])
            
            # 初期位置との誤差が2mいないだったら位置調整終了(gps_datasheetより誤差2m)
            if(gps["distance_2d"] < 2):
                # 初期位置調整のあとはモータがすべて止まってほしいためself.motor.stop_go_back()
                self.motor.stop_go_back()
                break
            
            # まずは角度調整,角度調節せず直進すると明後日の方向に
            self.rotate_yaw(gps["azimuth"],sen_data)

            # 直進 進む強さは電流計の値を見て調整できるようにしたい
            # pidしながら直進
            MV = self.pid_yaw.go_yaw(gps["azimuth"],sen_data["yaw"])
            self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)

    # 機体の向きを変える関数
    # 引数 goal:向きたい角度 **sen_data:センサの値(辞書型)
    def rotate_yaw(self,goal,**sen_data):
        while(True):
            # ゴールと誤差が5°以内なら終了
            if((goal-sen_data["yaw"]) < 5):
                # 角度調節した後はモータが止まってほしいためself.motor.stop()
                self.motor.stop()
                break

            # 方位角とオイラー角を合わせないといけない?
            # pidで角度調整
            MV = self.pid_yaw.go_yaw(goal,sen_data["yaw"])
            self.motor.spinturn(MV)

    # コンフィグファイルで設定した深さに機体を潜らせる関数
    # 引数 **sen_data:センサの値(辞書型)
    def diving(self,**sen_data):
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
    # 引数 rotate:どのくらい進むかself.rotate(辞書型)のkeyの値 yaw:機体に向き(pidの向き) **sen_data:センサの値(辞書型) 
    def diving_advance(self,rotate,yaw,**sen_data):
        # 潜水して進む前のモータ回転数を記録(合計値)
        rot = list(range(4))
        for i in range(4):
            rot[i] = int(sen_data["rot"+str(i)])
        
        rot_sum = sum(rot)

        # モータが一定回転したら終了
        while(True):
            # 現在のモータ回転数を記録
            for i in range(4):
                rot[i] = int(sen_data["rot"+str(i)])
        
            # 潜水後のモータ回転数の平均記録
            ava = (sum(rot)-rot_sum) / len(rot)

            # モータ回転数が規定値を超えていれば終了
            if(ava > self.rotate[rotate]):
                # 潜水して進み終えたら浮上するから潜っているモータと前進しているモータストップ
                # 機体は浮力で自然に浮かぶため浮上の手助けのため止めている
                self.motor.stop()
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
            self.motor.up_down(MV)

            # 方向pid
            MV = self.pid_yaw.go_yaw(yaw,sen_data["yaw"])
            self.motor.go_back_each(self.speed-MV,self.speed+MV,self.speed,self.speed)

    # 浮上する関数
    # 引数 **sen_data:センサの値(辞書型)
    def ascend(self,**sen_data):
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
    # 引数 maker:浮上位置の設定self.gps_maker(辞書型)のkeyの値 yaw:機体の向き(pidの向き) **sen_data:センサの値(辞書型)
    def re_diving(self,maker,yaw,**sen_data):
        while(True):
            # wapoint関数で距離、方位角、逆方位角もとめる(距離と角度)
            gps = waypoint(sen_data["lot"],sen_data["lat"],
                self.gps_maker[maker]["lon"],self.gps_maker[maker]["lat"])
            
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

            of.gps_position("test",sen_sata)

        except KeyboardInterrupt:
            motor.stop()

        except Exception as e:
            motor.stop()