import pickle
import multiprocessing
import os
import sys
import json
import neat
from canvas import Canvas
import numpy as np
import math
import random
from neat import parallel
from datetime import datetime
import pprint


# RUNCOUNT = 5
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
    winner = pop.run(pe.evaluate, 3)
    best = runTest(winner)
    clrpath = json.dumps(best.colorPath,indent=2)
    print("\nBest's Full Result:\n{}".format(clrpath))
    with open("best_{}_{}.pkl".format(projectName,datetime.now()),"wb") as f:
        pickle.dump(winner, f)
        f.close()

def fullRun(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    canvas = Canvas(matrix, genome=genome, network=net)
    for color in canvas.colors:
        canvas.activeString = color
        while canvas.colorPath[color]['left'] > 0:
            output = net.activate(canvas.generateMashed())
            output[0] = round(output[0]* (len(canvas.squaresLeft) - 1))
            if output[1] > 0.5:
                if not canvas.cutString():
                    break
                continue
            canvas.colorSquare(canvas.squaresLeft[output[0]])
    return canvas


def eval_genome(genome, config):
    genome.fitness = 0
    totalFitness = 0
    try:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        # for runC in range(0,RUNCOUNT):
        canvas = Canvas(matrix, genome=genome, network=net)
        for color in canvas.colors:
            canvas.activeString = color
            while canvas.colorPath[color]['left'] > 0:
                output = net.activate(canvas.generateMashed())
                output[0] = round(output[0]* (len(canvas.squaresLeft) - 1))
                # print(canvas.colorPath[color]["path"])
                if output[1] > 0.5:
                    if not canvas.cutString():
                        genome.fitness = -1 * (99 * canvas.colorPath[color]['left'] - canvas.colorPath[color]["stringUsed"])
                        colorfitness = -1 * (99 * canvas.colorPath[color]['left'] - canvas.colorPath[color]["stringUsed"])
                        break
                    genome.fitness = -1 * (canvas.colorPath[color]["stringUsed"])
                    continue
                canvas.colorSquare(canvas.squaresLeft[output[0]])
                genome.fitness = -1 * (canvas.colorPath[color]["stringUsed"])
                colorfitness = -1 * (canvas.colorPath[color]["stringUsed"])
            # if canvas.colorPath[color]['left'] == 0:
            #     print("FINISHED {}".format(color))
            totalFitness += colorfitness
        genome.fitness = totalFitness
        return genome.fitness
    except Exception as e:
        print(e)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_feedforward.txt')
    run(config_path)