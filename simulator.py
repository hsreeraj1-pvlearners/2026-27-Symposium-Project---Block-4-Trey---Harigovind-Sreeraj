import pygame
import sys

pygame.init()

# --- Initialization ---

# Constants
WINDOW_CAPTION = "EV3 Robot Simulator"
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

BLACK = (0, 0, 0)
BLUE = (50, 120, 220)
DARK_GRAY = (70, 70, 70)
GRAY = (180, 180, 180)
GREEN = (50, 180, 90)
RED = (220, 50, 50)
WHITE = (255, 255, 255)

FPS = 60

# Creating the window
screen = pygame.display.set_mode(
  (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption(WINDOW_CAPTION)

clock = pygame.time.Clock()

# --- Room initialization ---

# Dimensioning and display
ROOM_WIDTH = 6000
ROOM_HEIGHT = 4000

PIXELS_PER_MM = 0.15

ROOM_PIXEL_WIDTH = ROOM_WIDTH * PIXELS_PER_MM
ROOM_PIXEL_HEIGHT = ROOM_HEIGHT * PIXELS_PER_MM

ROOM_X = (WINDOW_WIDTH - ROOM_PIXEL_WIDTH) / 2
ROOM_Y = (WINDOW_HEIGHT - ROOM_PIXEL_HEIGHT) / 2

# --- Robot initialization ---

# Dimensions in millimeters
ROBOT_LENGTH = 120
ROBOT_WIDTH = 180
WHEEL_DIAMETER = 56
WHEEL_TRACK = 154

# Reset
robot_x = ROOM_WIDTH / 2
robot_y = ROOM_HEIGHT / 2
robot_angle = 0

left_motor_speed = 0
right_motor_speed = 0

robot_moving = False

# --- Coordinate conversion ---

def world_to_screen(x, y):
  screen_x = ROOM_X + (x * PIXELS_PER_MM)
  screen_y = ROOM_Y + ROOM_PIXEL_HEIGHT - (y * PIXELS_PER_MM)
  
  return screen_x, screen_y

def screen_to_world(x, y):
  world_x = (x - ROOM_X) / PIXELS_PER_MM
  world_y = (ROOM_Y + ROOM_PIXEL_HEIGHT - y) / PIXELS_PER_MM

  return world_x, world_y

# --- Room rendering ---

def draw_room():
  pygame.draw.rect(
    screen,
    WHITE,
    (ROOM_X, ROOM_Y, ROOM_PIXEL_WIDTH, ROOM_PIXEL_HEIGHT)
  )
  
  pygame.draw.rect(
    screen,
    BLACK,
    (ROOM_X, ROOM_Y, ROOM_PIXEL_WIDTH, ROOM_PIXEL_HEIGHT),
    3
  )

# --- Robot rendering ---

def draw_robot():
  robot_screen_x, robot_screen_y = world_to_screen(
    robot_x,
    robot_y,
  )
  
  robot_surface = pygame.Surface(
    (
      round(ROBOT_LENGTH * PIXELS_PER_MM),
      round(ROBOT_WIDTH * PIXELS_PER_MM)
    ),
    pygame.SRCALPHA
  )
  
  robot_surface.fill(BLUE)
  
  rotated_robot=pygame.transform.rotate(
    robot_surface,
    robot_angle
  )
  
  robot_rect = rotated_robot.get_rect(
    center=(robot_screen_x, robot_screen_y)
  )
  
  screen.blit(rotated_robot, robot_rect)
