import pygame

from pygame import display, Surface
from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()


class GameObject:
    def __init__(self, positions, size=Config.WALL_SIZE, colour=Config.WALL_COLOUR, deadly=False):
        self.surface = Surface(vec(size))
        self.surface.fill(colour)
        self.rectangle = self.surface.get_rect()
        self.rectangle.bottomleft = positions
        self.deadly = deadly

    def __eq__(self, other):
        return self.rectangle.bottomleft == other.rectangle.bottomleft

    def draw(self, shift=0):
        rectangle = self.rectangle.copy()
        rectangle.left -= shift
        return self.surface, rectangle


class Player(GameObject):
    def __init__(self, positions=(0, Config.SCREEN_HEIGHT - Config.WALL_SIZE[1]), size=Config.PLAYER_SIZE, colour=Config.PLAYER_COLOUR):
        super().__init__(positions, size, colour)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.colliding = True
        self.dead = False


class Environment:
    def __init__(self):
        self.objects = {}
        self.deadly_object = GameObject((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), deadly=True)
        self.players = []

    def add_object(self, game_object):
        self.objects[game_object.rectangle.bottomleft] = game_object

    def get_object(self, coordinates):
        return self.objects.get(coordinates)

    def get_furthest_player(self):
        return max(self.players, key=lambda player: player.rectangle.left).rectangle.left

    def account_for_collision(self, player):
        player.colliding = False
        if player.rectangle.colliderect(self.deadly_object.rectangle):
            player.dead = True
        if player.rectangle.bottom >= Config.SCREEN_HEIGHT:
            player.velocity.y = 0
            player.rectangle.bottom = Config.SCREEN_HEIGHT
            player.colliding = True
        player.previous_rectangle = player.rectangle.copy()

    def get_keys(self):
        keys = pygame.key.get_pressed()
        self.update(self.players[0], (keys[KeyBinds.RIGHT], keys[KeyBinds.UP], keys[KeyBinds.LEFT]))

    def update(self, player, keys):
        if player.dead:
            return
        player.acceleration = vec(0, 0)
        player.acceleration.y += 0 if player.colliding else Config.GRAVITY
        if keys[0] > 0.5:
            player.acceleration.x = Config.ACCELERATION
        if keys[1] > 0.5:
            if player.colliding:
                player.velocity.y = Config.JUMPING_POWER
        if keys[2] > 0.5:
            player.acceleration.x = -Config.ACCELERATION
        player.acceleration.x += player.velocity.x * Config.FRICTION
        player.velocity += player.acceleration
        change = player.velocity + 0.5 * player.acceleration
        player.rectangle.bottomleft += vec(round(change.x, 0), round(change.y, 0))
        self.account_for_collision(player)

    def render_environment(self):
        game_display.fill((0, 0, 0))
        shift = self.get_furthest_player()
        for player_object in self.players:
            game_display.blit(*player_object.draw(shift))
        game_display.blit(*self.deadly_object.draw(shift))
        display.update()

    def create_ground(self):
        furthest_player = self.get_furthest_player()
        if self.deadly_object.rectangle.right < furthest_player:
            self.deadly_object.rectangle.left = furthest_player + Config.SCREEN_WIDTH


if __name__ == "__main__":
    environment = Environment()
    player = Player()
    environment.players.append(player)
    while True:
        environment.create_ground()
        environment.render_environment()
        environment.get_keys()
        pygame.event.pump()
        frames_per_second.tick(60)