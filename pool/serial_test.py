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
    filiname = "/home/pi/2021/pool/my_log/" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt")
    #arduino接続
    ser = serial.Serial('/dev/ttyACM0', 115200)

    motor = Motor()

    power = 30
    print("motor power : ",power)
    
    while True:
        
        try:
            #motor.forward_each(power,power,power,power)
            #motor.up(power)

            #arduinoから一行読み取り
            String_data = ser.readline().decode('utf-8').rstrip()
            #文字列から辞書型に変換
            #print(String_data)
            dic_date = ast.literal_eval(String_data)
            #debagprint
            print(dic_date["x"])

            #motor.forward_each(power,power,power,power)

            with open(filiname, 'a') as f:
                f.writelines(str(dic_date))
                f.writelines("\n")


        except KeyboardInterrupt as key:
            motor.stop()
            break

        except Exception as e:
            motor.stop()
            print("\n")
            print("error : ",e)
            print("\n")
