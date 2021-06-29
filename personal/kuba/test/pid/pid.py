from sys import exec_prefix
import time
from multiprocessing import Value
import serial
import ast
from my_motor import spinturn, stop

def fix_yaw(yaw2goal, yaw_now, max_correct, correct_yaw):

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
    max_correctVal = max_correct.value
    if abs(yaw2goal.value - yaw_now.value) > 180:
      e = 360 - abs(yaw2goal.value - yaw_now.value)
    else:
      e = abs(yaw2goal.value - yaw_now.value)

    M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
    direction = turn_dir(yaw_now.value, yaw2goal.value)

    if M > max_correctVal:
      M = max_correctVal
    elif M < 0:
      M = 0

    correct_yaw.value = int(M * direction)

    M1 = M
    e1 = e
    e2 = e1
    time.sleep(0.1)

def turn_dir(yaw_now, goal2yaw):
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
        
if __name__ == '__main__':
  ser = serial.Serial('/dev/ttyACM0', 9600)

  yaw2goal = 30

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

    try:
      String_data = ser.readline().decode('utf-8').rstrip()
      dic_date = ast.literal_eval(String_data)
      print(dic_date['yaw'])

      max_correctVal = 10
      if abs(yaw2goal - dic_date['yaw']) > 180:
        e = 360 - abs(yaw2goal - dic_date['yaw'])
      else:
        e = abs(yaw2goal - dic_date['yaw'])

      M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
      direction = turn_dir(dic_date['yaw'], yaw2goal)

      if M > max_correctVal:
        M = max_correctVal
      elif M < 0:
        M = 0

      spinturn(int(M * direction))

      M1 = M
      e1 = e
      e2 = e1
      time.sleep(0.1)
    
    except KeyboardInterrupt:
      stop()
      break

    except Exception as e:
      print("error : ",e)


def fix_depth(depth2goal, depth_now, correct_depth):

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
    e = abs(depth2goal.value - depth_now.value)

    M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))

    if M > max_correctVal:
      M = max_correctVal
    elif M < 0:
      M = 0

    correct_depth.value = int(M)

    M1 = M
    e1 = e
    e2 = e1
    time.sleep(0.5)
