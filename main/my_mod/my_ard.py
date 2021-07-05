import ast
import serial
import multiprocessing 

def get_sen(sen_data):
    # arduinoのピン通信速度設定
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        try:
            # arduinoから送られてきたデータを一行取得デコード
            String_data = ser.readline().decode('utf-8').rstrip()
            # 文字型から辞書型に変換
            dic_date = ast.literal_eval(String_data)
            # multiprocessでprocess間値共有 main.pyで設定
            sen_data = dic_date
        except KeyboardInterrupt as key:
            break

        except Exception as e:
            print("\n")
            print("my_ard.py get_sen try error : ",e)
            print("\n")

if __name__ == "__main__":
    pass