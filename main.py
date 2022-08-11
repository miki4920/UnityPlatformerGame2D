import pygame
from pygame import display, Surface
from pygame.locals import *
from pygame.sprite import Sprite

from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock


def key_handler(key):
    movement_vector = [0, 0]
    if key == KeyBinds.LEFT:
        movement_vector[0] -= 1
    if key == KeyBinds.RIGHT:
        movement_vector[0] += 1
    if key == KeyBinds.UP:
        movement_vector[1] -= 1
    if key == KeyBinds.DOWN:
        movement_vector[1] += 1
    return movement_vector


class GameObject:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return self.name

    def update(self, x, y):
        self.x += x
        self.y += y


class Environment:
    def __init__(self):
        self.objects = {}

    def add_object(self, game_object):
        self.objects[str(game_object)] = game_object

    def update_object(self, name, coordinates):
        self.objects[name].update(*coordinates)

    def render_environment(self):
        game_display.fill((0, 0, 0))
        x_unit = Config.SCREEN_WIDTH / Config.WIDTH
        y_unit = Config.SCREEN_HEIGHT / Config.HEIGHT
        for game_object in self.objects.values():
            surface = Surface((game_object.width * x_unit, game_object.height * y_unit))
            surface.fill((128, 255, 40))
            rectangle = surface.get_rect()
            rectangle.topleft = (game_object.x*x_unit, game_object.y*y_unit)
            game_display.blit(surface, rectangle)
        display.update()


environment = Environment()
environment.add_object(GameObject("player", 0, 9, 1, 1))


while True:
    environment.render_environment()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            movement_vector = key_handler(event.key)
            environment.update_object("player", movement_vector)
