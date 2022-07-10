#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sudoku Solver

Created on Thu Jan 20 21:39:26 2022

@author: Manos Bairaktaris - bairaktaris@gmail.com

License: GNU General Public License v.3 or later (https://www.gnu.org/licenses/gpl-3.0.html)
"""

from pprint import pprint
from copy import deepcopy
from time import time
from os import system

from sudoku_assistance_methods import *
from sample_sudoku_lists import *


def set_of_possible_solutions(s : list) -> list:
    ap = deepcopy(s)
    ap_copy = deepcopy(s)
    allNums = set(range(1,10,1))

    for x in range(9):
        for y in range(9):
            if ap_copy[x][y]==0:
                x3 = x // 3
                y3 = y // 3
                remainingNums = allNums - set(getRow(ap_copy,x)) - set(getColumn(ap_copy, y)) - set(convert_2D_list_to_1D(get3x3(ap_copy,y3,x3))) 
                if len(remainingNums)==0:
                    print("\n printing before ending: \n")
                    pprint(ap_copy)
                    pprint(getRow(ap_copy,x))
                    pprint(getColumn(ap_copy,y))
                    pprint(convert_2D_list_to_1D(get3x3(ap_copy,y3,x3)))
                    raise Exception(f"No solution found. \n x = {x} \t y = {y}")
                else: 
                    ap[x][y] = list(remainingNums)
            else:
                ap[x][y] = [ s[x][y] ]
    return ap


def open_cells(sps : list) -> list:
    """Get a list from set_of_possible_solutions (sps) 
    and provides a list of lists with the following
    format: [x,y,num_of_solutions]"""
    result = []
    for x in range(9):
        for y in range(9):
            if sps[x][y] is list:
                result.append([x,y,len(sps[x][y])],0) # the last "0" is considered as the initial first value to be tried
    return result                


def solveSrl(sudoku):
    sud = deepcopy(sudoku)
    origin = deepcopy(sudoku)

    proceed = True # By default proceed forward
    
    sp = set_of_possible_solutions(sudoku)
    print("Possible solutions found.")
    
    print("\n Sp = ")
    pprint(sp)
    print("\n  \n")
    print("sud = ")
    pprint(sud)
    print("\n  \n")
    
    x = y = 0
    choice = [[-1 for i in range(9)] for j in range(9)]
        
    #set values where there is only one possible solution
    for x in range(9):
        for y in range(9):
            choice[x][y] = -1
            if len(sp[x][y])==1:
                origin[x][y] = sud[x][y] = sp[x][y][0]                
    if check_Sudoku(sud):
        print("Solved before starting")
        return sud
                
    print("After setting values \n sud = ")
    pprint(sud)
    print("\n  \n")
    
    if check_Sudoku(sud):
        print("Solved only with cross check")
        return sud
     
    # current cell to work with
    i = x = y = 0
    maxXY = minXY = 0

    print("\n origin:")
    pprint(origin)
    print("\n choice")
    pprint(choice)    

    #system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
    print()

    while not(check_Sudoku(sud)) and not(y>=9 and proceed) and not(y<0 and proceed==False):
        i += 1

        if origin[x][y]!=0:
            print(f"\n i = {i} \t x = {x} \t y = {y}", end="\t")
            print(f"choice = {choice[x][y]} of {len(sp[x][y])-1}", end="\t")
            print(f"minXY = {minXY} \t maxXY = {maxXY} \t Origin>0 Continue")
            #sud[x][y] = origin[x][y]
            x,y = proceed_ForW(x,y) if proceed else proceed_BackW(x,y)
            continue
        
        # This has no effect and is for monitoring and debugging only.
        if maxXY<getXYpointer(x,y):
            minXY = maxXY = getXYpointer(x,y)
        else:
            minXY = min( minXY, getXYpointer(x,y) )
            
        print(f"\n i = {i} \t x = {x} \t y = {y}", end="\t")
        print(f"choice = {choice[x][y]} of {len(sp[x][y])-1} \t",
              f"minXY = {minXY} \t maxXY = {maxXY}", end="   ")

        choice[x][y] += 1
        #if this cell has checked all choices, reset it and continue Backwards this time
        if choice[x][y]>=len(sp[x][y]):
            print("choice>len(sp)")
            choice[x][y]=-1
            sud[x][y] = origin[x][y]
            proceed = False
            x,y = proceed_BackW(x,y)
            continue

        # If everything else is normal, i.e. sud[x][x]==0
        sud[x][y] = sp[x][y][ choice[x][y] ]
        print("sud[x][y] & origin==0", end="   ")
        
        if check_cell(sud,x,y):
            # Proceed forward
            proceed = True
            x,y = proceed_ForW(x,y)
            print("cell=True & FW")
        else:
            # stay in the same cell
            print(f"cell=False & stay")
            """if choice[x][y]>=len(sp[x][y]):
                choice[x][y]=-1
                sud[x][y]=0
                x,y = proceed_BackW(x,y)
                print("move BW")"""

    if (not check_Sudoku(sud)):
        sud.append("Process FAILED. No solution.")
        ret = sud, origin, choice, sp
    else:
        ret = sud
            
    return ret
        

# run it!
startTime = time()

pprint(solveSrl(sampleSudoku2))

totTime = time() - startTime
print(f" \n Time = {totTime:1.2f}")
#print(f"i = {i} \t x = {x} \t y = {y} \n")
