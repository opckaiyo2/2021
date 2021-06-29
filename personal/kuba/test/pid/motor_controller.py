import Adafruit_PCA9685
import time

class Motor:
    def __init__(self):
        
        self.pwm = Adafruit_PCA9685.PCA9685()

        self.motor = {

                #motor position
                #pin : motor pin
                #dir : controll direction pin
                #cor : correct value

                'front_right' : {
                    'pin' : 7,
                    'dir' : 13,
                    'cor' : 1,
                },

                'center_right' : {
                    'pin' : 9,
                    'dir' : 14,
                    'cor' : 1,
                },

                'back_right' : {
                    'pin' : 8,
                    'dir' : 4,
                    'cor' : 1,
                },

                'front_left' : {
                    'pin' : 12,
                    'dir' : 6,
                    'cor' : 1,
                },

                'center_left' : {
                    'pin' : 10,
                    'dir' : 5,
                    'cor' : 1,
                },

                'back_left' : {
                    'pin' : 11,
                    'dir' : 15,
                    'cor' : 1,
                },
            }
    
    #convert value
    def parsent2val(self, val):
        if val == 0:
            direction = 1
            pwm_val = 0

        elif val > 0:
            direction = 4000
            pwm_val = int(val * 4000 / 100)
        
        elif val < 0:
            direction = 1
            pwm_val = int(val * 4000 / -100)

        return pwm_val, direction

    #Controll motor (val : from -100 to 100)
    #Usage : Motor.Controll(Motor.motor['back_left'], 50)
    #        Motor.Controll(Motor.motor['center_right'], -30)
    def Controll(self, motor, val):
        #conversion val
        pwm_val, direction = self.parsent2val(val)
        #set direction
        self.pwm.set_pwm(motor['pin'], 0, pwm_val)
        #set pwm
        self.pwm.set_pwm(motor['dir'], 0, direction)

    def front_controll(self, val):
        self.Controll(self.motor['front_right'], self.motor['front_right']['cor'] * -val)
        self.Controll(self.motor['front_left'], self.motor['front_left']['cor'] * val)

    def back_controll(self, val):
        self.Controll(self.motor['back_right'], self.motor['back_right']['cor'] * -val)
        self.Controll(self.motor['back_left'], self.motor['back_left']['cor'] * val)

    def free_controll(self, val):
        self.Controll(self.motor['front_right'], val)
        self.Controll(self.motor['center_right'], val)
        self.Controll(self.motor['back_right'], val)
        self.Controll(self.motor['front_left'], val)
        self.Controll(self.motor['center_left'], val)
        self.Controll(self.motor['back_left'], val)
        
    def forward(self, val):
        self.Controll(self.motor['front_right'], self.motor['front_right']['cor'] * -val)
        self.Controll(self.motor['back_right'], self.motor['back_right']['cor'] * -val)
        self.Controll(self.motor['front_left'], self.motor['front_left']['cor'] * val)
        self.Controll(self.motor['back_left'], self.motor['back_left']['cor'] * val)
    def back(self, val):
        self.Controll(self.motor['front_right'], self.motor['front_right']['cor'] * val)
        self.Controll(self.motor['back_right'], self.motor['back_right']['cor'] * val)
        self.Controll(self.motor['front_left'], self.motor['front_left']['cor'] * -val)
        self.Controll(self.motor['back_left'], self.motor['back_left']['cor'] * -val)
    def turn(self, val):
        self.Controll(self.motor['front_right'], self.motor['front_right']['cor'] * val)
        self.Controll(self.motor['back_right'], self.motor['back_right']['cor'] * val)
        self.Controll(self.motor['front_left'], self.motor['front_left']['cor'] * val)
        self.Controll(self.motor['back_left'], self.motor['back_left']['cor'] * val)
    def up(self, val):
        self.Controll(self.motor['center_right'], self.motor['center_right']['cor'] * val)
        self.Controll(self.motor['center_left'], self.motor['center_left']['cor'] * -val)
    def down(self, val):
        self.Controll(self.motor['center_right'], self.motor['center_right']['cor'] * -val)
        self.Controll(self.motor['center_left'], self.motor['center_left']['cor'] * val)
    def stop(self):
        self.Controll(self.motor['front_right'], 0)
        self.Controll(self.motor['center_right'], 0)
        self.Controll(self.motor['back_right'], 0)
        self.Controll(self.motor['front_left'], 0)
        self.Controll(self.motor['center_left'], 0)
        self.Controll(self.motor['back_left'], 0)
    def forward_each(self, fr_val, br_val, fl_val, bl_val):
        self.Controll(self.motor['front_right'], self.motor['front_right']['cor'] * -fr_val)
        self.Controll(self.motor['back_right'], self.motor['back_right']['cor'] * -br_val)
        self.Controll(self.motor['front_left'], self.motor['front_left']['cor'] * fl_val)
        self.Controll(self.motor['back_left'], self.motor['back_left']['cor'] * bl_val)
    def forward_stop(self):
        self.Controll(self.motor['front_right'], 0)
        self.Controll(self.motor['back_right'], 0)
        self.Controll(self.motor['front_left'], 0)
        self.Controll(self.motor['back_left'], 0)
    def updown_stop(self):
        self.Controll(self.motor['center_right'], 0)
        self.Controll(self.motor['center_left'], 0)

    def help(self):

        print("---correct value---")
        print("front_right : ", self.motor['front_right']['cor'])
        print("center_right", self.motor['center_right']['cor'])
        print("back_right", self.motor['center_right']['cor'])
        print("front_left", self.motor['back_right']['cor'])
        print("center_left", self.motor['front_left']['cor'])
        print("back_left", self.motor['center_left']['cor'])
        print("------------------")

        print("0 : stop")
        print("1 : forward")
        print("2 : back")
        print("3 : turn")
        print("4 : up")
        print("5 : down")
        print("6 : front_controll")
        print("7 : back_controll")
        print("8 : free_controll")
        print("9 : help")
        

if __name__ == '__main__':
    myMotor = Motor()
    num = 0
    parsent_val = 0

    myMotor.help()

    while True:
        try:
            num = int(input("input = "))
            if num != 0:
                parsent_val = int(input("output(%) = "))
             
            if num == 0 :
                myMotor.stop()
            elif num == 1 :
                myMotor.forward(parsent_val)
            elif num == 2 :
                myMotor.back(parsent_val)
            elif num == 3 :
                myMotor.turn(parsent_val) 
            elif num == 4 :
                myMotor.up(parsent_val)
            elif num == 5 :
                myMotor.down(parsent_val)
            elif num == 6 :
                myMotor.front_controll(parsent_val)
            elif num == 7 :
                myMotor.back_controll(parsent_val)
            elif num == 8 :
                myMotor.free_controll(parsent_val)
            elif num == 9 :
                myMotor.help()
            else:
                print("Error : Command not exist.")
                
            

        except KeyboardInterrupt:
           myMotor.stop() 
           break
