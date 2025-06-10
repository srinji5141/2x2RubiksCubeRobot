# 2x2 Rubik's Cube Robot

A LEGO EV3 robot that can automatically solve a 2x2 Rubik's Cube. This project was developed as part of CS188 at UCLA.

## Overview

This robot uses a LEGO EV3 brick to control a mechanical system that can:
- Scan all faces of a 2x2 Rubik's Cube using a color sensor
- Manipulate the cube through precise rotations and flips
- Solve the cube using an efficient algorithm
- Execute the solution through mechanical movements

## Hardware Requirements

- LEGO EV3 Brick
- EV3 Motors (3x)
- EV3 Color Sensor
- Custom-built mechanical assembly for cube manipulation
- 2x2 Rubik's Cube

## Software Requirements

- LEGO EV3 MicroPython v2.0 or higher
- Python 3.x (for development)

## Project Structure

- `main.py` - Main robot control program
- `cube.py` - Cube state representation and manipulation
- `solver.py` - Cube solving algorithm implementation
- `massive_table.bin` - Lookup table for optimal solutions

## How It Works

1. **Cube Scanning**: The robot uses a color sensor mounted on a movable arm to scan each face of the cube. The sensor reads RGB values and converts them to cube colors.

2. **State Representation**: The cube's state is represented in memory using a 14-element array.

3. **Solving Algorithm**: The robot uses a combination of:
   - Pattern recognition
   - Lookup tables for optimal solutions
   - Efficient move sequences

4. **Mechanical Execution**: The solution is executed through:
   - A turntable for cube rotation
   - A flipping mechanism for cube manipulation
   - Precise motor control for accurate movements

## Usage

1. Place the cube on the robot's turntable
2. Run the main program on the EV3 brick
3. The robot will:
   - Scan the cube
   - Calculate the solution
   - Execute the moves automatically
4. The solved cube can be removed from the turntable

## Features

- Automatic cube scanning
- Real-time color detection
- Optimal solution finding
- Precise mechanical control

## Development

The project is written in MicroPython for the EV3 brick. Key components:

- `main.py` handles robot control and sensor interaction
- `cube.py` manages cube state and move validation
- `solver.py` implements the solving algorithm

## License

This project is for educational purposes only.

## Notes

- The robot requires calibration for optimal color detection
- Solution times may vary based on cube state