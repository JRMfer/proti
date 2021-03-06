"""
dee.py

Minor Programmeren
Team Proti

Uses a Dead End Elimination like algorithm described by Okke to create a tree of all routes that are possibly lower than a preset score. 
"""
from anytree import Node, RenderTree, Walker, PreOrderIter
import copy
import matplotlib.pyplot as plt 
import timeit
from progress.bar import Bar

# lists with different proteins, some from the website and some created for testing, comment out the ones not needed

# protein = ['H', 'H', 'P', 'H', 'H', 'H', 'P', 'H'] # official 8, mc -3
protein = ['H', 'H', 'P', 'H', 'H', 'H', 'P', 'H', 'P', 'H', 'H', 'H', 'P', 'H'] # official 14, mc -6
# protein = ['H', 'P', 'H', 'P', 'P', 'H', 'H', 'P', 'H', 'P', 'P', 'H', 'P', 'H', 'H', 'P', 'P', 'H', 'P', 'H'] # official 20, mc -9
# protein = ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'H', 'H', 'P', 'P', 'H', 'P', 'P'] # official 36, mc -10
# protein = ['H', 'H', 'P', 'H', 'H', 'H', 'P', 'H', 'P', 'H', 'H', 'H', 'P', 'H', 'H', 'H', 'P', 'H', 'H', 'H', 'P', 'H', 'P', 'H', 'H', 'H', 'P', 'H'] # double 14, mc -12
# protein = ['H', 'C', 'P', 'H', 'P', 'C', 'P', 'H', 'P', 'C', 'H', 'C', 'H', 'P', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'P', 'H', 'P', 'C', 'P', 'H', 'P', 'P', 'P', 'H', 'P', 'H', 'H', 'H', 'C', 'C', 'H', 'C', 'H', 'C', 'H', 'C', 'H', 'H'] # official 50
# protein = ['H', 'H', 'P', 'H', 'C', 'H', 'P', 'C', 'P', 'C', 'H'] #  mc -3
# protein = ['P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P'] # okke short, mc -4
# protein = ['H', 'P', 'P', 'H', 'P', 'H', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P'] # okke long, mc -6
# protein = ['H', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'P', 'H', 'H'] # opt -9
# protein = ['P', 'P', 'H', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'P', 'H', 'H'] # op -8
protein = ['H', 'P', 'P', 'H', 'P', 'P', 'H', 'P', 'H', 'P', 'P', 'H', 'P']
protein = ['H', 'H', 'P', 'H', 'C', 'H', 'P', 'C', 'P', 'C', 'H'] #  mc -3


length = len(protein)
print(length)
# set theoretical lower bound on score
even = protein[::2]
odd = protein[1::2]
min_score = 2 * max([- even.count('H') - 5 * even.count('C'), - odd.count('H') - 5 * odd.count('C')])



def main():
    
    # initiate a progress bar
    bar = Bar('Progress', max=length)

    # direction of atom relative to the previous ones
    directions = ['left', 'right', 'straight']

    """
    Setting this variable right allows the program to run well. 
    It makes sure no branches are explored that couldn't possibly get a score lower than this lowest known score.
    Setting it too high means the program is slow as it will start constructing 3^(n-1) branches.
    Setting it too low results in finding no solutions.
    You can find the lowest known score by running one of the other faster but less certain programs first.
    """
    lowest_known_score = -0
    
    # variables to keep track of the optimal configuration
    best_score = 0
    best_x = []
    best_y = []
    atom_time = []
    keep_going = True

    # loop for constructing the tree
    for i, p in enumerate(protein):
        atom_start = timeit.default_timer()
        # stops when the remaining atoms can't add to the score
        if keep_going:

            # keep track of how many nodes are added per depth level
            breadth_counter = 0

            # place the first atom
            # intermezzo: the loop relies heavily on the globals()[...] function
            # it creates a transforms a stirng into an actual variable and allows for dynamic naming and referencing of the nodes
            if i == 0:
                name = f'{p}{i}{i}'
                globals()[name] = Node('start')
                bar.next()
                continue
            
            # second atom is placed in one direction only, others would merely be a rotaion around the axis with no score advantage
            if i == 1:
                name = f'{p}{i}{i}'
                globals()[name] = Node('left', parent=globals()[f'{protein[0]}00'])
                bar.next()
                continue

            # determines how many nodes there are in in the previous tree layer
            parent_counter = len(list(PreOrderIter(globals()[f'{protein[0]}00'], filter_=lambda node: node.is_leaf)))
        
            # for each node, create a new one in every direction
            for j in range(len(directions) * parent_counter):

                # get the name of the parent node
                parent = f'{protein[i-1]}{i-1}{j}'

                # see if that parent exists, if not its score was too high and no further node along that branch has to be made
                try:
                    globals()[parent]
                except:
                    continue
            
                # if it exist contruct a new node for each direction
                for d in directions:
                    
                    # name of the node to be
                    name = f'{p}{i}{breadth_counter}'
                    
                    # see which nodes are visited already to get to this point in the tree
                    nodes_visited = [node.name for node in globals()[parent].path]
                    # the atoms still to be placed
                    nodes_to_visit = protein[i:]
                    # print(nodes_to_visit)

                    # score of the protien so far
                    partial_score = partial_score_func(nodes_visited)

                    # lowest score possible given the remaining atoms
                    possible_score = possible_score_func(nodes_to_visit, partial_score, lowest_known_score)

                    if partial_score < lowest_known_score:
                        lowest_known_score = copy.deepcopy(partial_score)
            
                    # new node is only made if it is possible to get a score lower than the lowest known score
                    if partial_score + possible_score >= lowest_known_score and possible_score != 0:
                        breadth_counter += 1
                        continue
                    
                    # create new node
                    globals()[name] = Node(d, parent=globals()[parent])
                    breadth_counter += 1

                    # this part only runs when the last atom is placed or the remaining atoms can't add to the score
                    if i == length - 1 or possible_score == 0:
                    
                        # determine the path of the string
                        nodes_visited = [node.name for node in globals()[name].path]
                        pos_x, pos_y = direction_to_xy(nodes_visited)

                        # disregard foldings onto itself
                        if double(pos_x, pos_y):
                            continue
                        
                        # get the structures score
                        current_score = score(pos_x, pos_y)

                        # save if it is an improvemnt
                        if current_score <= best_score:
                            best_x = copy.deepcopy(pos_x)
                            best_y = copy.deepcopy(pos_y)
                            best_score = copy.deepcopy(current_score)
                           
                        # stop running if the remaining atoms can't add to the score
                        if possible_score == 0:
                            keep_going = False

        # log how long each iteration takes
        atom_stop = timeit.default_timer()
        atom_time.append(atom_stop - atom_start)

        # update the progress bar
        bar.next()

    # stop the progres bar and timer
    bar.finish()
    stop = timeit.default_timer()

    # print some interesting information and plot best result
    print(f'Lowest theoretical score: {min_score}')
    print('Runtime: %.4f seconds' %(stop - start))
    if len(nodes_to_visit) > 1:
        print(f'{nodes_to_visit[1:]} are not placed since they would not add to the score')

    if len(best_x) == 0:
        print('No stable solution')
    else:
        plot(best_x, best_y, best_score, atom_time, stop - start)


def terminal_display(root):
    """Prints a graphical representation of the tree to the terminal."""

    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def plot(list_x, list_y, score, atom_time, total_time):
    """Makes a graph of two lists list_x, list_y."""
    
    # differentiate between types of atom
    red_dots_x = []
    red_dots_y = []
    blue_dots_x = []
    blue_dots_y = []
    yellow_dots_x = []
    yellow_dots_y = []

    # search through protein and place each atom in the appropiate list
    for x, y, p in zip(list_x, list_y, protein):

        if p == 'H':
            red_dots_x.append(x)
            red_dots_y.append(y)
        if p == 'P':
            blue_dots_x.append(x)
            blue_dots_y.append(y)       
        if p == 'C':
            yellow_dots_x.append(x)
            yellow_dots_y.append(y)

   # create graphs with colors
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 9))

    ax1.plot(list_x, list_y, '--', color='darkgrey')
    ax1.plot(red_dots_x, red_dots_y, 'or', markersize=17)
    ax1.plot(blue_dots_x, blue_dots_y, 'ob', markersize=17)
    ax1.plot(yellow_dots_x, yellow_dots_y, 'oy', markersize=17)
    ax1.set_title(f'Folded protein of length {length}, score: {score}')

    ax2.plot(atom_time)
    ax2.set_title(f'Time per atom, {round(total_time,2)} seconds total')
    ax2.set(xlabel='Atom', ylabel='Time')

    plt.show()


def direction_to_xy(nodes_visited):
    """Converts a series of string with directions like ['left', 'right'] to lists with xy positions."""

    pos_x = [0,1]
    pos_y = [0,0]

    # go over every node
    for i, n in enumerate(nodes_visited):
        
        # first two nodes are already placed to confine solutions to one quadrant
        if i == 0 or i == 1:
            continue
        
        # previous direction is determined
        delta_x = pos_x[-1] - pos_x[-2]
        delta_y = pos_y[-1] - pos_y[-2]

        # rotation matrices used to turn into the desired direction
        if n == 'straight':
            pos_x.append(pos_x[-1] + delta_x)
            pos_y.append(pos_y[-1] + delta_y)
        elif n == 'left':
            pos_x.append(pos_x[-1] - delta_y)
            pos_y.append(pos_y[-1] + delta_x)
        elif n == 'right':
            pos_x.append(pos_x[-1] + delta_y )
            pos_y.append(pos_y[-1] - delta_x)

    return pos_x, pos_y

def partial_score_func(nodes_visited):
    """Calculates the socre obtained by the nodes visit so far."""

    pos_x, pos_y = direction_to_xy(nodes_visited)

    # weed out the proteins folded into itself
    if double(pos_x, pos_y):
        return 1000

    partial_score = score(pos_x, pos_y)

    return partial_score


def possible_score_func(nodes_to_visit, partial_score, lowest_known_score):
    """Calculates the best score the remaining bit of the protien can acquire."""

    possible_score = 0

    # an H atom can get at most -2 and a C atom at best -10
    for i, n in enumerate(nodes_to_visit):

        if i == len(nodes_to_visit) - 1:
            if n == 'H':
                possible_score += -3
            if n == 'C':
                possible_score += -15
            continue

        if n == 'H':
             possible_score += -2
        if n == 'C':
            possible_score += -10

    if possible_score + partial_score < min_score:
        possible_score = min_score - partial_score
        if lowest_known_score == min_score:
            possible_score += -1
        
    return possible_score


def score(list_x, list_y):
    """Given the coordinates of a protein string, calculate the score of the shape."""

    # list to place the 'already scored' atoms into
    coordinates = []
    directions = [[-1,0],[0,1],[1,0],[0,-1]]
    length = len(list_x)
    score = 0

    for i in range(length):

        # P's dont interact so can skip those cases
        if not protein[i] == 'P':

            # for every atom look around in all 4 directions
            for d in directions:

                # check whether one of the previously placed atoms is in the vicinity and determine the score of the interaction with it and the current atom
                for j in range(len(coordinates)):

                    if [list_x[i] + d[0], list_y[i] + d[1]] == coordinates[j] and not(list_x[i] + d[0] == list_x[i-1] and list_y[i] + d[1] == list_y[i-1]):
                        
                        if protein[i] == 'H':
                            if protein[j] == 'H' or protein[j] == 'C':
                                score += -1

                        if protein[i] == 'C':
                            if protein[j] == 'C':
                                score += -5
                            if protein[j] == 'H':
                                score += -1 

        # place in the list with coordinates
        coordinates.append([list_x[i], list_y[i]])
    
    return score


def double(list_x, list_y):
    """Checks whether two atoms occupy the same point."""

    coordinates = []

    # see if a coordinate is already in the list, then add that coordinate to the list
    for x, y in zip(list_x, list_y):
        if [x,y] in coordinates:
            return True
        coordinates.append([x,y])
    
    return False

if __name__ == "__main__":
    start = timeit.default_timer()
    main()