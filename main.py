import pygame
from pygame import display, Surface
from pygame.locals import *
from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()


class GameObject:
    def __init__(self, name, positions, dimensions):
        self.name = name
        self.positions = positions
        self.surface = Surface(dimensions)
        self.surface.fill((128, 255, 40))
        self.rectangle = self.surface.get_rect()
        self.rectangle.bottomleft = positions
        self.draw()

    def __eq__(self, other):
        return self.name == other.name

    def draw(self, shift=0):
        self.rectangle.bottomleft = self.positions.x, self.positions.y
        return self.surface, self.rectangle


class Environment:
    def __init__(self):
        self.objects = {}
        self.player = GameObject("player", vec(0, 400), vec(50, 50))
        self.add_object(self.player)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.previous_positions = vec(*self.player.positions)

    def add_object(self, game_object):
        self.objects[str(game_object)] = game_object

    def get_object(self, name):
        return self.objects.get(name)

    def get_object_collision(self):
        for game_object in self.objects.values():
            if game_object != self.player:
                if game_object.rectangle.colliderect(self.player.rectangle):
                    return game_object.rectangle
        return None

    def account_for_collision(self, change):
        collision = self.get_object_collision()
        if collision:
            if self.player.positions.y > collision.top:
                self.velocity.y = 0
                self.player.positions.y = collision.top
            elif self.player.positions.y < collision.bottom:
                self.velocity.y = 0
                self.player.positions.y = collision.bottom
        self.player.positions.y += round(change.y, 0)
        self.player.rectangle.bottomleft = self.player.positions
        collision = self.get_object_collision()
        if collision:
            if self.player.positions.x < collision.left:
                self.velocity.x = 0
                self.player.positions.x = collision.left
            elif self.player.positions.x > collision.right:
                self.velocity.x = 0
                self.player.positions.x = collision.right
        self.player.positions.x += round(change.x, 0)
        self.player.rectangle.bottomleft = self.player.positions


    def update(self, keys):
        self.acceleration = vec(0, Config.GRAVITY)
        if keys[KeyBinds.LEFT]:
            self.acceleration.x = -Config.ACCELERATION
        if keys[KeyBinds.RIGHT]:
            self.acceleration.x = Config.ACCELERATION
        if keys[KeyBinds.UP]:
            if self.velocity.y >= 0:
                self.velocity.y = -10
        self.acceleration.x += self.velocity.x * Config.FRICTION
        self.velocity += self.acceleration
        change = self.velocity + 0.5 * self.acceleration
        self.account_for_collision(change)

    def render_environment(self):
        game_display.fill((0, 0, 0))
        for game_object in self.objects.values():
            game_display.blit(*game_object.draw(self.player.positions.x))
        display.update()


environment = Environment()
environment.add_object(GameObject("wall", vec(0, Config.SCREEN_HEIGHT), vec(400, 50)))
environment.add_object(GameObject("wall", vec(0, Config.SCREEN_HEIGHT-50), vec(50, 50)))

while True:
    environment.render_environment()
    environment.update(pygame.key.get_pressed())
    pygame.event.pump()
    frames_per_second.tick(60)
