"""
SIMANN+.py

Renamed and reorganized some parts of monte.py for convenience
Simmulated annealing seems to work
Tweaking start temperature and iterations to figure out what combo works best
Best till now seems to be -28
"""

import numpy as np 
import matplotlib.pyplot as plt 
import random
import math
import copy

# PROTEIN = 'PPHPPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHPHH'
PROTEIN = 'CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC'
PROTEIN = ['H', 'P', 'H', 'P', 'P', 'H', 'H', 'P', 'H', 'P', 'P', 'H', 'P', 'H', 'H', 'P', 
  'P', 'H', 'P', 'H'] # 20, opt -9, bench 0.21, -8
PROTEIN = ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 
  'H', 'H', 'H', 'H', 'H', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'H', 'H', 'P', 'P', 'H', 'P', 'P'] # 36,  opt -14, bench 4.6, -12
PROTEIN = ['P', 'P', 'H', 'P', 'P', 'H', 'P', 'H', 'P', 'H', 'H', 'H', 'H', 'P', 'H', 'P', 
  'P', 'P', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 
      'P', 'H', 'P', 'H', 'H', 'H', 'H', 'P', 'H', 'P', 'H', 'P', 'H', 'P', 'H', 'H']  # 50, opt -21 low -16

LENGTH = len(PROTEIN)
ITERATIONS = 50000
DIRECTIONS = [[-1, 0], [0, 1], [1, 0], [0, -1]]
START_TEMP = 100

def main():
    x = [i for i in range(LENGTH)]
    y = [0] * LENGTH
    

    rotations = 0
    lowest_score = 0
    best_x = []
    best_y = []
    scores = []

    local_optimum = False
    local_optimum_rotation = 0

    while rotations < ITERATIONS:

        backup_x = copy.deepcopy(x)
        backup_y = copy.deepcopy(y)

        rotating_amino = random.randint(0, LENGTH - 1)
        fold_protein(x, y, rotating_amino)

        if double(x, y):
            x = backup_x
            y = backup_y
            continue

        old_score = score(backup_x, backup_y)
        new_score = score(x, y)

        if rotations % 1000 == 0:
            if new_score == old_score:                
                local_optimum = True

        if local_optimum == True:
            local_optimum_rotation = rotations
            print("Found local optimum")
            local_optimum = False

        temperature = START_TEMP * (0.997 ** (rotations - local_optimum_rotation))
        # temperature = START_TEMP - (START_TEMP / ITERATIONS) * rotations
        acceptance_chance = 2 ** ((old_score - new_score)/temperature)
        treshhold = random.random()

        if new_score > old_score and acceptance_chance < treshhold:
            x = backup_x
            y = backup_y

        scores.append(old_score)

        if old_score < lowest_score:
            best_x = copy.deepcopy(x)
            best_y = copy.deepcopy(y)
            lowest_score = copy.deepcopy(old_score)

        rotations += 1

    visualization(best_x, best_y, lowest_score, scores)


def double(x, y):
    coordinates = []

    for amino_x, amino_y in zip(x, y):
        if [amino_x, amino_y] in coordinates:
            return True
        coordinates.append([amino_x, amino_y])

    return False


def fold_protein(x, y, amino_pos):

    rotating_amino_x = x[amino_pos]
    rotating_amino_y = y[amino_pos]

    direction = random.random()

    for i in range(amino_pos + 1, LENGTH):
        relative_x = x[i] - rotating_amino_x
        relative_y = y[i] - rotating_amino_y

        if direction > 0.5:
            # rotate left
            x[i] = rotating_amino_x - relative_y
            y[i] = rotating_amino_y + relative_x
        else:
            # rotate right
            x[i] = rotating_amino_x + relative_y
            y[i] = rotating_amino_y - relative_x


def score(x, y):
    coordinates = []
    score = 0

    for i in range(LENGTH):

        if not PROTEIN[i] == 'P':
            
            for direction in DIRECTIONS:
                dir_x = direction[0]
                dir_y = direction[1]
                check_x = x[i] + dir_x
                check_y = y[i] + dir_y

                for j in range(len(coordinates)):

                    if [check_x, check_y] == coordinates[j] and not \
                        (check_x == x[i - 1] and check_y == y[i - 1]):

                        protein = PROTEIN[i]
                        neighbour = PROTEIN[j]

                        if protein == 'H':
                            if neighbour == 'H' or neighbour == 'C':
                                score += -1

                        if protein == 'C':
                            if neighbour == 'C':
                                score += -5
                            if neighbour == 'H':
                                score += -1

        coordinates.append([x[i], y[i]])

    return score

def visualization(x, y, score, scores):

    H_x = []
    H_y = []
    P_x = []
    P_y = []
    C_x = []
    C_y = []

    iterations = [i for i in range(ITERATIONS)]

    for i in range(LENGTH):
        amino = PROTEIN[i]
        amino_x = x[i]
        amino_y = y[i]

        if amino == 'H':
            H_x.append(amino_x)
            H_y.append(amino_y)
        if amino == 'P':
            P_x.append(amino_x)
            P_y.append(amino_y)
        if amino == 'C':
            C_x.append(amino_x)
            C_y.append(amino_y)

    plt.figure()

    plt.subplot(211)
    plt.plot(x, y, "k--")
    plt.plot(H_x, H_y, "ro", label = "hydrofoob")
    plt.plot(P_x, P_y, "bo", label = "polair")
    plt.plot(C_x, C_y, "go", label = "cysteine")
    plt.xlabel("step")
    plt.ylabel("step")
    plt.legend()
    plt.title("Total score: {}".format(score))

    plt.subplot(212)
    plt.plot(iterations, scores)
    plt.title("Statistics")
    plt.xlabel("iterations")
    plt.ylabel("scores")
    plt.savefig("simannealplus.png")
    plt.show()


if __name__ == "__main__":
    main()