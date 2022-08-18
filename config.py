from pygame.locals import *


class KeyBinds:
    UP = K_UP
    DOWN = K_DOWN
    RIGHT = K_RIGHT
    LEFT = K_LEFT


class Config:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    PLAYER_SIZE = (50, 50)
    PLAYER_COLOUR = (255, 128, 128)

    WALL_SIZE = (60, 60)
    WALL_COLOUR = (100, 100, 100)
    FPS = 60

    LEVEL_HEIGHT = SCREEN_HEIGHT - WALL_SIZE[1]

    ACCELERATION = 3
    JUMPING_POWER = -14
    FRICTION = -0.5
    GRAVITY = 0.5
