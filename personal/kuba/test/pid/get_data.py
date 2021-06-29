import sys
import ast
import serial
import time
import datetime
import multiprocessing
sys.path.append('/usr/share/python3-mscl')
import mscl

def get_axisData(axis_data, axis_flg):
  cnt_data = 1
  hz = 100

  connection = mscl.Connection.Serial("/dev/ttyUSB0", 115200)
  node = mscl.InertialNode(connection)
  success = node.ping()
  print(success)

  node.setToIdle()
  estFilterChs = mscl.MipChannels()
  estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_ESTIMATED_LINEAR_ACCEL, mscl.SampleRate.Hertz(hz)))
  estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_ESTIMATED_ANGULAR_RATE, mscl.SampleRate.Hertz(hz)))
  estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_ESTIMATED_ORIENT_EULER, mscl.SampleRate.Hertz(hz)))
  estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_PRESSURE_ALTITUDE, mscl.SampleRate.Hertz(hz)))

  node.setActiveChannelFields(mscl.MipTypes.CLASS_ESTFILTER, estFilterChs)
  node.enableDataStream(mscl.MipTypes.CLASS_ESTFILTER)
  node.resume()

  date_time = datetime.datetime.now()
  start_time = time.time()

  while True:
      packets = node.getDataPackets(500)

      for packet in packets:
          packet.descriptorSet()  # the descriptor set of the packet
          points = packet.data()

          accelX = points[0].as_float()
          accelY = points[1].as_float()
          accelZ = points[2].as_float()

          angX = points[3].as_float()
          angY = points[4].as_float()
          angZ = points[5].as_float()

          roll = points[6].as_float()
          pitch = points[7].as_float()
          yaw = points[8].as_float()

          mag = points[8].as_float()

          pressure = points[9].as_float()

      prog_time = time.time() - start_time

      axis_data['No'] = cnt_data
      axis_data['time'] = '{:2.3f}'.format(prog_time)
      axis_data['gyro'] = {'pitch': '{:2.3f}'.format(pitch),
                          'roll': '{:2.3f}'.format(roll),
                          'yaw': '{:2.3f}'.format(yaw)}
      axis_data['deg_gyro'] = {'pitch': int(180*pitch+180),
                              'roll': int(60*roll+180),
                              'yaw': int(60*yaw+180)}
      axis_data['accel'] = {'x': accelX,
                           'y': accelY,
                           'z': accelZ}
      axis_data['anguler'] = {'x' : angX,
                              'y' : angY,
                              'z' : angZ
                              }
      axis_data['pressure'] = '{:2.3f}'.format(pressure)
      cnt_data += 1

      axis_flg.value = True


def get_ardData(ard_data, ard_flg):
  ser2ard = serial.Serial('/dev/ttyACM0', 115200)
  while True:
    dump = ser2ard.read_until(b"SOF")
    data = ser2ard.readline()
    data = data.decode('unicode-escape')
    data = ast.literal_eval(data)

    ard_data['ard_gyro'] = {'yaw' : data['yaw'],
                            'pitch' : data['pitch'],
                            'roll' : data['roll']}
    ard_data['front_right'] = {'rot' : data['rot1'],
                               'rpm' : data['rpm1'],
                               'thr' : data['thr0']}
    ard_data['front_left'] = {'rot' : data['rot4'],
                               'rpm' : data['rpm4'],
                               'thr' : data['thr0']}
    ard_data['back_right'] = {'rot' : data['rot5'],
                               'rpm' : data['rpm5'],
                               'thr' : data['thr0']}
    ard_data['back_left'] = {'rot' : data['rot0'],
                               'rpm' : data['rpm0'],
                               'thr' : data['thr0']}
    ard_data['center_right'] = {'thr' : data['thr0']}
    ard_data['center_left'] = {'thr' : data['thr0']}
    ard_data['lipoC2'] = data['lipoC2'],
    ard_data['lipoC3S1'] = data['lipoC3S1'],
    ard_data['lipoC3S2'] = data['lipoC3S2'],
    ard_data['lipoC3S3'] = data['lipoC3S3'],
    ard_data['depth'] = data['depth'],

    ard_flg.value = True

def sort_data(axis_data, ard_data):
  log_data = {
    'front_right' : {
      'rot' : ard_data['front_right']['rot'],
      'rpm' : ard_data['front_right']['rpm'],
      'thr' : ard_data['front_right']['thr']
    },
    'front_left' : {
      'rot' : ard_data['front_left']['rot'],
      'rpm' : ard_data['front_left']['rpm'],
      'thr' : ard_data['front_left']['thr']
    },
    'back_right' : {
      'rot' : ard_data['back_right']['rot'],
      'rpm' : ard_data['back_right']['rpm'],
      'thr' : ard_data['back_right']['thr']
    },
    'back_left' : {
      'rot' : ard_data['back_left']['rot'],
      'rpm' : ard_data['back_left']['rpm'],
      'thr' : ard_data['back_left']['thr']
    },
    'center_left' : {
      'thr' : ard_data['center_left']['thr']
    },
    'center_right' : {
      'thr' : ard_data['center_right']['thr']
    },
    'avg_rot' : int((int(ard_data['front_right']['rot']) + int(ard_data['back_right']['rot']) + int(ard_data['front_left']['rot']) + int(ard_data['back_left']['rot']))/4)  ,
    'lipoC2' : ard_data['lipoC2'],
    'lipoC3S1' : ard_data['lipoC3S1'],
    'lipoC3S2' : ard_data['lipoC3S2'],
    'lipoC3S3' : ard_data['lipoC3S3'],
    'axis_gyro' : {
      'yaw' : 0,
      'roll' :0,
      'pitch' :0
    },
    'ard_gyro' : {
      'yaw' : ard_data['ard_gyro']['yaw'],
      'roll' : ard_data['ard_gyro']['roll'],
      'pitch' : ard_data['ard_gyro']['pitch']
    },
    'axis_deg' : {
      'yaw' : 0,
      'roll' : 0,
      'pitch' : 0
    },
    'ard_deg' : {
      'yaw' : int(ard_data['ard_gyro']['yaw']) + 180,
      'roll' : int(ard_data['ard_gyro']['roll']) + 180,
      'pitch' : int(ard_data['ard_gyro']['pitch']) + 180
    },
    'axis_accel' : {
      'x' : 0,
      'y' : 0,
      'z' : 0
    },
    'axis_anguler' : {
      'x' : 0,
      'y' : 0,
      'z' : 0
    },
    'axis_pressure' : 0,
    'depth' : int(float(ard_data['depth'][0]) * 10000),
  }

  return log_data
