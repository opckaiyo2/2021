import time
import random

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
    max_correctVal = max_correct
    if abs(yaw2goal - yaw_now) > 180:
      e = 360 - abs(yaw2goal - yaw_now)
    else:
      e = abs(yaw2goal - yaw_now)

    M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
    direction = turn_dir(yaw_now, yaw2goal)

    if M > max_correctVal:
      M = max_correctVal
    elif M < 0:
      M = 0

    correct_yaw = (M * direction)

    M1 = M
    e1 = e
    e2 = e1
    time.sleep(1.0)

    print("目標 : " + str(yaw2goal))
    print("現在 : " + str(yaw_now))
    print("操作量 : " + str(M))
    print("方向+操作量 : " + str(correct_yaw))
    print("")

    yaw_now -= correct_yaw * random.uniform(0.9, 1.1) + random.uniform(-1.0,1.0)

    if(yaw_now < 0):
        yaw_now += 359


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
    
    yam2goal = 180
    yaw_now = 0
    max_correct = 30
    correct_yaw = 0

    while(True):
        fix_yaw(yam2goal,yaw_now,max_correct,correct_yaw)
        


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
