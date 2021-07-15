import time
import sys

sys.path.append("/home/pi/2021/pool/my_mod")
from motor_controller import Motor

#-----------------------------------------
# モータを順番に一つずつ正転逆転させるprogram
#-----------------------------------------

if __name__ == "__main__":
    

    motor = Motor()

    try:
        while(True):
            #""" ここの#を入れたり消したりでコメントアウトを切り替えられる
            print("motor_power 10")
            
            motor.forward_each(10,0,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(-10,0,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,10,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,-10,0,0)
            time.sleep(2.0)
            motor.stop()
            
            motor.forward_each(0,0,10,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,-10,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,0,10)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,0,-10)
            time.sleep(2.0)
            motor.stop()

            motor.up(10)
            time.sleep(2.0)
            motor.stop()

            motor.down(10)
            time.sleep(2.0)
            motor.stop()
            #"""

    except KeyboardInterrupt:
        motor.stop()
        #pass
    except:
        motor.stop()
        #pass

