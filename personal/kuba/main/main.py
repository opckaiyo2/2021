import sys
import serial
import ast
import os

sys.path.append("/home/pi/2021/kuba/my_mod")
from my_serial import my_serial

if __name__ == "__main__":
    serial = my_serial()

    try:
        dict_sen = serial.recive_date()
        print(dict_sen)

    except KeyboardInterrupt as key:
        print("main.py main KeyboardInterrupt break")