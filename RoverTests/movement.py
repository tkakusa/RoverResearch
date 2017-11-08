import PiMotor
import time

right = "MOTOR1"
left = "MOTOR2"
speed = 50

def forward():
    mr = PiMotor.Motor(right, 2)
    ml = PiMotor.Motor(left, 2)
    
    mr.forward(speed)
    ml.forward(speed)
    
    time.sleep(2)
    
    mr.stop()
    ml.stop()

forward()
