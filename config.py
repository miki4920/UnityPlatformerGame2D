from pygame.locals import *


class KeyBinds:
    UP = K_UP
    DOWN = K_DOWN
    RIGHT = K_RIGHT
    LEFT = K_LEFT


class Config:
    WIDTH = 10
    HEIGHT = 10
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    FPS = 5

    ACCELERATION = -0.1
    JUMPING_POWER = -0.25
    FRICTION = -0.99
    GRAVITY = 0.01
