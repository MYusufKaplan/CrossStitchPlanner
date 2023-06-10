import pickle
import multiprocessing
import os
import sys
import neat
from canvas import Canvas
import numpy as np
import math
import random
from neat import parallel
from datetime import datetime

RUNCOUNT = 5
projectName = "testrun"

matrix = [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]


def runTest(genome):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    return fullRun(genome, config)


def run(config_path):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    globals()['population_size'] = len(pop.population)
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, 1000)
    # best = runTest(winner)
    # print("\nBest's Full Result: {}".format(best))
    # with open("best_{}_{}.pkl".format(projectName,datetime.now()),"wb") as f:
    #     pickle.dump(winner, f)
    #     f.close()

def fullRun(genome, config):
    # Show Best Run
    return genome


def eval_genome(genome, config):
    genome.fitness = 0
    totalFitness = 0
    try:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for runC in range(0,RUNCOUNT):
            canvas = Canvas(matrix, genome=genome, network=net)
            for color in canvas.colors:
                canvas.activeString = color
                while canvas.colorPath[color]['left'] > 0:
                    # TODO mashedinput needs to be changed...
                    output = net.activate(canvas.mashedInput)
                    output[0] = round(output[0]* (len(canvas.squares) - 1))
                    if output[1] > 0.5:
                        if not canvas.cutString():
                            genome.fitness = 5*len(canvas.squares)
                            colorfitness = 5*len(canvas.squares)
                            break
                        genome.fitness = canvas.colorPath[color]["stringUsed"]
                        continue
                    if not canvas.colorSquare(canvas.squares[output[0]]):
                        genome.fitness = 5*len(canvas.squares)
                        colorfitness = 5*len(canvas.squares)
                    genome.fitness = canvas.colorPath[color]["stringUsed"]
                    colorfitness = canvas.colorPath[color]["stringUsed"]
                totalFitness += colorfitness
        genome.fitness = totalFitness / RUNCOUNT
        return genome.fitness
    except Exception as e:
        print(e)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_feedforward.txt')
    run(config_path)