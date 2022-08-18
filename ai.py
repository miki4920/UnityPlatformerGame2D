import neat
import pygame

from game import Environment, Player, frames_per_second

imgarray = []
xpos_end = 0


def evaluate_genomes(genomes, config):
    global environment, genomes_list, nets
    environment = Environment()
    genomes_list = []
    nets = []
    for genome_id, genome in genomes:
        environment.players.append(Player())
        genomes_list.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    while True:
        if len(environment.players) == 0:
            break
        environment.create_ground()
        environment.render_environment()
        shift = environment.get_furthest_player()
        to_delete = []
        for i, player in enumerate(environment.players):
            obstacle_x, obstacle_y = environment.deadly_object.rectangle.topleft
            output = nets[i].activate((player.rectangle.bottom, obstacle_x-player.rectangle.right, obstacle_y))
            environment.update(player, output)
            if player.dead or shift > player.rectangle.right:
                to_delete.append(i)
            genomes_list[i].fitness = player.rectangle.left
        to_delete = to_delete[::-1]
        for key in to_delete:
            del environment.players[key]
            del nets[key]
            del genomes_list[key]
        frames_per_second.tick(60)
        pygame.event.pump()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(evaluate_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    run('config-feedforward')