import sys
import ast
import datetime
import serial

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        
        try:
            String_data = ser.readline().decode('utf-8').rstrip()
            dic_date = ast.literal_eval(String_data)
            print(String_data)
            print(dic_date["time"])

            if dic_date:
                break
        except KeyboardInterrupt as key:
            break

        except:
            pass

    ser.close()

class my_serial:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def recive_date(self):  
        while True:
            
            try:
                self.ser.write(b"send\n")
                self.ser.flush()
                String_data = self.ser.readline().decode('utf-8').rstrip()
                print(String_data)
                dic_date = ast.literal_eval(String_data)

                if dic_date:
                    return dic_date
            except KeyboardInterrupt as key:
                print("my_serial.py my_serial KeyboardInterrupt break")
                break

            except Exception as e:
                print("my_serial except [" + str(e) + "]")
                pass
        self.ser.close()