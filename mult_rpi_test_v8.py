# v8 --> comments to clarify what commands do

# serves as functional proof of concept to show wiring and coding works

# implemented a class to make multiple axis easier to navigate

#
# Developing code to run MULTIPLE stepper driver + stepper motor system
from time import sleep # note: sleep input units = seconds
import RPi.GPIO as GPIO

# I/O Pins

# MOTOR 1
PUL1 = 17 
DIR1 = 22
ENA1 = 23

# MOTOR 2
PUL2 = 24
DIR2 = 25
ENA2 = 26

# MOTOR 3
PUL3 = 16 
DIR3 = 20
ENA3 = 21


pul_delay = 0.00005 # seconds/pulse, sets speed
step_cycle_input = 2000 # Subject to change...
 

class Motor:
    def __init__(self, p, d, e):
        self.PUL = p
        self.DIR = d
        self.ENA = e

    def setup(self):    # sets up the motors
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)

    def setDir(self,input = ""):    # set direction of motor
        if input == "low":
            GPIO.output(self.DIR, GPIO.LOW)
            print("Direction set to LOW")
        elif input =="high":
            GPIO.output(self.DIR, GPIO.HIGH)
            print("Direction set to HIGH")
    
    def enaMotor(self, input = ""):
        if input == "enable":
            GPIO.output(self.ENA, GPIO.HIGH)
            print("ENABLED Motor") 
        elif input == "disable":
            GPIO.output(self.ENA, GPIO.LOW)
            print("DISABLED Motor")
            
    def flipDir(self):
        if GPIO.input(self.DIR) ==  1:
            GPIO.output(self.DIR, GPIO.LOW)
        elif GPIO.input(self.DIR) == 0:
            GPIO.output(self.DIR, GPIO.HIGH)
            
        print("Flipped Directions...")

    def step(self):     # one cycle step
        GPIO.output(self.PUL,GPIO.HIGH)

        sleep(pul_delay)

        GPIO.output(self.PUL,GPIO.LOW)

        sleep(pul_delay)        

    def run(self):  # walk in the direction
        for x in range(step_cycle_input):    
            self.step()
        print("Motor Stopped...")   

    def jog(self):
        self.run()
        self.flipDir()
        self.run()
        self.flipDir()




def main(): 

    # Set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # MOTOR 1
    motor1 = Motor(PUL1,DIR1,ENA1)
    motor1.setup()

    # MOTOR 2
    motor2 = Motor(PUL2,DIR2,ENA2)
    motor2.setup()

    # MOTOR 3
    motor3 = Motor(PUL3,DIR3,ENA3)
    motor3.setup()

    
    
    print('Initialization Completed')
    while True:     # continuously asking for user input
        user_input = raw_input("Enter command:") 

        if user_input == 'run1': # runs motor #1 with the given inputs and direction
            print("Motor GO!") 
            motor1.run()
            print("Motor Stopped...")
        elif user_input == "run2": # runs motor #2 with the given inputs and direction
            print("Motor GO!") 
            motor2.run()
            print("Motor Stopped...")
        elif user_input == "run3":  # runs motor #3 with the given inputs and direction
            print("Motor GO!") 
            motor3.run()
            print("Motor Stopped...")

        elif user_input == 'disable':   # disables all motors, will not move upon run inputs
            motor1.enaMotor(user_input)
            motor2.enaMotor(user_input)
            motor3.enaMotor(user_input)
        elif user_input == 'enable':    # enables all motors, will allow movemen upon run inputs
            motor1.enaMotor(user_input)
            motor2.enaMotor(user_input)
            motor3.enaMotor(user_input)
        elif user_input == 'flip':  # flips direction of ALL motors at the same time
            motor1.flipDir()
            motor2.flipDir()
            motor3.flipDir()
        elif user_input =='jog1':   # jog motor #1 back and forth
            motor1.jog()
        elif user_input == 'jog2':  # jog motor #2 back and forth
            motor2.jog()
        elif user_input == 'jog3':  # jog motor #3 back and forth
            motor3.jog()
        elif user_input == 'runall':    # runs all motors 
            for x in range(step_cycle_input):  

                GPIO.output(motor1.PUL,GPIO.HIGH)
                GPIO.output(motor2.PUL,GPIO.HIGH)
                GPIO.output(motor3.PUL,GPIO.HIGH)
                sleep(pul_delay)

                GPIO.output(motor1.PUL,GPIO.LOW)
                GPIO.output(motor2.PUL,GPIO.LOW)
                GPIO.output(motor3.PUL,GPIO.LOW)
                sleep(pul_delay)        
            print("Motor Stopped...")  

            
        elif user_input == 'off':   # ends session with Raspberry Pi
            GPIO.cleanup()
            break
    



main()







