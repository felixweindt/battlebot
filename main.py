#!/usr/bin/env pybricks-micropython
# from pynput import keyboard

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



ev3 = EV3Brick()
drive_motor = Motor(Port.B)      
steering_motor = Motor(Port.A)    
weapon_motor = Motor(Port.D)      

color_sensor = ColorSensor(Port.S4)    
ultrasonic_sensor = UltrasonicSensor(Port.S3) 

# Geschwindigkeiten und Lenkeinschlag (ANPASSEN!!)
DRIVE_SPEED = 500            
STEERING_ANGLE = 40        
WEAPON_SPEED = 5000

def stop_all_motors():
    drive_motor.stop()
    steering_motor.run_target(DRIVE_SPEED, 0)
    weapon_motor.stop()

print("Controls:")
print("w - forward")
print("s - backward")
print("a - steer left")
print("d - steer right")
print("space - weapon")
print("q - quit")

while True:
    cmd = input("Enter command: ")
    
    if cmd == 'w':
        drive_motor.run(-DRIVE_SPEED)
    elif cmd == 's':
        drive_motor.run(DRIVE_SPEED)
    elif cmd == 'a':
        steering_motor.run_target(DRIVE_SPEED, STEERING_ANGLE, wait=False)
    elif cmd == 'd':
        steering_motor.run_target(DRIVE_SPEED, -STEERING_ANGLE, wait=False)
    elif cmd == 'e':
        steering_motor.run_target(DRIVE_SPEED, 0)
    elif cmd == ' ':
        weapon_motor.run(WEAPON_SPEED)
    elif cmd == 'q':
        stop_all_motors()
    else:
        stop_all_motors()
        weapon_motor.stop()


# Keep the program running
while True:
    wait(10)
    if not listener.running:
        break



