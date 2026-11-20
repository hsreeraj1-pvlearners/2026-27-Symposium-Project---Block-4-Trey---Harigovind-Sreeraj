# ======================================================================
# Initializing
# ======================================================================


# Imports
import random
from math import cos, pi, radians, sin

from pybricks.ev3devices import Motor, UltrasonicSensor,GyroSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

# --- Constants ---
  # Raw Constants
WHEEL_DIAMETER = 56  # Millimeters
  # Calculated Constants
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER

# Robot Positioning
robot_x = 0.00
robot_y = 0.00
robot_angle = 0

# Mapping Data (lists)
wall_points = []
wall_x
wall_y

# Function Definitions
