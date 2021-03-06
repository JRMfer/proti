"""
main.py 

Minor Programmeren
Team Proti

All the algorithms can be accessed.
In the user interface the user can enter an algorithm to run 
and they can choose a protein to fold by entering the ID of the protein.
The available proteins and their respective ID's are printed to the terminal 
for the user to see
"""

# import modules
from algorithms import BFBAB as BF
from algorithms import BFBAB3D as BF3D
from algorithms import DEE
from algorithms import FF
from algorithms import HC
from algorithms import MONTE
from algorithms import MONTE3D as M3D
from algorithms import SIMANN as SA
from algorithms import SIMANN3D as SA3D
from algorithms import SIMANNPLUS as SAPLUS
from algorithms import SIMANNPLUS3D as SAPLUS3D
from algorithms import TREE 
from algorithms import GENETIC
from algorithms import HC3D
from classes.protein import Protein
import sys

def main():
    # available algorithms
    algos = {'BFBAB':BF, 'BFBAB3D':BF3D, 'DEE':DEE, 'FF':FF, 'HC':HC, \
            'HC3D':HC3D, 'MONTE':MONTE, 'MONTE3D':M3D, 'SIMANN':SA, \
            'SIMANN3D':SA3D,'SIMANN+':SAPLUS, 'SIMANN3D+':SAPLUS3D, \
            'TREE':TREE, 'GENETIC':GENETIC} 

    print("Available algorithms:")
    for key in algos:
        print(f"{key} - ", end ="")

    # get algorithm for folding
    algo = input("\n" + "Enter algorithm to run: ").upper()

    # check if algorithm name exists
    if algo not in algos:
        sys.exit("Algorithm not found. Please try again.")
    
    # read available proteins from text file
    proteins = {}
    filename = "proteins.txt"

    with open(filename, "r") as file:
        lines = file.readlines()

        print("Available proteins: ")
        # save protein string in a dictionary to choose from
        for i in range(len(lines)):
            protein = lines[i].strip("\n")             
            proteins[i] = protein
            print(f"ID: {i}, Protein: {protein}")
    
    # get protein to fold
    choose_protein = input("\n" + "Which protein would you like to fold? Enter ID: ")
 
    # check if id input valid
    try:
        fold_protein = proteins[int(choose_protein)]
    except ValueError:
        sys.exit("Invalid input. Restart program.")

    length = len(fold_protein)
    proti = Protein(fold_protein, length)    

    # run choosen algorithm
    algos[algo].run(proti)


if __name__ == "__main__":
    main()