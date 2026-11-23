import random
from math import cos, pi, radians, sin

from pybricks.ev3devices import GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

# --- Constants ---
  # Raw constants
SPEED = 65  # Degrees per second
OBSTACLE_DISTANCE = 150  # Millimeters
TURN_SPEED = 13  # Degrees per second
WHEEL_DIAMETER = 56  # Millimeters
  # Calculated Constants
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER
# Hardware
ev3 = EV3Brick()
right_motor = Motor(Port.A)
left_motor = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S2)
# Robot positioning
robot_x = 0.00
robot_y = 0.00
robot_angle = 0
# Mapping data (lists)
wall_points = []
wall_x = []
wall_y = []

# --- Function Definitions---
def drive_until_obstacle():
  global robot_x, robot_y, robot_angle
  previous_left_angle = left_motor.angle()
  previous_right_angle = right_motor.angle()
  previous_heading = -gyro_sensor.angle()
  left_motor.run(SPEED)
  right_motor.run(SPEED)
  while True:
    current_left_angle = left_motor.angle()
    current_right_angle = right_motor.angle()
    left_rotation = current_left_angle - previous_left_angle
    right_rotation = current_right_angle - previous_right_angle
    left_distance = ((left_rotation / 360) * WHEEL_CIRCUMFERENCE)
    right_distance = ((right_rotation / 360) * WHEEL_CIRCUMFERENCE)
    distance = (left_distance + right_distance) / 2
    current_heading = -gyro_sensor.angle()
    average_heading = (current_heading + previous_heading) / 2
    robot_x += distance * cos(radians(average_heading))
    robot_y += distance * sin(radians(average_heading))
    robot_angle = current_heading
    if ultrasonic_sensor.distance() < OBSTACLE_DISTANCE:
      break
    wait(1)
  left_motor.brake()
  right_motor.brake()

def plot_obstacle():
  distance = ultrasonic_sensor.distance()
  obstacle_x = (robot_x + (distance * cos(radians(robot_angle))))
  obstacle_y = (robot_y + (distance * sin(radians(robot_angle))))
  wall_points.append((obstacle_x, obstacle_y))
  wall_x.append(obstacle_x)
  wall_y.append(obstacle_y)

def turn(angle):
  global robot_angle
  starting_angle = -gyro_sensor.angle()
  target_angle = starting_angle + angle  
  if angle > 0:
    left_motor.run(-TURN_SPEED)
    right_motor.run(TURN_SPEED)
  else:
    left_motor.run(TURN_SPEED)
    right_motor.run(-TURN_SPEED)
  while True:
    current_angle = -gyro_sensor.angle()
    if angle > 0 and current_angle >= target_angle:
      break
    elif angle < 0 and current_angle <= target_angle:
      break
    wait(1)
  left_motor.brake()
  right_motor.brake()
  robot_angle = -gyro_sensor.angle()

gyro_sensor.reset_angle(0)

# --- Main function loop ---
while True:
  drive_until_obstacle()
  plot_obstacle()
  random_angle = random.randint(1,359)
  turn(random_angle)
