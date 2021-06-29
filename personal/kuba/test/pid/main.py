from multiprocessing import Process, Manager, Value
from get_data import get_axisData, get_ardData, sort_data
from motor_controller import Motor
from pid import fix_yaw, fix_depth

with Manager() as manager:
  ard_data = manager.dict()
  ard_flg = Value('b', False)
  yaw2goal = Value('i', 0)
  yaw_now = Value('i', 0)
  correct_yaw = Value('i', 0)
  max_correct_yaw = Value('i', 20)

  get_ardLog = Process(target=get_ardData,daemon=True, args=(ard_data, ard_flg,))
  fix_yaw = Process(target=fix_yaw, daemon=True, args=(yaw2goal, yaw_now, max_correct_yaw, correct_yaw))

  get_ardLog.start()
  fix_yaw.start()
  
  forward_base_speed = 0

  try:
    motor = Motor()

    while(True):
      print(ard_data)
      print(correct_yaw.value)
      motor.forward_each(
        forward_base_speed - correct_yaw.value,
        forward_base_speed - correct_yaw.value,
        forward_base_speed + correct_yaw.value,
        forward_base_speed + correct_yaw.value
      )

  except KeyboardInterrupt:
    motor.stop()

  except:
    motor.stop()