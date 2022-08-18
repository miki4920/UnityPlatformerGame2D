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
        self.rectangle = self.surface.get_rect()
        self.rectangle.bottomleft = positions

    def __eq__(self, other):
        return self.rectangle.bottomleft == other.rectangle.bottomleft

    def draw(self, shift=0):
        rectangle = self.rectangle.copy()
        rectangle.left -= shift
        return self.surface, rectangle


class Player(GameObject):
    def __init__(self, positions, size=Config.PLAYER_SIZE, colour=Config.PLAYER_COLOUR):
        super().__init__(positions, size, colour)
        self.previous_rectangle = self.surface.get_rect()
        self.previous_rectangle.bottomleft = positions
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.colliding = True


class Environment:
    def __init__(self):
        self.objects = {}
        self.players = {}
        for i in range(0, Config.SCREEN_WIDTH, Config.WALL_SIZE[0]):
            self.add_object(GameObject(vec(i, Config.SCREEN_HEIGHT)))

    def add_object(self, game_object):
        self.objects[game_object.rectangle.bottomleft] = game_object

    def add_player(self, player_id, player):
        self.players[player_id] = player

    def get_object(self, coordinates):
        return self.objects.get(coordinates)

    def get_furthest_player(self):
        return max(self.players.values(), key=lambda player: player.rectangle.left).rectangle.left

    def get_nearest_obstacle(self, player):
        objects = [game_object for game_object in self.objects.values() if game_object.rectangle.left + 1 > player.rectangle.right]
        return min(objects, key=lambda game_object: game_object.rectangle.topleft).rectangle.topleft

    def get_object_collision(self, player):
        for game_object in self.objects.values():
            if game_object.rectangle.colliderect(player.rectangle):
                return game_object.rectangle
        return None

    def account_for_collision(self, player):
        player.colliding = False
        while collision := self.get_object_collision(player):
            if player.previous_rectangle.bottom <= collision.top:
                player.velocity.y = 0
                player.rectangle.bottom = collision.top
                player.colliding = True
            if player.previous_rectangle.top >= collision.bottom:
                player.velocity.y = 0
                player.rectangle.top = collision.bottom
            if player.previous_rectangle.right <= collision.left:
                player.velocity.x = 0
                player.rectangle.right = collision.left
            if player.previous_rectangle.left >= collision.right:
                player.velocity.x = 0
                player.rectangle.left = collision.right
        player.previous_rectangle = player.rectangle.copy()

    def get_keys(self):
        keys = pygame.key.get_pressed()
        self.update(self.players[1], (keys[KeyBinds.RIGHT], keys[KeyBinds.UP], keys[KeyBinds.LEFT]))

    def update(self, player, keys):
        player.acceleration = vec(0, 0)
        player.acceleration.y += 0 if player.colliding else Config.GRAVITY
        if keys[0]:
            player.acceleration.x = Config.ACCELERATION
        if keys[1]:
            if player.colliding:
                player.velocity.y = Config.JUMPING_POWER
        if keys[2]:
            player.acceleration.x = -Config.ACCELERATION
        player.acceleration.x += player.velocity.x * Config.FRICTION
        player.velocity += player.acceleration
        change = player.velocity + 0.5 * player.acceleration
        player.rectangle.bottomleft += vec(round(change.x, 0), round(change.y, 0))
        self.account_for_collision(player)

    def render_environment(self):
        to_delete = []
        game_display.fill((0, 0, 0))
        shift = self.get_furthest_player()
        for player_object in self.players.values():
            game_display.blit(*player_object.draw(shift))
        for game_object in self.objects.values():
            if game_object.rectangle.right < shift:
                to_delete.append(game_object.rectangle.bottomleft)
            game_display.blit(*game_object.draw(shift))
        for positions in to_delete:
            del self.objects[positions]
        display.update()

    def create_ground(self):
        self.get_nearest_obstacle(self.players[1])
        positions = (Config.SCREEN_WIDTH + Config.WALL_SIZE[0] * (self.get_furthest_player() // Config.WALL_SIZE[0]), Config.SCREEN_HEIGHT)
        if not self.get_object(positions):
            self.add_object(GameObject(positions))
            counter = Config.SCREEN_HEIGHT
            while randint(0, 1):
                counter -= Config.WALL_SIZE[1]
                if counter <= Config.WALL_SIZE[1] * 3:
                    break
                self.add_object(GameObject((positions[0], counter)))


if __name__ == "__main__":
    environment = Environment()
    player = Player((0, Config.SCREEN_HEIGHT - Config.WALL_SIZE[1]))
    environment.add_player(1, player)
    while True:
        environment.create_ground()
        environment.render_environment()
        environment.get_keys()
        pygame.event.pump()
        frames_per_second.tick(60)