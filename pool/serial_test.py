import sys
import ast
import datetime
import serial

sys.path.append("/home/pi/2021/pool/my_mod")
from motor_controller import Motor

#--------------------------------
# arduinoから一行読み取り辞書型変換
#--------------------------------

if __name__ == "__main__":
    #arduino接続
    ser = serial.Serial('/dev/ttyACM0', 9600)

    motor = Motor()

    power = 10
    print("motor power : ",power)
    
    while True:
        
        try:
            motor.forward_each(power,power,power,power)
            motor.up(power)

            #arduinoから一行読み取り
            String_data = ser.readline().decode('utf-8').rstrip()
            #debagprint
            print(String_data)
            #文字列から辞書型に変換
            dic_date = ast.literal_eval(String_data)
            #debagprint
            print(String_data)
            #辞書型かたtimeを引き出しprint
            print(dic_date["time"])

        except KeyboardInterrupt as key:
            motor.stop()
            break

        except Exception as e:
            motor.stop()
            print("\n")
            print("error : ",e)
            print("\n")