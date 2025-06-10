#!/usr/bin/env pybricks-micropython
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Import required libraries for EV3 brick, sensors, and motors
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import solver

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize and calibrate the cube flipping arm motor (Port A)
# This motor controls the arm that flips the cube
arm = Motor(Port.A)
wait(1000)
ev3.speaker.beep()
# Calibrate arm position by running until it stalls at the base position
arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
arm.reset_angle(0)

# Initialize the turn table motor (Port C)
# This motor rotates the cube platform
motor = Motor(Port.C)
wait(500)
ev3.speaker.beep()

# Initialize the color sensor (Port S4)
# This sensor reads the colors of the cube faces
color_sensor = ColorSensor(Port.S4)
wait(500)
ev3.speaker.beep()

# Initialize the color sensor arm motor (Port B)
# This motor moves the color sensor in and out
color_sensor_arm = Motor(Port.B)
wait(500)
ev3.speaker.beep()
# Calibrate color sensor arm position
color_sensor_arm.run_until_stalled(70, Stop.HOLD)
color_sensor_arm.reset_angle(0)
color_sensor_arm.run_target(20, -5, then=Stop.HOLD, wait=True)

# Function to flip the cube using the arm motor
# Sequence: Open arm -> Grip cube -> Push cube back
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

# Global variable to track the current rotation position of the turn table
pos = 0

# Function to rotate the cube platform 90 degrees left
def rotate_left():
    global pos 
    pos += 270
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)

# Function to rotate the cube platform 90 degrees right
def rotate_right():
    global pos 
    pos -= 270
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)
    
# Function to turn the cube platform left with overshoot correction
def turn_left():
    global pos
    pos += 330
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)
    pos -= 60
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)

# Function to turn the cube platform right with overshoot correction
def turn_right():
    global pos
    pos -= 330
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)
    pos += 60
    motor.run_target(1000, pos, then=Stop.BRAKE, wait=True)

# Function to extend the color sensor arm to reading position
def extend_color_sensor():
    COLOR_SENSOR_DEGREES_PER_SEC = 300
    color_sensor_arm.run_target(COLOR_SENSOR_DEGREES_PER_SEC, -70, then=Stop.HOLD, wait=True)

# Function to retract the color sensor arm to resting position
def retract_color_sensor():
    COLOR_SENSOR_DEGREES_PER_SEC = 300
    color_sensor_arm.run_target(COLOR_SENSOR_DEGREES_PER_SEC, -5, then=Stop.HOLD, wait=True)

# Color calibration data: (Color name, (R, G, B, Intensity))
# These values are used to identify cube face colors
COLORS = (
    ("WHITE", (70, 69, 63, 75)),
    ("BLUE", (9, 28, 36, 10)),
    ("GREEN", (13, 42, 48, 14)),
    ("RED", (37, 9, 2, 40)),
    ("ORANGE", (53, 73, 93, 56)),
    ("BLACK", (9, 10, 3, 10)),
)

# Function to convert RGB values to the closest matching color name
# Uses Euclidean distance to find the closest color from the calibration data
def convert_rgb_to_color(r, g, b, intensity):
    closest_color = "NONE"
    closest_color_dist = 999999999
    for (color_name, (color_r, color_g, color_b, color_intensity)) in COLORS:
        dist = abs(r - color_r)**2 + abs(g - color_g)**2 + abs(b - color_b)**2 + abs(intensity - color_intensity)**2
        if dist < closest_color_dist:
            closest_color = color_name
            closest_color_dist = dist
    return closest_color

# Array to store the colors of all 24 cube facelets
arr = [1]*24

# Function to read the current color from the color sensor
# Returns both the color name and raw RGB values
def read_current_color():
    r, g, b = color_sensor.rgb()
    intensity = color_sensor.reflection()
    return convert_rgb_to_color(r, g, b, intensity), (r, g, b, intensity)

# Function to scan one face of the cube
# Rotates the cube 4 times and reads the color of each facelet
def scan_face():
    temp_array = []
    for i in range(4):
        color, (r,g,b, intensity) = read_current_color()
        print(color, (r,g,b, intensity))
        temp_array.append(color)
        wait(100)
        rotate_left()
    return temp_array
        
# Function to scan all faces of the cube
# Uses a key array to map scanned colors to the correct positions in the state array
def scan_cube():
    # Key array maps scanned positions to state array positions
    key = [2,1,0,3,5,4,7,6,10,9,8,11,14,13,12,15,18,17,16,19,21,20,23,22]
    key_counter = 0
    global arr
   
    # Scan white face
    extend_color_sensor()
    face = scan_face() # white
    for item in face:
        arr[key[key_counter]] = item
        key_counter += 1
    retract_color_sensor()
    
    for i in range(3):
        flip()
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
    
    rotate_left()
    flip()
    flip()
    arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  

# Main program execution
scan_cube()
print(arr)

# Convert scanned colors to cube state and get solution
state = solver.convert_color_arr_to_16_state(arr)
if state is None:
    print("Scan error!")
    exit(0)
print("got state: ", state)

# Get and execute solution moves
sol = solver.get_solution_for_state(state)
print("solution: ", sol)

# Execute each move in the solution
for move in sol:
    if move == "z'":
        flip()
    elif move[0] == "y":
        if len(move) == 1:
            arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
            rotate_left()
        else:
            arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
            rotate_right()
    elif move[0] == "D":
        if len(move) == 1:
            arm.run_target(200, 125, then=Stop.BRAKE, wait=True)
            turn_right()
        elif move[1] == "'":
            arm.run_target(200, 125, then=Stop.BRAKE, wait=True)  
            turn_left()
        elif move[1] == "2":
            arm.run_target(200, 125, then=Stop.BRAKE, wait=True)  
            turn_left()
            turn_left()

# Reset arm position and play completion sound
arm.run_until_stalled(-200, then=Stop.BRAKE, duty_limit=None)  
motor.run_target(1000, 1080 * 4, wait=False)
ev3.speaker.play_file("champions.wav")