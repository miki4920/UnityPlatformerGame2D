import neat
import pygame

from game import Environment, frames_per_second, game_display

imgarray = []
xpos_end = 0


def evaluate_genomes(genomes, config):
    for genome_id, genome in genomes:
        pass


environment = Environment()
while True:
    environment.create_ground()
    environment.render_environment()
    environment.get_keys()
    pygame.event.pump()
    frames_per_second.tick(60)
    print(pygame.surfarray.array3d(game_display.copy()))
    # print(image[:, :, ::-1])
# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                      'config-feedforward')
#
# p = neat.Population(config)
#
# p.add_reporter(neat.StdOutReporter(True))
# stats = neat.StatisticsReporter()
# p.add_reporter(stats)
# p.add_reporter(neat.Checkpointer(10))
#
# winner = p.run(evaluate_genomes)
