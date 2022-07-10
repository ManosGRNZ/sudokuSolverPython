#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sudoku Solver Assistance Methods

Created on Sat July 02 2022, 11:00am

@author: Manos Bairaktaris - bairaktaris@gmail.com

License: GNU General Public License v.3 or later (https://www.gnu.org/licenses/gpl-3.0.html)
"""

from pprint import pprint
from copy import deepcopy

def getRow(a : list ,r : int) -> list:
    row = []
    for i in range(len(a)):
        row.append(a[r][i])
    return row

def getColumn(a : list ,c : int) -> list:
    column = []
    for i in range(len(a[c])):
        column.append(a[i][c])
    return column

def get3x3(a : list ,x : int ,y : int) -> list:
    array3x3 = []
    for i in range(3):
        array3x3.append(getRow(a,y*3+i)[(x*3):(x*3+3)])
    return array3x3

def convert_2D_list_to_1D(list2D : list) -> list:
    list1D = [i for row in list2D for i in row ]
    return list1D



def check_cell(s : list, x : int, y : int) -> bool:
    n = s[x][y]
    check = n>0 # True if there is a number (i.e. not 0)
    
    if getRow(s,x).count(n)>1 or getColumn(s,y).count(n)>1 or convert_2D_list_to_1D(get3x3(s,y//3,x//3)).count(n)>1:
        check = False
    return check


def check_Sudoku(s : list) -> bool:
    for x in range(9):
        for y in range(9):
            if not(check_cell(s, x, y)):
                   return False
    return True


def num_of_missing_cells(s : list) -> int:
    missing = 0
    for x in range(9):
        for y in range(9):
            if s[x][y]==0:
                missing += 1
    return missing


def getXYpointer(x,y):
    return x+y*9

def proceed_ForW(x,y):
    xr = x+1
    yr = y
    if xr>8:
        xr = 0
        yr += 1
    #if yr>8:
        #raise Exception("No solution. y>8")
    return xr,yr

def proceed_BackW(x,y):
    xr = x-1
    yr = y
    if xr<0:
        xr = 8
        yr -= 1
    #if yr<0:
        #raise Exception("No solution. y<0")
    return xr,yr
