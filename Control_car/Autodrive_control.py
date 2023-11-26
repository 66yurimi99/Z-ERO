import sys
import signal
import RPi.GPIO as GPIO
import time

### setting GPIO ###
class AutoDrive:
    ## Car, Driver sleep, object detection, Lane direction
    def __init__(self, isCar, Driver_state,obj,theta):
        self.isCar = isCar
        self.obj_state = obj
        self.theta = theta
        self.default_vel = 100
        self.state = None
        ## GPIO set
        self.GPIO_Right = 12
        self.GPIO_Left = 13

    def Set_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        # GPIO_Right = 12
        # GPIO_Left = 13
        GPIO.setup(self.GPIO_Right, GPIO.OUT)  # PwM_R
        GPIO.setup(self.GPIO_Left, GPIO.OUT)  # PwM_L

        self.left_wheel = GPIO.PWM(self.GPIO_Left, 50)
        self.right_wheel = GPIO.PWM(self.GPIO_Right, 50)
        self.left_wheel.start(10)
        self.right_wheel.start(10)
        
    def get_Object_state(self,obj):
        # Far
        if obj == 3:
            self.obj_state = 1
        # little bit closer
        elif obj == 2:
            self.obj_state = 0.5
        # very close
        elif obj == 1:
            self.obj_state = 0
        return self.obj_state

    def get_Direction(self):
        if self.theta >= 30:
            self.state = "left"
        elif -30 < self.theta < 30:
            self.state = "straight"
            if self.theta == 0.0:
                self.theta = 1.0
        else:
            self.state = "right"
        return self.state, self.theta

    def Cal_velocity(self):
        print(f"Current state: {self.state}")
        print(f"theta in auto class: {self.theta}")
        # cv2.putText(.....)
        self.vel = self.default_vel* abs(self.theta)/90 * self.obj_state
        print(f"max Speed: {self.vel}")
        if self.vel>=100:
            self.vel = 99
        elif self.vel<60:
            self.vel = 60
        if self.state == "straight":
            self.left_wheel.ChangeDutyCycle(0.8*self.vel)
            self.right_wheel.ChangeDutyCycle(self.vel)
        elif self.state == "right":
            self.left_wheel.ChangeDutyCycle(self.vel)
            self.right_wheel.ChangeDutyCycle(self.vel) #0.7 * self.vel
        elif self.state == "left":
            self.left_wheel.ChangeDutyCycle(0.5 * self.vel)
            self.right_wheel.ChangeDutyCycle(self.vel)
        time.sleep(1)

    def handle_sigint(self,signum, fr):
        self.stop_motor()
        sys.exit(0)

    # signal.signal(signal.SIGINT, handle_sigint)

    def stop_motor(self):
        self.left_wheel.stop()
        self.right_wheel.stop()
