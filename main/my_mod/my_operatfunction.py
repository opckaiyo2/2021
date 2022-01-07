#coding: utf-8
# 自作関数読み込みのためのライブラリ
import sys
# Arduinoのsensordataを変換するためのライブラリ
import ast
# コンフィグファイル使用のライブラリ
import configparser
# gpsの位置計算用ライブラリ
from pyproj import Geod
# マルチプロセスのためのライブラリ
from multiprocessing import Process, Manager, Value
# 主に時間計測やwait処理などで必要なライブラリ
import time

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
    # この関数はOFクラスがインスタンス化を行う時に必ず最初に呼び出される特殊な関数
    def __init__(self):
        # 設定ファイル読み込み-------------------------------------------

        # コンフィグファイルの場所
        INI_FILE = "/home/pi/2021/main/config/config.ini"
        # クラスをインスタンス化
        inifile = configparser.ConfigParser()
        #  コンフィグファイルの場所 文字コードを指定しコンフィグ読み込み
        inifile.read(INI_FILE,encoding="utf-8")

        # gpsのwaypoint(潜水位置など)をコンフィグファイルから読み込み
        gps_initial = ast.literal_eval(inifile.get("operation", "gps_initial"))
        gps_diving = ast.literal_eval(inifile.get("operation", "gps_diving"))
        gps_ascend = ast.literal_eval(inifile.get("operation", "gps_ascend"))
        gps_test = ast.literal_eval(inifile.get("operation", "gps_test"))
        
        # 機体のスピードを調整するduty比(電流値の関係で55がMAX電気科と要相談)
        self.speed = inifile.getfloat("operation", "defalut_speed")
        # 機体の潜る深さを設定する
        self.depth = inifile.getfloat("operation", "depth")

        # デバッグモードのon:offフラグ
        debug_flag = inifile.getboolean("operation","debug_flag")

        # 機体を自動で動かす場合海上ではGPSを使用するが海中ではモータの回転数をで制御する
        # その際に使用するモータ回転数読み込み辞書型化する
        self.rotate = {"ava_rot":inifile.getint("autonomy","ava_rot"),
                    "re_rot":inifile.getint("autonomy","re_rot")}

        # 読み込んだwaypointを辞書型化する
        self.gps_maker = {"initial":gps_initial,
                    "diving":gps_diving,
                    "ascend":gps_ascend,
                    "test":gps_test}

        # 設定ファイル読み込み-------------------------------------------

        # 深さをPIdで制御するためのクラスをインスタンス化
        self.pid_depth = PID_depth()
        # モータを制御するためのクラスをインスタンス化
        self.motor = Motor()

    # コンフィグファイルで設定した初期・潜水・浮上位置に向かう関数
    # 引数 maker:どの位置に向かうかself.gps_maker(辞書型)のkeyの値 sen_data:センサの値(辞書型)
    # この関数は時間がなかったため動作未確認です。
    def gps_position(self,maker,sen_data):
        # 設定した目的地に到達するまで無限ループ
        while(True):
            # 現在のgps値とconfig.iniの初期位置比較
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
            MV = self.pid_yaw.go_yaw(gps["azimuth"],sen_data)
            self.motor.go_back_each(self.speed+MV,self.speed-MV,self.speed+MV,self.speed-MV)

    # 機体の向きを変える関数
    # 引数 goal:向きたい角度 sen_data:センサの値(辞書型)
    def rotate_yaw(self,goal,sen_data):
        print("Uターン開始方位\t\t"+str(sen_data["x"]))
        print("Uターン終了予定方位\t"+str(goal))
        # 方位pIdのクラスをインスタンス化
        pid_yaw = PID_yaw()
        while(True):
            if(debug_flag):
                # 現在の機体向きを表示
                print("\r現在方位\t\t"+str(sen_data["x"]),end="")
            # ゴールと誤差が5°以内なら終了
            if(abs(goal-sen_data["x"]) < 30):
                # 角度調節した後はモータが止まってほしいためself.motor.stop()
                self.motor.stop()
                # 見やすさ改善改行
                print("\n")
                break

            # pidで角度調整(現在は不具合が出たためコメントアウト中)
            #MV = pid_yaw.go_yaw(goal,sen_data)
            self.motor.spinturn(30)

    # コンフィグファイルで設定した深さに機体を潜らせる関数
    # 引数 sen_data:センサの値(辞書型)
    def diving(self,sen_data):
        print("潜水開始深さ\t"+str(sen_data["depth"]))
        print("潜水終了深さ\t"+str(self.depth))
        # 潜る前の圧力センサの値を保持(浮上時に使用)
        self.initial_depth = sen_data["depth"]
        while(True):
            if(debug_flag):
                # 現在の機体の深さを表示
                print("\r深さ\t\t"+str(sen_data["depth"]),end="")
            # datasheetの分解能から記入したい(0.2)
            # ゴールとの誤差が0.2なら深さ調節終了
            if(abs(self.depth-sen_data["depth"]) < 0.2):
                # 見やすさ改善改行
                print("\n")
                # 潜水後も潜り続けてほしいためモータはとめない
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
            self.motor.up_down(MV)

    # 水に潜った状態で前に進む関数
    # 引数 rotate:どのくらい進むかself.rotate(辞書型)のkeyの値 yaw:機体に向き(pidの向き) sen_data:センサの値(辞書型) 
    def diving_advance(self,rotate,yaw,sen_data):
        print("目標回転数\t"+str(rotate))
        # 方位pIdのクラスをインスタンス化
        pid_yaw = PID_yaw()

        # 潜水して進む前のモータ回転数を記録(合計値)
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]
        
        # モータが一定回転するまで無限ループ
        while(True):
            # 現在のモータ回転数を記録
            rot = 0
            for i in range(4):
                rot += sen_data["rot"+str(i)]

            if(debug_flag):
                print("\r回転数\t\t"+str(rot-rot_ini),end="")

            # モータ回転数が規定値を超えていれば終了
            if(rot - rot_ini) >= rotate:
                # 見やすさ改善改行
                print("\n")
                # 潜水して進み終えたら浮上するから潜っているモータと前進しているモータストップ
                # 機体は浮力で自然に浮かぶため浮上の手助けのため止めている
                self.motor.stop()
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])

            # pid暴走した際のセーフティ
            if(sen_data["depth"] > self.depth):
                MV = 0

            # 深さpidの値をモータ反映
            self.motor.up_down(MV)

            # 方向pid
            MV = pid_yaw.go_yaw(yaw,sen_data)
            if(abs(sen_data["x"]-yaw) < 5):
                MV = 0
            
            # 方向pidの値をモータ反映
            self.motor.go_back_each(self.speed+MV,self.speed-MV,self.speed+MV,self.speed-MV)

    # 浮上する関数
    # 引数 sen_data:センサの値(辞書型)
    def ascend(self,sen_data):
        print("浮上開始深さ\t"+str(sen_data["depth"]))
        print("浮上終了深さ\t"+str(self.initial_depth))
        # 目的の深さになるまで無限ループ
        while(True):
            # 目標の深さになったら終了
            if(abs(self.initial_depth-sen_data["depth"]) < 0.2):
                # 見やすさ改善改行
                print("\n")
                # 浮上あとは機体は浮くようになっているためモータストップ
                self.motor.stop_up_down()
                time.sleep(1)
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.initial_depth,sen_data["depth"])
            self.motor.up_down(-20)

    # 浮上後設定した浮上位置か比較し、再潜水を行う関数
    # 引数 maker:浮上位置の設定self.gps_maker(辞書型)のkeyの値 yaw:機体の向き(pidの向き) sen_data:センサの値(辞書型)
    # この関数は時間がなかったため動作未確認です。
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
    # この関数は時間がなかったため動作未確認です。
    def waypoint(self,s_lat,s_lon,g_lat,g_lon):
        g = Geod(ellps='WGS84')
        azimuth, back_azimuth, distance_2d = g.inv(s_lat,s_lon, g_lat, g_lon)
        gps = {'azimuth': azimuth, 'back_azimuth': back_azimuth,'distance_2d': distance_2d}
        return gps

    # モータの回転数合計を見て既定の回転数に達すまでモータ回し続ける
    # 深さを調節するモータはpidで回すので前進後進モータだけ止める
    # 引数 gola:目的の回転回数 sen_data:センサ値(辞書型)
    def rotate_advance(self,rotate,x,sen_data):
        print("目標回転数\t"+str(rotate))
        print("目標方位\t"+str(x)+"\n")
        # 方位pIdのクラスをインスタンス化
        pid_yaw = PID_yaw()
        
        # 前進する前のモータ回転数を記録(合計値)
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]

        # モータが一定回転するまで無限ループ
        while(True):
            # 現在のモータ回転数を記録
            rot = 0
            for i in range(4):
                rot += sen_data["rot"+str(i)]


            # モータ回転数が規定値を超えていれば終了
            if (rot - rot_ini) >= rotate:
                # 見やすさ改善改行
                print("\n")
                # 海上で進んだあとは潜る事が多いので前進モータだけ止める
                self.motor.stop_go_back()
                break

            # 方向pid
            MV = pid_yaw.go_yaw(x,sen_data)
            
            # 方向pidの値をモータ反映
            self.motor.go_back_each(self.speed+MV,self.speed-MV,self.speed+MV,self.speed-MV)

            if(debug_flag):
                print("回転数\t\t"+str(rot-rot_ini)+"\t\t")
                print("現在方位\t"+str(sen_data["x"])+"\t\t")
                print("修正量\t\t"+str(MV)+"\t\t")
                print("\033[4A")

    def diving2(self,goal,sen_data):
        # 潜る前の圧力センサの値を保持(浮上時に使用)
        self.initial_depth = sen_data["depth"]
        self.goal = goal
        while(True):
            # datasheetの分解能から記入したい(0.2)
            # ゴールとの誤差が0.2なら深さ調節終了
            if(abs(self.goal-sen_data["depth"]) < 0.2):
                # 潜水後も潜り続けてほしいためモータはとめない
                break
            if(sen_data["depth"] > self.goal):
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.goal,sen_data["depth"])
            self.motor.up_down(MV)
            #print(MV)
    
    # 水に潜った状態で前に進む関数
    # 引数 rotate:どのくらい進むかself.rotate(辞書型)のkeyの値 yaw:機体に向き(pidの向き) sen_data:センサの値(辞書型) 
    def diving_advance2(self,rotate,yaw,sen_data,cap_flag):
        pid_yaw = PID_yaw()
        # 潜水して進む前のモータ回転数を記録(合計値)
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]
        
        # モータが一定回転したら終了
        while(True):
            #ブイを捉えたら終了
            if cap_flag.value == 1:
                break

            rot = 0
            # 現在のモータ回転数を記録
            for i in range(4):
                rot += sen_data["rot"+str(i)]

            # モータ回転数が規定値を超えていれば終了
            if(rot - rot_ini) >= rotate:
                # 潜水して進み終えたら浮上するから潜っているモータと前進しているモータストップ
                # 機体は浮力で自然に浮かぶため浮上の手助けのため止めている
                self.motor.stop()
                break

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])

            if(sen_data["depth"] > self.depth):
                MV = 0

            self.motor.up_down(MV)

            # 方向pid
            MV = pid_yaw.go_yaw(yaw,sen_data)
            #MV = 0
            if(abs(sen_data["x"]-yaw) < 5):
                MV = 0
            
            #print("\tpid goal : "+str(yaw))
            #print("\tpid sen : "+str(sen_data["x"]))
            #print("\tpid mv : "+str(MV))
            #print("\n\n")
            self.motor.go_back_each(self.speed+MV,self.speed-MV,self.speed+MV,self.speed-MV)

    #カメラの映像から制御する
    #ブイの面積が一定以上の値になったら終了
    #ブイのX軸Y軸を見て方向を制御する
    #X → 0 ~ 650
    #Y → 0 ~ 475
    def camera_advance(self,sen_data,X,Y,S):
        cap_depth = 0
        while(True):

            #bui tikai END
            if S.value > 100000:
                break

            #X軸制御　左にブイがある時
            if X.value < 0:
                self.motor.go_back_each(self.speed,self.speed+10,self.speed,self.speed)
            elif X.value >= 0 and X.value < 65:
                self.motor.go_back_each(self.speed,self.speed+8,self.speed,self.speed)
            elif X.value >= 65 and X.value < 130:
                self.motor.go_back_each(self.speed,self.speed+6,self.speed,self.speed)
            elif X.value >= 130 and X.value < 195:
                self.motor.go_back_each(self.speed,self.speed+4,self.speed,self.speed)
            elif X.value >= 195 and X.value < 260:
                self.motor.go_back_each(self.speed,self.speed+2,self.speed,self.speed)
            elif X.value >= 260 and X.value < 300:
                self.motor.go_back_each(self.speed,self.speed+1,self.speed,self.speed)             
            #ブイが画面の真ん中
            elif X.value >= 300 and X.value < 350:
                self.motor.go_back_each(self.speed+1,self.speed,self.speed,self.speed)    
            #X軸制御　右にブイがある時
            elif X.value >= 350 and X.value < 390:
                self.motor.go_back_each(self.speed+1,self.speed,self.speed,self.speed)
            elif X.value >= 390 and X.value < 455:
                self.motor.go_back_each(self.speed+2,self.speed,self.speed,self.speed)
            elif X.value >= 455 and X.value < 520:
                self.motor.go_back_each(self.speed+4,self.speed,self.speed,self.speed)
            elif X.value >= 520 and X.value < 585:
                self.motor.go_back_each(self.speed+6,self.speed,self.speed,self.speed)
            elif X.value >= 585 and X.value < 650:
                self.motor.go_back_each(self.speed+8,self.speed,self.speed,self.speed)
            elif X.value >= 585 and X.value >= 650:
                self.motor.go_back_each(self.speed+10,self.speed,self.speed,self.speed)
            #例外
            else:
                self.motor.go_back_each(self.speed,self.speed,self.speed,self.speed)
            
            if Y.value >= 30:
                cap_depth += 0.02
                print(cap_depth)
                # 深さpid
                MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
                MV = MV + cap_depth
                self.motor.up_down(MV)

            # 深さpid
            MV = self.pid_depth.go_depth(self.depth,sen_data["depth"])
            MV = MV + cap_depth
            self.motor.up_down(MV)

    def Manual_advance(self,sen_data):
        # 前進する前のモータ回転数を記録(合計値)
        rot_ini = 0
        for i in range(4):
            rot_ini += sen_data["rot"+str(i)]

        # モータが一定回転するまで無限ループ
        while(True):
            # 現在のモータ回転数を記録
            rot = 0
            for i in range(4):
                rot += sen_data["rot"+str(i)]

            print("\r回転数\t\t"+str(rot-rot_ini),end="")

            self.motor.go_back(self.speed)

# ここはこのファイルを単体で実行するとここからプログラムがスタートする。
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
            
            of.rotate_yaw(180,sen_sata)
            #motor.go_back(10)

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
