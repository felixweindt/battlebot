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
steering_motor = Motor(Port.C)    
weapon_motor = Motor(Port.A)      

color_sensor = ColorSensor(Port.S1)    
ultrasonic_sensor = UltrasonicSensor(Port.S4)  

# Geschwindigkeiten und Lenkeinschlag (ANPASSEN!!)
DRIVE_SPEED = 360          
DRIVE_SEARCH_SPEED = 200   
STEERING_ANGLE = 40        
WEAPON_SPEED = 1050         

# Lenkwinkel (ANPASSEN!!)
SEARCH_STEERING_ANGLE = 35   
ATTACK_STEERING_ANGLE = 25   
ESCAPE_STEERING_ANGLE = 40   


ATTACK_DISTANCE = 500
BOUNDARY_REFLECTION = 30   # Ändern mit Wert des Tapes

# Zustände
STATE_SEARCH = "search"
STATE_ATTACK = "attack"
STATE_AVOID = "avoid"
current_state = STATE_SEARCH

def search_for_opponent():
    # Einleitung Suchkreiseln
    steering_motor.run_target(DRIVE_SPEED, SEARCH_STEERING_ANGLE)
    drive_motor.run(DRIVE_SEARCH_SPEED)
    
    distance = ultrasonic_sensor.distance()
    
    if distance < ATTACK_DISTANCE:
        # Räder gerade stellen für Angriff
        steering_motor.run_target(DRIVE_SPEED, 0)
        drive_motor.hold()
        return True
    
    return False

def attack_opponent():
    # Waffe aktivieren und angreifen
    weapon_motor.run(WEAPON_SPEED)
    distance = ultrasonic_sensor.distance()
    
    if distance > ATTACK_DISTANCE:
        # Motoren stoppen und wieder in die main schleife
        weapon_motor.stop()
        drive_motor.stop()
        steering_motor.run_target(DRIVE_SPEED, 0)
        return False
    
    if color_sensor.reflection() < BOUNDARY_REFLECTION:
        weapon_motor.stop()
        drive_motor.stop()
        return False
    
    # Direkter Angriff
    steering_motor.run_target(DRIVE_SPEED, 0)
    drive_motor.run(DRIVE_SPEED)
    return True

def avoid_boundary():
    if color_sensor.reflection() < BOUNDARY_REFLECTION:
        drive_motor.stop()
        weapon_motor.stop()
        
        # Rückwärts fahren
        steering_motor.run_target(DRIVE_SPEED, 0) 
        drive_motor.run_angle(-DRIVE_SPEED, 360)
        
        # Wegfahren
        steering_motor.run_target(DRIVE_SPEED, ESCAPE_STEERING_ANGLE)
        drive_motor.run_angle(DRIVE_SPEED, 360)  
        
        return True
    
    return False

# Warten auf Spielstart 
ev3.speaker.beep()
while Button.CENTER not in ev3.buttons.pressed():
    wait(10)

# Hauptschleife
while True:
    if avoid_boundary():
        current_state = STATE_SEARCH
        continue

    if current_state == STATE_SEARCH:
        if search_for_opponent():
            current_state = STATE_ATTACK
            
    elif current_state == STATE_ATTACK:
        if not attack_opponent():
            current_state = STATE_SEARCH
