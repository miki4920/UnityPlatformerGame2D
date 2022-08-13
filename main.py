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
        self.surface = Surface(dimensions)
        self.surface.fill((128, 255, 40))
        self.previous_rectangle = self.surface.get_rect()
        self.previous_rectangle.bottomleft = positions
        self.rectangle = self.surface.get_rect()
        self.rectangle.bottomleft = positions

    def __eq__(self, other):
        return self.name == other.name

    def draw(self):
        return self.surface, self.rectangle


class Environment:
    def __init__(self):
        self.objects = {}
        self.player = GameObject("player", vec(0, 400), vec(50, 50))
        self.add_object(self.player)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def add_object(self, game_object):
        self.objects[str(game_object)] = game_object

    def get_object(self, name):
        return self.objects.get(name)

    def get_center_distance(self, rectangle):
        return vec(*self.player.rectangle.center).distance_squared_to(vec(*rectangle.center))

    def get_object_collision(self):
        collisions = []
        for game_object in self.objects.values():
            if game_object != self.player:
                if game_object.rectangle.colliderect(self.player.rectangle):
                    collisions.append(game_object.rectangle)
        if collisions:
            collisions = sorted(collisions, key=lambda collision: self.get_center_distance(collision))
        return collisions

    def account_for_collision(self):
        collisions = self.get_object_collision()
        while len(collisions) != 0:
            collision = collisions[0]
            self.velocity.y = 0
            if self.player.previous_rectangle.bottom <= collision.top:
                self.player.rectangle.bottom = collision.top
            if self.player.previous_rectangle.top >= collision.bottom:
                self.player.rectangle.top = collision.bottom
            if collision.colliderect(self.player.rectangle):
                if self.player.previous_rectangle.right <= collision.left:
                    self.player.rectangle.right = collision.left
                if self.player.previous_rectangle.left >= collision.right:
                    self.player.rectangle.left = collision.right

            collisions = self.get_object_collision()
        self.player.previous_rectangle = self.player.rectangle.copy()

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
        self.player.rectangle.bottomleft += vec(round(change.x, 0), round(change.y, 0))
        self.account_for_collision()

    def render_environment(self):
        game_display.fill((0, 0, 0))
        for game_object in self.objects.values():
            game_display.blit(*game_object.draw())
        display.update()


environment = Environment()
environment.add_object(GameObject("wall", vec(0, Config.SCREEN_HEIGHT), vec(50, 50)))
environment.add_object(GameObject("wall", vec(50, Config.SCREEN_HEIGHT), vec(50, 50)))
environment.add_object(GameObject("wall", vec(100, Config.SCREEN_HEIGHT), vec(50, 50)))
environment.add_object(GameObject("wall", vec(100, Config.SCREEN_HEIGHT-50), vec(50, 50)))
environment.add_object(GameObject("wall", vec(150, Config.SCREEN_HEIGHT), vec(50, 50)))

while True:
    environment.render_environment()
    environment.update(pygame.key.get_pressed())
    pygame.event.pump()
    frames_per_second.tick(60)
