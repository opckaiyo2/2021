import time
from motor_controller import Motor

if __name__ == "__main__":
    motor = Motor()

    try:
        while(True):
            
            motor.forward_each(30,0,0,0)
            time.sleep(2.0)
            motor.stop()
            motor.forward_each(0,30,0,0)
            time.sleep(2.0)
            motor.stop()
            motor.forward_each(0,0,30,0)
            time.sleep(2.0)
            motor.stop()
            motor.forward_each(0,0,0,30)
            time.sleep(2.0)
            motor.stop()
            motor.up(30)
            time.sleep(2.0)
            motor.stop()
            motor.down(30)
            time.sleep(2.0)
            motor.stop()

    except KeyboardInterrupt:
        motor.stop()
    except:
        motor.stop()
        

