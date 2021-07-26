import time
import sys

sys.path.append("/home/pi/2021/pool/my_mod")
from motor_controller import Motor

#-----------------------------------------
# モータを順番に一つずつ正転逆転させるprogram
#-----------------------------------------

if __name__ == "__main__":
    

    motor = Motor()

    power = 30

    try:
        while(True):
            #""" ここの#を入れたり消したりでコメントアウトを切り替えられる
            print("motor_power ",power)
            
            motor.forward_each(power,0,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(-1*power,0,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,power,0,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,-1*power,0,0)
            time.sleep(2.0)
            motor.stop()
            
            motor.forward_each(0,0,power,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,-1*power,0)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,0,power)
            time.sleep(2.0)
            motor.stop()

            motor.forward_each(0,0,0,-1*power)
            time.sleep(2.0)
            motor.stop()

            motor.up(power)
            time.sleep(2.0)
            motor.stop()

            motor.down(power)
            time.sleep(2.0)
            motor.stop()
            #"""

    except KeyboardInterrupt:
        motor.stop()
        #pass
    except:
        motor.stop()
        #pass

