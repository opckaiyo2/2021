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

  #remote = Process(target=remote_process, daemon=True, args=("6000",))
  #camera = Process(target=camera_process, daemon=True, args=("5000",))
  get_axisLog = Process(target=get_axisData,daemon=True, args=(axis_data, axis_flg,))
  get_ardLog = Process(target=get_ardData,daemon=True, args=(ard_data, ard_flg,))
  #fix_yaw = Process(target=fix_yaw, daemon=True, args=(yaw2goal, yaw_now, max_correct_yaw, correct_yaw))
  #fix_depth = Process(target=fix_depth, daemon=True, args=(depth2goal, depth_now, correct_depth))
  fix_yaw = Process(target=pid_yaw.fix_yaw, daemon=True, args=(yaw2goal, yaw_now, max_correct_yaw, correct_yaw))
  fix_depth = Process(target=pid_depth.fix_depth, daemon=True, args=(depth2goal, depth_now, correct_depth))

  #remote.start()
  #camera.start()
  get_axisLog.start()
  get_ardLog.start()
  fix_yaw.start()
  fix_depth.start()

  time.sleep(3)
  old_settings = termios.tcgetattr(sys.stdin)

  try:
    filename = 'teaching'
    motor = Motor()

    log_data = {}

    status = -1
    isPid_forward = 3
    isPid_updown = False

    threshold_rot = [0, 0, 0, 0, 0, 0, 0]
    front_right_rot = [0, 0, 0, 0, 0, 0, 0]
    front_left_rot = [0, 0, 0, 0, 0, 0, 0]
    back_right_rot = [0, 0, 0, 0, 0, 0, 0]
    back_left_rot = [0, 0, 0, 0, 0, 0, 0]
    center_right_rot = [0, 0, 0, 0, 0, 0, 0]
    center_left_rot = [0, 0, 0, 0, 0, 0, 0]

    forward_base_speed = 70
    max_correct_yaw.value = 20
    depth_base_speed = 60

    tty.setcbreak(sys.stdin.fileno())

    while True:
      if isInputData():
        input_key = sys.stdin.read(1)
        if input_key == 'a':
          status += 1

      print("status", status)

      if axis_flg.value == False and ard_flg.value == True:
        log_data = sort_data(axis_data, ard_data)
        yaw_now.value = log_data['ard_deg']['yaw']
        depth_now.value = log_data['depth']
        axis_flg.value = ard_flg.value = False

      if status == 0:
        #set start value
        print("set start value")
        log_data = sort_data(axis_data, ard_data)
        yaw2goal.value = log_data['ard_deg']['yaw']
        start_depth = log_data['depth']
        depth2goal.value = start_depth

      elif status == 1:
       # print("correct_yaw", correct_yaw.value)
       # print("correct_depth", correct_depth.value)
       # print("start")
        print("start")
        isPid_forward = 1

      elif status == 2:
        print("record rot[0]")
        #ロータリエンコーダの値をthreshold_rot[0]に記録
        threshold_rot[0] = log_data['avg_rot']
        front_right_rot[0] = ard_data['front_right']['rot']
        front_left_rot[0] = ard_data['front_left']['rot']
        back_right_rot[0] = ard_data['back_right']['rot']
        back_left_rot[0] = ard_data['back_left']['rot']
        center_right_rot[0] = ard_data['center_left']['thr']
        center_left_rot[0] = ard_data['center_right']['thr']
        status += 1

      elif status == 3:
        print("donw and forward")
        #depth2goal.value = start_depth
        depth2goal.value = 8000
        isPid_updown = True
        
      elif status == 4:
        print("record rot[1]")
        #ロータリエンコーダの値をthreshold_rot[1]に記録
        threshold_rot[1] = log_data['avg_rot']
        front_right_rot[1] = ard_data['front_right']['rot']
        front_left_rot[1] = ard_data['front_left']['rot']
        back_right_rot[1] = ard_data['back_right']['rot']
        back_left_rot[1] = ard_data['back_left']['rot']
        center_right_rot[1] = ard_data['center_left']['thr']
        center_left_rot[1] = ard_data['center_right']['thr']
        status += 1

      elif status == 5:
        print("set set_turnyaw start_depth")
        yaw2goal.value = calc_turnVal(yaw2goal.value)
        print("yaw2goal_turnVal", yaw2goal.value)
        depth2goal.value = start_depth
        status += 1

      elif status == 6:
        print("turn and up")
        #turn and up
        max_correct_yaw.value = 80
        isPid_forward = 2

      elif status == 7:
        #ロータリエンコーダの値をthreshold_rot[2]に記録
        threshold_rot[2] = log_data['avg_rot']
        front_right_rot[2] = ard_data['front_right']['rot']
        front_left_rot[2] = ard_data['front_left']['rot']
        back_right_rot[2] = ard_data['back_right']['rot']
        back_left_rot[2] = ard_data['back_left']['rot']
        center_right_rot[2] = ard_data['center_left']['thr']
        center_left_rot[2] = ard_data['center_right']['thr']
        print("set max_correct")
        max_correct_yaw.value = 20
        depth2goal.value = start_depth
        depth2goal.value = 8000
        status += 1

      elif status == 8:
        print("down and forward")
        isPid_forward = 1

      elif status == 9:
        print("up")
        depth2goal.value = start_depth

      elif status == 10:
        print("record rot[3]")
        #ロータリエンコーダの値をthreshold_rot[3]に記録
        threshold_rot[3] = log_data['avg_rot']
        front_right_rot[3] = ard_data['front_right']['rot']
        front_left_rot[3] = ard_data['front_left']['rot']
        back_right_rot[3] = ard_data['back_right']['rot']
        back_left_rot[3] = ard_data['back_left']['rot']
        center_right_rot[3] = ard_data['center_left']['thr']
        center_left_rot[3] = ard_data['center_right']['thr']
        status += 1
      
      elif status == 11:
        print("forward")
        isPid_updown = False 

      elif status == 12:
        #ロータリエンコーダの値をthreshold_rot[4]に記録
        threshold_rot[4] = log_data['avg_rot']
        front_right_rot[4] = ard_data['front_right']['rot']
        front_left_rot[4] = ard_data['front_left']['rot']
        back_right_rot[4] = ard_data['back_right']['rot']
        back_left_rot[4] = ard_data['back_left']['rot']
        center_right_rot[4] = ard_data['center_left']['thr']
        center_left_rot[4] = ard_data['center_right']['thr'] 
        status += 1
        
      elif status == 13:
        print("stop")
        isPid_forward = 3
        isPid_updown = False
        motor.stop()
        #ロータリエンコーダの値をthreshold_rot[5]に記録
        threshold_rot[5] = log_data['avg_rot']
        front_right_rot[5] = ard_data['front_right']['rot']
        front_left_rot[5] = ard_data['front_left']['rot']
        back_right_rot[5] = ard_data['back_right']['rot']
        back_left_rot[5] = ard_data['back_left']['rot']
        center_right_rot[5] = ard_data['center_left']['thr']
        center_left_rot[5] = ard_data['center_right']['thr']

        #filenameにthreshold_rotを上書き
        print("write rot to file")
        with open('/home/pi/2021/pool/Teaching_data/teaching.txt', mode = 'w') as f:
          json.dump(threshold_rot, f)
        with open('/home/pi/2021/pool/Teaching_data/front_right.txt', mode = 'w') as f:
          json.dump(front_right_rot, f)
        with open('/home/pi/2021/pool/Teaching_data/front_left.txt', mode = 'w') as f:
          json.dump(front_left_rot, f)
        with open('/home/pi/2021/pool/Teaching_data/back_right.txt', mode = 'w') as f:
          json.dump(back_right_rot, f)
        with open('/home/pi/2021/pool/Teaching_data/center_right.txt', mode = 'w') as f:
          json.dump(center_right_rot, f)
        with open('/home/pi/2021/pool/Teaching_data/center_left.txt', mode = 'w') as f:
          json.dump(center_left_rot, f)

        status = -1

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

        print("correct_yaw", correct_yaw.value)
        print("correct_depth", correct_depth.value)

      print("\n")
      print(ard_data['front_right']['rot'])
      print(ard_data['front_left']['rot'])
      print(ard_data['back_right']['rot'])
      print(ard_data['back_left']['rot'])
      print("\n")

  except KeyboardInterrupt:
    motor.stop()

  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
