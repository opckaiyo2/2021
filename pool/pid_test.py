import time
import random
import serial
import ast
import sys

sys.path.append("/home/pi/2021/pool/my_mod")
from motor_controller import Motor

class PID_yaw:
  def __init__(self):
    self.e = 0
    self.e1 = 0
    self.e2 = 0
    self.M = 0
    self.M1 = 0

  def fix_yaw(self,yaw2goal, yaw_now, max_correct, correct_yaw):
    motor = Motor()

    #"""
    Kp = 0.1
    Ki = 0.01
    Kd = 0.001
    """
    Kp = 0.001
    Ki = 0.01
    Kd = 0.5
    #"""


    max_correctVal = max_correct
    if abs(yaw2goal - yaw_now) > 180:
      self.e = 360 - abs(yaw2goal - yaw_now)
    else:
      self.e = abs(yaw2goal - yaw_now)

    self.M = self.M1 + Kp * (self.e-self.e1) + Ki * self.e + Kd * ((self.e-self.e1) - (self.e1-self.e2))
    direction = self.turn_dir(yaw_now, yaw2goal)

    if self.M > max_correctVal:
      self.M = max_correctVal
    elif self.M < 0:
      self.M = 0

    correct_yaw = (self.M * direction)

    self.e2 = self.e1
    self.e1 = self.e
    self.M1 = self.M
    #time.sleep(1.0)

    """
    print("目標 : " + str(yaw2goal))
    print("現在 : " + str(yaw_now))
    print("操作量 : " + str(self.M))
    print("方向+操作量 : " + str(correct_yaw))
    print("")
    """

    print("M : ",self.M)
    motor.turn(self.M)


  def turn_dir(self,yaw_now, goal2yaw):
    direction = 0

    if yaw_now <= 180:
      if -180 < yaw_now - goal2yaw < 0:
        direction = -1
      else:
        direction = 1

    elif yaw_now <= 360:
      if 0 < yaw_now - goal2yaw < 180:
        direction = 1
      else:
        direction = -1
      
    return direction 

class PID_depth:
  def __init__(self):
    self.e = 0
    self.e1 = 0
    self.e2 = 0
    self.M = 0
    self.M1 = 0

  def fix_depth(self,depth2goal, depth_now, correct_depth):

    M = 0.00
    M1 = 0.00
    e = 0.00
    e1 = 0.00
    e2 = 0.00
    #Kp = 0.1
    #Ki = 0.01
    #Kd = 0.001

    Kp = 0.001
    Ki = 0.01
    Kd = 0.5

    while True:
      max_correctVal = 10
      self.e = abs(depth2goal.value - depth_now.value)

      self.M = self.M1 + Kp * (self.e-self.e1) + Ki * self.e + Kd * ((self.e-self.e1) - (self.e1-self.e2))

      if self.M > max_correctVal:
        self.M = max_correctVal
      elif self.M < 0:
        self.M = 0

      correct_depth.value = int(self.M)

      self.M1 = self.M
      self.e1 = self.e
      self.e2 = self.e1
      time.sleep(0.5)




if __name__ == '__main__':
  #;alskfjbvsanfruv haspfvnjhspfrvna
  motor = Motor()

  yam2goal = 0
  yaw_now = 0
  max_correct = 30
  correct_yaw = 0

  pid = PID_yaw()

  while(True):
    ser = serial.Serial('/dev/ttyACM0', 9600)

    while(True):
      try:
        String_data = ser.readline().decode('utf-8').rstrip()
        dic_date = ast.literal_eval(String_data)
        #print(dic_date)
        yaw_now = int(dic_date["yaw"])
        break

      except KeyboardInterrupt:
        motor.stop()  
        break
      
      except Exception as e:
        print("serial error : ",e)
        pass

    try:

      pid.fix_yaw(yam2goal,yaw_now,max_correct,correct_yaw)
    
    except KeyboardInterrupt:
      motor.stop()
      break

    except Exception as e:
      motor.stop()
      print(e)
      break
