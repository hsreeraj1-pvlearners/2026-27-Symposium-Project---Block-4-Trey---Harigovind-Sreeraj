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

# Dimensions
ROBOT_WIDTH = 180
WHEEL_DIAMETER = 56

# Reset
robot_x = ROOM_WIDTH / 2
robot_y = ROOM_HEIGHT / 2
robot_angle = 0

left_motor_speed = 0
right_motor_speed = 0

robot_moving = False
