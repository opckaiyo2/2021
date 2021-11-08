#coding: utf-8
import configparser
import termios
import tty
import sys
import time

# 自作関数の場所をsystempathに追加
sys.path.append("/home/pi/2021/tinou/main/my_mod")
# motor制御
from my_motor import Motor

def Manual(sen_data):
    motor = Motor()

    while(not('endtime' in sen_data)):
        pass

    # 設定ファイル読み込み-------------------------------------------

    INI_FILE = "/home/pi/2021/main/config/config.ini"
    inifile = configparser.SafeConfigParser()
    inifile.read(INI_FILE,encoding="utf-8")

    log_flag = inifile.getboolean("manual", "log_flag")
    
    # 設定ファイル読み込み-------------------------------------------

    power = 30
    ch_state = 0
    rot = 0
    log_rotate = {"test":0}
    log_time = {}
    start = time.time()

    while(True):
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            if ch == "w":
                motor.go_back(power)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_go_back"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_go_back " + str(power)
            elif ch == "s":
                motor.go_back(power*-1)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_go_back"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_go_back " + str(power*-1)
            elif ch == "q":
                motor.spinturn(power)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_spinturn"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_spinturn " + str(power)
            elif ch == "e":
                motor.spinturn(power*-1)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_spinturn"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_spinturn " + str(power*-1)
            elif ch == "-":
                power -= 10
                print("power : "+str(power))
            elif ch == "+":
                power += 10
                print("power : "+str(power))
            elif ch == "r":
                motor.up_down(power)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_up_down"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_up_down " + str(power)
            elif ch == "f":
                motor.up_down(power*-1)
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_up_down"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_up_down " + str(power*-1)
            elif ch == "u":
                motor.stop_go_back()
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_goback_stop"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_goback_stop"
            elif ch == "j":
                motor.stop_up_down()
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_updown_stop"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_updown_stop"
            elif ch == "m":
                motor.stop()
                for i in range(4): rot += sen_data["rot"+str(i)]
                ch_state += 1
                log_rotate["motor_stop"+str(ch_state)] = rot
                log_time[time.time()-start] = "motor_stop"
            else:
                print("対応した操作がありません")
                print("w : 前進")
                print("s : 後進")
                print("q : 旋回左")
                print("e : 旋回右")
                print("- : モータ出力 -10")
                print("+ : モータ出力 +10")
                print("r : 潜水")
                print("f : 浮上")
                print("u : 前進後進モータstop")
                print("j : 潜水浮上モータstop")
                print("m : 全てもモータstop")

        except Exception as e:
            print(log_rotate)
            motor.stop()