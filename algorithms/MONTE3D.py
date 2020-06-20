"""
MONTE3D.py

Minor Programmeren
Team Proti

Folds protein into the (probably) most stable state using a Monte Carlo algorithm. 
"""

# import modules
from helpers import *
import random
import math
import copy

def run(proti):

    # create the initial straight string
    pos_x = [i for i in range(proti.length)]
    pos_y = [0] * proti.length
    pos_z = [0] * proti.length

    # number of iterations, higher N is better result
    N = 100000
    rotation_counter = 0

    # lists to keep track of the scores and best configuration 
    lowest_score = 0
    best_x = []
    best_y = []
    best_z = []
    scores = []

    # probability functions depens on temperature and the boltzmann constant,
    # can be set to their actual values if you want to be physically responsible
    temperature = 1
    boltzmann = 1
    
    # loop that keeps folding the protein
    while rotation_counter < N:

        # a copy is made in case the fold is invalid or unfavourable
        log_pos_x = copy.deepcopy(pos_x)
        log_pos_y = copy.deepcopy(pos_y)
        log_pos_z = copy.deepcopy(pos_z)

        # protein is folded randomly
        random_rotation_xyz(pos_x, pos_y, pos_z, \
                            random.randint(0, proti.length - 1), proti)

        # check whether the protein has not folded onto itself
        if double_xyz(pos_x, pos_y, pos_z):
            # if it is folded wrongly, restore to the previous configuration
            pos_x = log_pos_x
            pos_y = log_pos_y
            pos_z = log_pos_z
            continue
        
        # calculate the scores of the old and new structure
        old_score = score_xyz(log_pos_x, log_pos_y, log_pos_z, proti)
        new_score = score_xyz(pos_x, pos_y, pos_z, proti)

        # keep track of each score
        scores.append(old_score)

        # if a score beats the old one, remember that structure 
        if new_score < lowest_score:
            best_x = copy.deepcopy(pos_x)
            best_y = copy.deepcopy(pos_y)
            best_z = copy.deepcopy(pos_z)
            lowest_score = copy.deepcopy(new_score)

        # probability function to determine whether a fold will be 'accepted' 
        p = math.exp(-(new_score - old_score)/(temperature * boltzmann))

        # the treshhold for acceptance varies and is randomly determined
        treshhold = random.random()
        if p < treshhold:
            pos_x = log_pos_x
            pos_y = log_pos_y
            pos_z = log_pos_z

        rotation_counter += 1

        # print statement for time indication in long calculations
        if rotation_counter % 1000 == 0:
            print(f'{rotation_counter / N * 100}%')

    # the best structure is copied to a csv file and shown in a graph
    output_xyz(best_x, best_y, best_z, lowest_score, proti)
    plot_xyz(best_x, best_y, best_z, lowest_score, scores, proti)
