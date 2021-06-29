import sys
import ast
import datetime
import serial

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        
        try:
            String_data = ser.readline().decode('utf-8').rstrip()
            print(String_data)
            dic_date = ast.literal_eval(String_data)
            print(String_data)
            print(dic_date["time"])

        except KeyboardInterrupt as key:
            break

        except:
            pass