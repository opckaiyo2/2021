import sys
import ast
import datetime
import serial

#--------------------------------
# arduinoから一行読み取り辞書型変換
#--------------------------------

if __name__ == "__main__":
    #arduino接続
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        
        try:
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
            break

        except Exception as e:
            print("\n")
            print("error : ",e)
            print("\n")