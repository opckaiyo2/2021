import sys
import time
import select
import tty
import termios
import json

sys.path.append("/home/pi/2021/pool/teaching_mod")

from multiprocessing import Process, Manager, Value
from get_data import get_axisData, get_ardData, sort_data
#from remote_process import remote_process
#from camera_process import camera_process
from motor_controller import Motor
from pid_test import PID_yaw, PID_depth
import datetime

pid_yaw = PID_yaw()
pid_depth = PID_depth()

def calc_turnVal(yaw_now):
  val = yaw_now - 180
  if val < 0:
    val += 360
  return val

def isInputData():
  return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

date_time = datetime.datetime.now()
with Manager() as manager:
  axis_data = manager.dict()
  ard_data = manager.dict()
  axis_flg = Value('b', False)
  ard_flg = Value('b', False)
  yaw2goal = Value('i', 0)
  yaw_now = Value('i', 0)
  correct_yaw = Value('i', 0)
  max_correct_yaw = Value('i', 20)
  depth2goal = Value('i', 0)
  depth_now = Value('i', 0)
  correct_depth = Value('i', 0)

  get_axisLog = Process(target=get_axisData,daemon=True, args=(axis_data, axis_flg,))
  get_ardLog = Process(target=get_ardData,daemon=True, args=(ard_data, ard_flg,))
  fix_yaw = Process(target=pid_yaw.fix_yaw, daemon=True, args=(yaw2goal, yaw_now, max_correct_yaw, correct_yaw))
  fix_depth = Process(target=pid_depth.fix_depth, daemon=True, args=(depth2goal, depth_now, correct_depth))

  get_ardLog.start()
  fix_yaw.start()
  fix_depth.start()

  time.sleep(3)
  old_settings = termios.tcgetattr(sys.stdin)

  try:
    motor = Motor()

    log_data = {}

    status = 0
    i = 0
    isPid_forward = 3
    isPid_updown = False

    threshold_rot = [0, 0, 0, 0, 0, 0, 0]
    with open("Teaching_data/teaching.txt", 'r') as f:
      threshold_rot = json.load(f)

    forward_base_speed = 90
    max_correct_yaw.value = 10
    depth_base_speed = 60
    depth2goal.value = 8000

    tty.setcbreak(sys.stdin.fileno())

    print("start")
    while True:
      if isInputData():
        input_key = sys.stdin.read(1)
        if input_key == 'a':
          status += 1
        if input_key == 'r':
          status = -1

      if axis_flg.value == False and ard_flg.value == True:
        log_data = sort_data(axis_data, ard_data)
        yaw_now.value = log_data['ard_deg']['yaw']
        depth_now.value = log_data['depth']
        axis_flg.value = ard_flg.value = False

      if log_data['avg_rot'] >= threshold_rot[i]:
        status += 1
        if i < 5:
          i += 1

      if status == -1:
        motor.stop()

      if status == 0:
        yaw2goal.value = log_data['ard_deg']['yaw']
        start_depth = log_data['depth']
        depth2goal.value = 8000

      elif status == 1:
        isPid_forward = 1

      elif status == 2:
        isPid_updown = True

      elif status == 3:
        isPid_forward = 3
        isPid_updown = False
        yaw2goal.value = calc_turnVal(yaw2goal.value)
        depth2goal.value = start_depth
        status += 1
        
      elif status == 4:
        isPid_updown = True
        isPid_forward = 2
        max_correct_yaw.value = 80
        
      elif status == 5:
        max_correct_yaw.value = 30
        depth2goal.value = 8000
        isPid_updown = True 
        isPid_forward = 1

      elif status == 6:
        depth2goal.value = start_depth

      elif status == 7:
        isPid_updown = False 
        
      elif status == 8:
        isPid_forward = 3
        isPid_updown = False
        motor.stop()
        sys.exit()

      if isPid_forward == 1:
        motor.forward_each(
          forward_base_speed - correct_yaw.value,
          forward_base_speed - correct_yaw.value,
          forward_base_speed + correct_yaw.value,
          forward_base_speed + correct_yaw.value)

      if isPid_forward == 2:
        motor.turn(correct_yaw.value)

      elif isPid_forward == 3:
        motor.forward_stop()


      if isPid_updown == True:
        if depth2goal.value > depth_now.value:
          motor.up(depth_base_speed + correct_depth.value)
          #print("UP")
        elif depth2goal.value < depth_now.value:
          motor.down(depth_base_speed + correct_depth.value)
          #print("DOWN")
      elif isPid_updown == False:
        motor.updown_stop()

  except KeyboardInterrupt:
    motor.stop()

  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
