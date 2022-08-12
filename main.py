import pygame
from pygame import display, Surface
from pygame.locals import *
from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()


class GameObject:
    def __init__(self, name, position, dimensions, units):
        self.name = name
        self.position = position
        self.dimensions = dimensions
        self.surface = None
        self.rectangle = None
        self.draw(units)

    def __eq__(self, other):
        return self.name == other.name

    def draw(self, units, shift=0):
        self.surface = Surface((self.dimensions.x * units.x, self.dimensions.y * units.y))
        self.surface.fill((128, 255, 40))
        self.rectangle = self.surface.get_rect()
        self.rectangle.topleft = ((self.position.x - shift) * units.x, self.position.y * units.y)
        return self.surface, self.rectangle


class Environment:
    def __init__(self):
        self.objects = {}
        self.player = GameObject("player", vec(0, Config.HEIGHT-2), vec(1, 1), self.get_units())
        self.add_object(self.player)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def add_object(self, game_object):
        self.objects[str(game_object)] = game_object

    def get_object(self, name):
        return self.objects.get(name)

    def check_object_collision(self):
        for game_object in self.objects.values():
            if game_object != self.player:
                if game_object.rectangle.colliderect(self.player.rectangle):
                    return game_object.rectangle
        return None

    def update(self, keys):
        self.acceleration = vec(0, Config.GRAVITY)
        if keys[KeyBinds.LEFT]:
            self.acceleration.x = Config.ACCELERATION
        if keys[KeyBinds.RIGHT]:
            self.acceleration.x = -Config.ACCELERATION
        if keys[KeyBinds.UP]:
            if self.player.position.y == 9:
                self.velocity.y = 0
                self.acceleration.y = Config.JUMPING_POWER
        self.acceleration.x += self.velocity.x * Config.FRICTION
        self.velocity += self.acceleration
        self.player.position += self.velocity + 0.5 * self.acceleration

    @staticmethod
    def get_units():
        x = game_display.get_width() / Config.WIDTH
        y = game_display.get_height() / Config.HEIGHT
        return vec(x, y)

    def render_environment(self):
        game_display.fill((0, 0, 0))
        for game_object in self.objects.values():
            game_display.blit(*game_object.draw(self.get_units(), self.player.position.x))
            if self.player.position.x - 1 > game_object.position.x:
                game_object.position.x += Config.WIDTH
        display.update()


environment = Environment()
environment.add_object(GameObject("wall", vec(0, Config.HEIGHT-1), vec(Config.WIDTH, 1), environment.get_units()))

while True:
    environment.render_environment()
    environment.update(pygame.key.get_pressed())
    pygame.event.pump()
    frames_per_second.tick(60)
