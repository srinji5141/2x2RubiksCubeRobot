#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()

# Initialize cube flipping arm
arm = Motor(Port.A)
wait(1000)
ev3.speaker.beep()
# Initialize position
arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  

# Initilize turn table motor
motor = Motor(Port.C)
wait(500)
ev3.speaker.beep()

# Initialize color sensor
color_sensor = ColorSensor(Port.S4)
wait(500)
ev3.speaker.beep()

#Initialize color sensor arm
color_sensor_arm = Motor(Port.B)
wait(500)
ev3.speaker.beep()
# Initialize position
color_sensor_arm.run_until_stalled(70, Stop.HOLD)
color_sensor_arm.reset_angle(0)
color_sensor_arm.run_target(20, -5, then=Stop.HOLD, wait=True)

# Flip function
def flip():
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()

    # Grip cube/flip state
    arm.run_angle(200, 270, then=Stop.BRAKE, wait=True)  
    ev3.speaker.beep()

    # Push cube/return to table state
    arm.run_angle(-200, 180, then=Stop.BRAKE, wait=True)  
    ev3.speaker.beep()

pos = 0

# L rotate function (from Srinjana's POV)
def rotate_left():
    global pos 
    pos += 270
    motor.run_target(500, pos, then=Stop.BRAKE, wait=True)

# R rotate function (from Srinjana's POV)
def rotate_right():
    global pos 
    pos -= 270
    motor.run_target(500, pos, then=Stop.BRAKE, wait=True)

def extend_color_sensor():
    COLOR_SENSOR_DEGREES_PER_SEC = 300
    color_sensor_arm.run_target(COLOR_SENSOR_DEGREES_PER_SEC, -75, then=Stop.HOLD, wait=True)

def retract_color_sensor():
    COLOR_SENSOR_DEGREES_PER_SEC = 300
    color_sensor_arm.run_target(COLOR_SENSOR_DEGREES_PER_SEC, -5, then=Stop.HOLD, wait=True)

COLORS = (
    ("WHITE", (70, 69, 63, 75)),
    ("BLUE", (9, 28, 36, 10)),
    ("GREEN", (13, 42, 48, 14)),
    ("RED", (37, 9, 2, 40)),
    ("ORANGE", (53, 73, 93, 56)),
    ("BLACK", (9, 10, 3, 10)),
)

def convert_rgb_to_color(r, g, b, intensity):
    closest_color = "NONE"
    closest_color_dist = 999999999
    for (color_name, (color_r, color_g, color_b, color_intensity)) in COLORS:
        dist = abs(r - color_r)**2 + abs(g - color_g)**2 + abs(b - color_b)**2 + abs(intensity - color_intensity)**2
        if dist < closest_color_dist:
            closest_color = color_name
            closest_color_dist = dist
    return closest_color

arr = [1]*24

def read_current_color():
    r, g, b = color_sensor.rgb()
    intensity = color_sensor.reflection()
    return convert_rgb_to_color(r, g, b, intensity), (r, g, b, intensity)

# Write your program here.
def scan_face():
    temp_array = []
    for i in range(4):
        color, (r,g,b, intensity) = read_current_color()
        print(color, (r,g,b, intensity))
        temp_array.append(color)
        wait(500)
        rotate_left()
    return temp_array
        
def scan_cube():
    key = [2,1,0,3,5,4,7,6,10,9,8,11,14,13,12,15,18,17,16,19,21,20,23,22]
    key_counter = 0
    global arr
   
    extend_color_sensor()
    face = scan_face() # white
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    for i in range(3):
        flip()
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()
    extend_color_sensor()
    face = scan_face() # orange
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    rotate_right()
    flip()
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()
    extend_color_sensor()
    face = scan_face() # green
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    flip()
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()
    extend_color_sensor()
    face = scan_face() # red
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    flip()
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()
    extend_color_sensor()
    face = scan_face() # blue
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    rotate_right()
    flip()
    # Open arm/reset state
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
    wait(500)
    ev3.speaker.beep()
    extend_color_sensor()
    face = scan_face() # yellow
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()

scan_cube()
print(arr)



# Harshith's code of rotating left 4 times from my POV

# Overshoot by 60 degrees and then return to ensure complete rotation
# positions = [0, 330, 270, 600, 540, 870, 810, 1140, 1080]
    # positions = [270, 540, 810, 1080]
    # for pos in positions:
    #     motor.run_target(500, pos, then=Stop.BRAKE, wait=True)
    #     wait(500)
    #     detected_color = color_sensor.color()
    #     r, g, b = color_sensor.rgb()
    #     print("Color:", detected_color)
    #     print("RGB:", r, g, b)
    #     wait(500)
# color_sensor_arm.run_target(100, -100, Stop.BRAKE)
# color_sensor_arm.run_target(200, 0, Stop.BRAKE)

##############################################
"""
    White:
    Color: Color.WHITE
    RGB: 84 84 81
    Color: Color.WHITE
    RGB: 82 81 78
    Color: Color.WHITE
    RGB: 80 78 74
    Color: Color.WHITE
    RGB: 80 77 74

    Yellow:
    Color: Color.WHITE
    RGB: 52 50 63
    Color: Color.WHITE
    RGB: 52 49 62
    Color: Color.WHITE
    RGB: 51 48 61
    Color: Color.WHITE
    RGB: 50 47 58
    
    Orange:
    Color: Color.WHITE
    RGB: 60 89 100
    Color: Color.WHITE
    RGB: 60 90 100
    Color: Color.WHITE
    RGB: 58 90 100
    Color: Color.WHITE
    RGB: 60 88 100
    
    Blue:
    RGB: 11 30 41
    Color: Color.BLUE
    RGB: 11 30 39
    Color: Color.BLUE
    RGB: 11 29 37
    Color: Color.BLUE
    RGB: 12 29 38
    
    Red:
    Color: Color.RED
    RGB: 43 12 2
    Color: Color.RED
    RGB: 43 12 1
    Color: Color.RED
    RGB: 43 12 5
    Color: Color.RED
    RGB: 43 12 3
    
    Green:
    Color: Color.BLUE
    RGB: 15 49 58
    Color: Color.BLUE
    RGB: 15 48 57
    Color: Color.BLUE
    RGB: 15 47 55
    Color: Color.BLUE
    RGB: 15 47 55
    
"""
