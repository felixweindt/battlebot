#!/usr/bin/env pybricks-micropython
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

print("reflection:", color_sensor.reflection())
print("distance:", ultrasonic_sensor.distance())
# drive_motor.run_target(100, 360)

#steering_motor.reset_angle(0)



print(steering_motor.angle())

steering_motor.run_target(100, 0)
print(steering_motor.angle())

steering_motor.run_target(100, 30)
print(steering_motor.angle())

steering_motor.run_target(100, -30)
print(steering_motor.angle())

steering_motor.run_target(100, 0)

# Constants for motor speeds
DRIVE_SPEED = 360    # Degrees per second
STEERING_SPEED = 100 # Degrees per second
WEAPON_SPEED = 1050  # Degrees per second

# Initialize motors to starting position
steering_motor.run_target(STEERING_SPEED, 0)

print("EV3 Button Control activated:")
print("UP/DOWN - Drive forward/backward")
print("LEFT/RIGHT - Steer left/right")
print("CENTER - Toggle weapon")
print("DOWN + CENTER - Quit")

weapon_active = False

while True:
    pressed = ev3.buttons.pressed()
    
    # Driving controls
    if Button.UP in pressed:
        drive_motor.run(DRIVE_SPEED)
    elif Button.DOWN in pressed:
        drive_motor.run(-DRIVE_SPEED)
    else:
        drive_motor.stop()
        
    # Steering controls
    if Button.LEFT in pressed:
        steering_motor.run_target(STEERING_SPEED, -30)
    elif Button.RIGHT in pressed:
        steering_motor.run_target(STEERING_SPEED, 30)
    else:
        steering_motor.run_target(STEERING_SPEED, 0)
        
    # Weapon control
    if Button.CENTER in pressed:
        weapon_active = not weapon_active
        if weapon_active:
            weapon_motor.run(WEAPON_SPEED)
        else:
            weapon_motor.stop()
        wait(300)  # Debounce delay
    
    # Quit program (DOWN + CENTER buttons)
    if Button.DOWN in pressed and Button.CENTER in pressed:
        drive_motor.stop()
        steering_motor.run_target(STEERING_SPEED, 0)
        weapon_motor.stop()
        break
    
    wait(10)  # Small delay to prevent CPU overload