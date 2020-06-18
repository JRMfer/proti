"""
From this main landing, multiple routes can be chosen. One at a time.
"""

from algorithms import BFBAB as BF
from algorithms import BFBAB3D as BF3D
from classes.protein import Protein
import re
import sys

if __name__ == "__main__":
    # Input for protein variable
    algos = 'BFBAB', 'BFBAB3D', 'DEE', 'FF', 'HC', 'MONTE', 'MONTE3D', 'SIMANN', 'SIMANN+', 'TREE'
    print(f'algorithms available: {algos}')
    usage = input("please input algorithm name followed by an underscore and a single protein string\n")
    usage = re.split('_+', usage)
    algo = usage[0]
    protein_list = list(usage[1])
    length = len(protein_list)
    allow_chars = ['P','C','H']

    for i in protein_list:
        if i not in allow_chars:
            sys.exit("Usage parameters not met. Please try again")

    if algo not in algos:
        sys.exit("Algorithm not found. Please try again")

    proti = Protein(protein_list, length)

    if algo == 'BFBAB':
        choice = BF.run(proti)




