
import PiMotor
import time

def run():
    '''
    Procedure to test all the motor pins

    Outputs to the terminal which motor is being powered and which config is being executed.
    Calls the "Forward" method in order to demonstrate which config you should be using to 
    define the correct "forward" for your project.
    '''
    '''
    us = PiMotor.Sensor("ULTRASONIC",10)
    us.trigger()
    while not us.Triggered:
        us.sonicCheck()
        print("Not Triggered")
        time.sleep(1)
    print("Triggered")
    '''
    d = ["MOTOR1","MOTOR2","MOTOR3","MOTOR4"]
    for motor in d:
        for config in range(1,3):
            print(motor + " config: " + str(config))
            m = PiMotor.Motor(motor,2)
            m.forward(50)
            time.sleep(2)
            m.stop()

run()
