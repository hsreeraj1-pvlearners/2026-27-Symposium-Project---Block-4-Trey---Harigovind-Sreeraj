import random
from math import cos, pi, radians, sin

from pybricks.ev3devices import GyroSensor, InfraredSensor, Motor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

# --- Constants ---
  # Raw constants
DETECTION_DISTANCE = 1500  # Millimeters
DISTANCE_TOLERANCE = 30  # Millimeters
DRIVE_SPEED = 65  # Degrees per second
MAX_CORRECTION = 5
MAX_CORRECTION_STEP = 30  # Millimeters
SIGNATURE_COUNT = 9
STEP_LENGTH = 50  # Millimeters
TARGET_WALL_DISTANCE = 120  # Millimeters
TURN_SPEED = 13  # Degrees per second
WHEEL_DIAMETER = 56  # Millimeters
  # Calculated constants
LOOP_MATCH_TOLERANCE = STEP_LENGTH / 2
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER
# Hardware
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
# Reset gyro sensor (to prevent drift)
dummy = InfraredSensor(Port.S2)
wait(1000)
gyro_sensor = GyroSensor(Port.S2)
wait(2000)  # The 2-second pause is to ensure the robot stays still
gyro_sensor.reset_angle(0)
# Robot positioning
robot_angle = 0
robot_x = 0.00
robot_y = 0.00
# Mapping data
wall_points = []
wall_x = []
wall_y = []
# Signature point data
object_start_index = 0
signature_x = []
signature_y = []

# --- Function definitions ---
def approach_surface():
  while True:
    distance = read_surface_distance()
    if distance is None:
      return False
    difference = distance - TARGET_WALL_DISTANCE
    if difference <= DISTANCE_TOLERANCE and difference >= 0:
      return True
    else:
      return False
    correction = min(
      difference,
      MAX_CORRECTION_STEP
    )
    drive_distance(correction)

def check_loop(point_x, point_y):
  points_collected = len(wall_x) - object_start_index
  if len(signature_x) != SIGNATURE_COUNT:
    return False
  if points_collected < SIGNATURE_COUNT * 2:
    return False
  first_index = len(wall_x) - SIGNATURE_COUNT
  for i in range(SIGNATURE_COUNT - 1):
    point_index = first_index + i
    if not check_signature(
      wall_x[point_index],
      wall_y[point_index],
      i
    ):
      return False
  return check_signature(
    point_x,
    point_y,
    SIGNATURE_COUNT - 1
  )

def check_signature(point_x, point_y, signature_index):
  if signature_index < 0 or signature_index >= SIGNATURE_COUNT:
    return False
  difference_x = point_x - signature_x[signature_index]
  difference_y = point_y - signature_y[signature_index]
  distance_squared = (
    difference_x ** 2 + difference_y ** 2
  )
  return distance_squared <= LOOP_MATCH_TOLERANCE ** 2

def correct_distance():
  for i in range(MAX_CORRECTION):
    distance = read_surface_distance()
    if distance is None:
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
  distance = read_surface_distance()
  if distance is None:
    return False
  return abs(
    distance - TARGET_WALL_DISTANCE
  ) <= DISTANCE_TOLERANCE

def create_signature():
  global signature_x, signature_y
  signature_x = wall_x[
    object_start_index:object_start_index + SIGNATURE_COUNT
  ]
  signature_y = wall_y[
    object_start_index:object_start_index + SIGNATURE_COUNT
  ]

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
  distance = read_surface_distance()
  if distance is None:
    return None
  surface_x = (
    robot_x + distance * cos(radians(robot_angle))
  )
  surface_y = (
    robot_y + distance * sin(radians(robot_angle))
  )
  wall_points.append((surface_x, surface_y))
  wall_x.append(surface_x)
  wall_y.append(surface_y)
  return surface_x, surface_y

def read_surface_distance():
  # The sensor reads points too close/far as 255 cm; unreliable
  distance = ultrasonic_sensor.distance()
  if distance >= 2550:
    return None
  return distance

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
