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

arm = Motor(Port.A)
# arm.run_until_stalled(-200, Stop.BRAKE)
wait(1000)

# try moving arm
# Move arm to hit the stop = open arm
arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  # -90 degrees (up)
wait(500)
ev3.speaker.beep()
# Move arm to grip and run
arm.run_angle(200, 270, then=Stop.BRAKE, wait=True)  # -90 degrees (up)
ev3.speaker.beep()

# Move arm to push back into place
arm.run_angle(-200, 180, then=Stop.BRAKE, wait=True)  # -90 degrees (up)
ev3.speaker.beep()

# Move arm down
# arm.run_angle(200, 90, then=Stop.HOLD, wait=True)   # +90 degrees (down)
# wait(500)

color_sensor_arm = Motor(Port.B)
# color_sensor_arm.run_target(100, -100, Stop.BRAKE)
wait(1000)
color_sensor = ColorSensor(Port.S1)

# Rotate 4 times to scan colors
motor = Motor(Port.C)
ev3.speaker.beep()

# Overshoot by 60 degrees and then return to ensure complete rotation
# positions = [0, 330, 270, 600, 540, 870, 810, 1140, 1080]
positions = [270, 540, 810, 1080]
for pos in positions:
    motor.run_target(500, pos, then=Stop.BRAKE, wait=True)
    wait(500)
    detected_color = color_sensor.color()
    r, g, b = color_sensor.rgb()
    print("Color:", detected_color)
    print("RGB:", r, g, b)
    wait(500)


color_sensor_arm.run_target(200, 0, Stop.BRAKE)

# Write your program here.
ev3.speaker.beep()



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
