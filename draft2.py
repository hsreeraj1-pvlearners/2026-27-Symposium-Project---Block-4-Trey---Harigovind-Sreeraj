from math import cos, pi, radians, sin

from pybricks.ev3devices import GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

# --- Constants ---
  # Raw constants
DRIVE_SPEED = 65  # Degrees per second
OBSTACLE_DISTANCE = 150  # Millimeters
TURN_SPEED = 13  # Degrees per second
WHEEL_DIAMETER = 56  # Millimeters
  # Calculated constants
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER
# Hardware
ev3 = EV3Brick()
gyro_sensor = GyroSensor(Port.S2)
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
# Robot positioning
robot_angle = 0
robot_x = 0.00
robot_y = 0.00
# Mapping data
wall_points = []
wall_x = []
wall_y = []

# --- Function definitions ---
