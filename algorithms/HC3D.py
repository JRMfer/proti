"""
HC3D.py

Minor Programmeren
Team Proti

Tries to find the most stable configuration of the protein in 3D
as per the Hill climber method
"""

# import modules
from generalhelpers import score_it, random_rotation_xyz, double, output, plot
import random
import copy
import timeit
from progress.bar import Bar

def run(proti):
    # start timing the run of the code
    start = timeit.default_timer()

    # initialize the protein in a straight configuration
    x = [i for i in range(proti.length)]
    y = [0] * proti.length
    z = [0] * proti.length

    # high number of iterations for optimising result
    iterations = 50000
    rotations = 0

    # initialize progress bar
    bar = Bar('Progress', max = iterations / 1000)

    # list to keep track of best configuration and scores
    lowest_score = 0
    best_x = []
    best_y = []
    best_z = []
    scores = []

    # fold protein for number of iterations
    while rotations < iterations:

        # remember the previous configuration
        backup_x = copy.deepcopy(x)
        backup_y = copy.deepcopy(y)
        backup_z = copy.deepcopy(z)

        # remember the previous score
        old_score = score_it(list_x=backup_x, list_y=backup_y, list_z=backup_z,
                             proti=proti)
        scores.append(old_score)

        # fold protein at a random amino
        rotating_amino = random.randint(0, proti.length - 1)
        random_rotation_xyz(list_x=x, list_y=y, list_z=z, n=rotating_amino,
                            proti=proti) 

        # if protein folded into itself restore and go back
        if double(list_x=x, list_y=y):
            x = backup_x
            y = backup_y
            z = backup_z
            continue

        # get the score of the current configuration
        new_score = score_it(list_x=x, list_y=y, list_z=z, proti=proti)

        # if the new score is worse set configuration back 
        if new_score > old_score:
            x = backup_x
            y = backup_y
            z = backup_z
            new_score = old_score

        # check if a lower score has been found and remember
        if new_score < lowest_score:
            best_x = copy.deepcopy(x)
            best_y = copy.deepcopy(y)
            best_z = copy.deepcopy(z)
            lowest_score = copy.deepcopy(new_score)

        rotations += 1 

        # continue the progress bar every thousand configuration
        if rotations % 1000 == 0:
            bar.next()

    # finish the progress bar and the timer and show information
    bar.finish()
    stop = timeit.default_timer()
    print('Runtime:', stop - start, 'seconds')

    # render the output and plot the figure
    output(list_x=best_x, list_y=best_y, list_z=best_z, score=lowest_score,
           proti=proti)
    plot(proti, lowest_score, best_x, best_y, 'Score after rotation', 'Rotation', 'Score', best_z, scores=scores)
