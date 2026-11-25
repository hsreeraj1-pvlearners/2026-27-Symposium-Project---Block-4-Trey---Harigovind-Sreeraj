import random
from math import cos, pi, radians, sin

from pybricks.ev3devices import GyroSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

# --- Constants ---
  # Raw constants
DETECTION_DISTANCE = 1500  # Millimeters
DISTANCE_TOLERANCE = 30  # Millimeters
DRIVE_SPEED = 65  # Degrees per second
MAX_CORRECTION = 5
SIGNATURE_COUNT = 9
TARGET_WALL_DISTANCE = 120  # Millimeters
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
# Current 

# --- Function definitions ---
def approach_surface():
  previous_heading = -gyro_sensor.angle()
  previous_left = left_motor.angle()
  previous_right = right_motor.angle()
  left_motor.run(DRIVE_SPEED)
  right_motor.run(DRIVE_SPEED)
  while ultrasonic_sensor.distance() > TARGET_WALL_DISTANCE:
    previous_heading, previous_left, previous_right = (
      update_position(
        previous_heading,
        previous_left,
        previous_right
      )
    )
    wait(10)
  left_motor.brake()
  right_motor.brake()

def correct_distance():
  for i in range(MAX_CORRECTION):
    distance = check_distance()
    if distance > DETECTION_DISTANCE:
      return False
    difference = distance - TARGET_WALL_DISTANCE
    if abs(difference) <= DISTANCE_TOLERANCE:
      return True
    correction = min(
      abs(difference),
      MAX_CORRECTION_STEP
    )
    if difference > 0:
      drive_distance(correction)
    else:
      drive_distance(-correction)
  return abs(check_distance() - TARGET_WALL_DISTANCE) <= (
    DISTANCE_TOLERANCE
  )

def drive_distance(distance):
  previous_heading = -gyro_sensor.angle()
  previous_left = left_motor.angle()
  previous_right = right_motor.angle()
  start_left = previous_left
  start_right = previous_right
  target_distance = abs(distance)
  if distance >= 0:
    direction = 1
  else:
    direction = -1
  left_motor.run(direction * DRIVE_SPEED)
  right_motor.run(direction * DRIVE_SPEED)
  while True:
    previous_heading, previous_left, previous_right = (
      update_position(
        previous_heading,
        previous_left,
        previous_right
      )
    )
    left_travel = (
      (left_motor.angle() - start_left)
      / 360
    ) * WHEEL_CIRCUMFERENCE
    right_travel = (
      (right_motor.angle() - start_right)
      / 360
    ) * WHEEL_CIRCUMFERENCE
    average_travel = (
      direction * (left_travel + right_travel) / 2
    )
    if average_travel >= target_distance :
      break
    wait(10)
  left_motor.brake()
  right_motor.brake()

def drive_until_obstacle():
  previous_heading = -gyro_sensor.angle()
  previous_left = left_motor.angle()
  previous_right = right_motor.angle()
  left_motor.run(DRIVE_SPEED)
  right_motor.run(DRIVE_SPEED)
  while ultrasonic_sensor.distance() > DETECTION_DISTANCE:
    previous_heading, previous_left, previous_right = (
      update_position(
        previous_heading,
        previous_left,
        previous_right
      )
    )
    wait(10)
  left_motor.brake()
  right_motor.brake()

def plot_surface():
  distance = ultrasonic_sensor.distance()
  surface_x = (
    robot_x + distance * cos(radians(robot_angle))
  )
  surface_y = (
    robot_y + distance * sin(radians(robot_angle))
  )
  wall_points.append((surface_x, surface_y))
  wall_x.append(surface_x)
  wall_y.append(surface_y)

def turn(angle):
  global robot_angle
  starting_angle = -gyro_sensor.angle()
  target_angle = starting_angle + angle  
  if angle > 0:
    left_motor.run(-TURN_SPEED)
    right_motor.run(TURN_SPEED)
  elif angle < 0:
    left_motor.run(TURN_SPEED)
    right_motor.run(-TURN_SPEED)
  else:
    return
  while True:
    current_angle = -gyro_sensor.angle()
    if angle > 0 and current_angle >= target_angle:
      break
    elif angle < 0 and current_angle <= target_angle:
      break
    wait(10)
  left_motor.brake()
  right_motor.brake()
  robot_angle = -gyro_sensor.angle()

def update_position(previous_heading, previous_left, previous_right):
  global robot_angle, robot_x, robot_y
  current_left = left_motor.angle()
  current_right = right_motor.angle()
  left_rotation = current_left - previous_left
  right_rotation = current_right - previous_right
  left_distance = (WHEEL_CIRCUMFERENCE * (left_rotation / 360))
  right_distance = (WHEEL_CIRCUMFERENCE * (right_rotation / 360))
  distance = (left_distance + right_distance) / 2
  current_heading = -gyro_sensor.angle()
  average_heading = (current_heading + previous_heading) / 2
  robot_x += distance * cos(radians(average_heading))
  robot_y += distance * sin(radians(average_heading))
  robot_angle = current_heading
  return current_heading, current_left, current_right

# --- Main function loop ---
