import neat
import pygame

from game import Environment, frames_per_second, game_display

imgarray = []
xpos_end = 0


def evaluate_genomes(genomes, config):
    global environments, genomes_list, nets
    environments = []
    genomes_list = []
    nets = []
    for genome_id, genome in genomes:
        environments.append(Environment())
        genomes_list.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    environment.create_ground()
    environment.render_environment()
    environment.get_keys()
    pygame.event.pump()
    frames_per_second.tick(60)


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
    config_path = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')
    run(config_path)