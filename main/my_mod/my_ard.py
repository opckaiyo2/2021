import ast
import serial
import multiprocessing 

def get_sen(ard_data):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        try:
            String_data = ser.readline().decode('utf-8').rstrip()
            dic_date = ast.literal_eval(String_data)
            ard_data = dic_date
        except KeyboardInterrupt as key:
            break

        except Exception as e:
            print("\n")
            print("my_ard.py get_sen try error : ",e)
            print("\n")

if __name__ == "__main__":
    pass