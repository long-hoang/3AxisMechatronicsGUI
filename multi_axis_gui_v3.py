# Functional
# program enables user to run motors simultaneously for testing
# set the number of steps (arbritrary at the moment)
# can disable and enable the motors
# can switch directions

import tkinter as tk
from time import sleep # note: sleep input units = seconds
import RPi.GPIO as GPIO

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



class Motor:
    def __init__(self, p, d, e):
        self.PUL = p
        self.DIR = d
        self.ENA = e
        
        self.step_cycle_input = 1000 
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
        for x in range(self.step_cycle_input):    
            self.step()
        print("Motor Stopped...")   

    def jog(self):
        self.run()
        self.flipDir()
        self.run()
        self.flipDir()


class MyApp:

    def __init__(self,root):
        root.title("Multi Axis Controller")
        root.geometry("500x500")
        root.maxsize(1000,1000)
        
        self.all_step_cycle_input = 0 # Subject to change...

        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)

        # MOTOR 1
        self.motor1 = Motor(PUL1,DIR1,ENA1)
        self.motor1.setup()

        # MOTOR 2
        self.motor2 = Motor(PUL2,DIR2,ENA2)
        self.motor2.setup()

        # MOTOR 3
        self.motor3 = Motor(PUL3,DIR3,ENA3)
        self.motor3.setup()




        self.user_entry = tk.IntVar()
        entry = tk.Entry(root, textvariable=self.user_entry)
        entry.pack()

        button0 = tk.Button(root, text = "Set Steps", command = self.set_steps)
        button0.pack()


        button1 = tk.Button(root, text = "Run all!", command = self.run_all)
        button1.pack()
        
        button2 = tk.Button(root, text = "Flip Directions", command = self.flip)
        button2.pack()
        
        button3 = tk.Button(root, text = "Disable all", command = self.disable_all)
        button3.pack()
        
        button4 = tk.Button(root, text = "Enable all", command = self.enable_all)
        button4.pack()        

        

        
    def set_steps(self):
        self.all_step_cycle_input = self.user_entry.get()
        print(self.all_step_cycle_input)
        
    def flip(self):
        self.motor1.flipDir()
        self.motor2.flipDir()
        self.motor3.flipDir()
    
    def disable_all(self):
        self.motor1.enaMotor("disable")
        self.motor2.enaMotor("disable")
        self.motor3.enaMotor("disable")
        
    def enable_all(self):
        self.motor1.enaMotor("enable")
        self.motor2.enaMotor("enable")
        self.motor3.enaMotor("enable")        
        
    def run_all(self): # important note -> this does not access the motor's
        # own method to run, so it d
        for x in range(self.all_step_cycle_input):  
            GPIO.output(self.motor1.PUL,GPIO.HIGH)
            GPIO.output(self.motor2.PUL,GPIO.HIGH)
            GPIO.output(self.motor3.PUL,GPIO.HIGH)
            sleep(pul_delay)

            GPIO.output(self.motor1.PUL,GPIO.LOW)
            GPIO.output(self.motor2.PUL,GPIO.LOW)
            GPIO.output(self.motor3.PUL,GPIO.LOW)
            sleep(pul_delay)        
        print("Motor Stopped...") 
    

root = tk.Tk()
MyApp(root)
root.mainloop()