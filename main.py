import pygame

from pygame import display, Surface
from random import randint
from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()


class GameObject:
    def __init__(self, positions, size=Config.WALL_SIZE, colour=Config.WALL_COLOUR):
        self.surface = Surface(vec(size))
        self.surface.fill(colour)
        self.previous_rectangle = self.surface.get_rect()
        self.previous_rectangle.bottomleft = positions
        self.rectangle = self.surface.get_rect()
        self.rectangle.bottomleft = positions

    def __eq__(self, other):
        return self.rectangle.bottomleft == other.rectangle.bottomleft

    def draw(self, shift=0):
        rectangle = self.rectangle.copy()
        rectangle.left -= shift
        return self.surface, rectangle


class Environment:
    def __init__(self):
        self.objects = {}
        self.player = GameObject(vec(0, Config.LEVEL_HEIGHT), Config.PLAYER_SIZE, Config.PLAYER_COLOUR)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.colliding = True
        self.score = 0
        for i in range(0, Config.SCREEN_WIDTH, Config.WALL_SIZE[0]):
            self.add_object(GameObject(vec(i, Config.SCREEN_HEIGHT)))

    def add_object(self, game_object):
        self.objects[game_object.rectangle.bottomleft] = game_object

    def get_object(self, coordinates):
        return self.objects.get(coordinates)

    def get_center_distance(self, rectangle):
        return vec(*self.player.rectangle.center).distance_squared_to(vec(*rectangle.center))

    def get_object_collision(self):
        for game_object in self.objects.values():
            if game_object.rectangle.colliderect(self.player.rectangle):
                return game_object.rectangle
        return None

    def account_for_collision(self):
        self.colliding = False
        while collision := self.get_object_collision():
            if self.player.previous_rectangle.bottom <= collision.top:
                self.velocity.y = 0
                self.player.rectangle.bottom = collision.top
                self.colliding = True
            if self.player.previous_rectangle.top >= collision.bottom:
                self.velocity.y = 0
                self.player.rectangle.top = collision.bottom
            if self.player.previous_rectangle.right <= collision.left:
                self.velocity.x = 0
                self.player.rectangle.right = collision.left
            if self.player.previous_rectangle.left >= collision.right:
                self.velocity.x = 0
                self.player.rectangle.left = collision.right
        self.player.previous_rectangle = self.player.rectangle.copy()

    def update(self, keys):
        self.acceleration = vec(0, 0)
        self.acceleration.y += 0 if self.colliding else Config.GRAVITY
        if keys[KeyBinds.RIGHT]:
            self.acceleration.x = Config.ACCELERATION
        if keys[KeyBinds.UP]:
            if self.colliding:
                self.velocity.y = Config.JUMPING_POWER
        self.acceleration.x += self.velocity.x * Config.FRICTION
        self.velocity += self.acceleration
        change = self.velocity + 0.5 * self.acceleration
        self.player.rectangle.bottomleft += vec(round(change.x, 0), round(change.y, 0))
        self.account_for_collision()
        self.score = self.player.rectangle.left if self.player.rectangle.left > self.score else self.score

    def render_environment(self):
        to_delete = []
        game_display.fill((0, 0, 0))
        game_display.blit(*self.player.draw(self.player.rectangle.left))
        for game_object in self.objects.values():
            if game_object.rectangle.right < self.player.rectangle.left:
                to_delete.append(game_object.rectangle.bottomleft)
            game_display.blit(*game_object.draw(self.player.rectangle.left))
        for positions in to_delete:
            del self.objects[positions]
        display.update()

    def create_ground(self):
        positions = (Config.SCREEN_WIDTH + Config.WALL_SIZE[0] * (self.player.rectangle.left // Config.WALL_SIZE[0]), Config.SCREEN_HEIGHT)
        if not self.get_object(positions):
            self.add_object(GameObject(positions))
            counter = Config.SCREEN_HEIGHT
            while randint(0, 1):
                counter -= Config.WALL_SIZE[1]
                if counter <= Config.WALL_SIZE[1] * 3:
                    break
                self.add_object(GameObject((positions[0], counter)))


environment = Environment()


while True:
    environment.create_ground()
    environment.render_environment()
    environment.update(pygame.key.get_pressed())
    pygame.event.pump()
    frames_per_second.tick(60)
