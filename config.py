from pygame.locals import *


class KeyBinds:
    UP = K_UP
    DOWN = K_DOWN
    RIGHT = K_RIGHT
    LEFT = K_LEFT


class Config:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    FPS = 5

    ACCELERATION = 2.5
    JUMPING_POWER = -10
    FRICTION = -0.99
    GRAVITY = 0.5
