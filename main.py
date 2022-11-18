import time
from copy import deepcopy as dc
import random
import os
import numpy as np
from time import perf_counter as ptime
from heapq import heappop as hpop, heappush as hpsh, heapify as hpfy


# turns string input to integers for numpy
def inter(arr):
    arr = [list(row) for row in arr]
    arr = [[int(char
                .replace(" ", "0")
                .replace("@", "1")
                .replace("+", "2")
                .replace("#", "3")
                .replace("$", "4")
                .replace(".", "5")
                .replace("*", "6"))
            for char in row] for row in arr]
    return np.array(arr, dtype=np.uint8)


# checking if the given state has been fully sorted, by checking if there aren't any unplaced boxes (4) left
def solved(sstate):
    return not np.isin(4, sstate)


pick = f"xsbs/{random.randint(1, 15)}/{random.randint(1, 100)}.xsb"
while not os.path.exists(pick):
    pick = f"xsbs/{random.randint(1, 15)}/{random.randint(1, 100)}.xsb"
startstate = open(pick).read().split("\n\n")
lname = pick.split("/")[0] + "/" + startstate[0].split("; ")[1]
startstate = startstate[1].split("\n")
startstate = [list(row) for row in startstate if row]
startstate = inter(startstate)

# we have a list of all 2x2 and 3x3 deadlocks, but it is inefficient to check for each of them for each child.
# so we only check the ones that *can* occur in our level by comparing wall structure. waller() strips the level
# and the deadlocks of everything but walls, and sees if they can occur in the level.
def waller(m):
    mcopy = np.copy(m)
    for celltype in (1, 2, 4, 5, 6):
        mcopy[mcopy == celltype] = 0
    return mcopy


# checks if smat is in mat. this is to check if there is a deadlock in our state
def submatrix(mat, smat):
    return bool((np.lib.stride_tricks.sliding_window_view(mat, smat.shape).reshape(-1, *smat.shape) == smat)
                .all(axis=(1, 2)).any())

# filtering the deadlocks
allDLs = [[[6, 6], [6, 4]], [[6, 6], [4, 6]], [[4, 6], [6, 6]], [[6, 4], [6, 6]], [[6, 4], [6, 4]], [[6, 6], [4, 4]],
          [[4, 6], [4, 6]], [[4, 4], [6, 6]], [[4, 4], [6, 4]], [[6, 4], [4, 4]], [[4, 6], [4, 4]], [[4, 4], [4, 6]],
          [[6, 4], [4, 6]], [[4, 6], [6, 4]], [[6, 4], [4, 6]], [[4, 6], [6, 4]], [[3, 3], [3, 4]], [[3, 3], [4, 3]],
          [[4, 3], [3, 3]], [[3, 4], [3, 3]], [[3, 4], [3, 4]], [[3, 3], [4, 4]], [[4, 3], [4, 3]], [[4, 4], [3, 3]],
          [[4, 4], [3, 4]], [[3, 4], [4, 4]], [[4, 3], [4, 4]], [[4, 4], [4, 3]], [[4, 4], [4, 4]], [[4, 4], [4, 4]],
          [[4, 4], [4, 4]], [[4, 4], [4, 4]], [[3, 4], [4, 3]], [[4, 3], [3, 4]], [[3, 4], [4, 3]], [[4, 3], [3, 4]],
          [[3, 3, 0], [3, 0, 3], [0, 4, 3]], [[0, 3, 3], [4, 0, 3], [3, 3, 0]], [[3, 4, 0], [3, 0, 3], [0, 3, 3]],
          [[0, 3, 3], [3, 0, 4], [3, 3, 0]], [[3, 3, 0], [3, 0, 3], [0, 4, 4]], [[0, 3, 3], [4, 0, 3], [4, 3, 0]],
          [[4, 4, 0], [3, 0, 3], [0, 3, 3]], [[0, 3, 4], [3, 0, 4], [3, 3, 0]], [[3, 3, 0], [3, 0, 4], [0, 4, 3]],
          [[0, 3, 3], [4, 0, 3], [3, 4, 0]], [[3, 4, 0], [4, 0, 3], [0, 3, 3]], [[0, 4, 3], [3, 0, 4], [3, 3, 0]],
          [[3, 3, 0], [3, 0, 4], [0, 4, 4]], [[0, 3, 3], [4, 0, 3], [4, 4, 0]], [[4, 4, 0], [4, 0, 3], [0, 3, 3]],
          [[0, 4, 4], [3, 0, 4], [3, 3, 0]], [[3, 4, 0], [3, 0, 4], [0, 4, 4]], [[0, 3, 3], [4, 0, 4], [4, 4, 0]],
          [[4, 4, 0], [4, 0, 3], [0, 4, 3]], [[0, 4, 4], [4, 0, 4], [3, 3, 0]], [[4, 3, 0], [3, 0, 4], [0, 4, 4]],
          [[0, 3, 4], [4, 0, 3], [4, 4, 0]], [[4, 4, 0], [4, 0, 3], [0, 3, 4]], [[0, 4, 4], [3, 0, 4], [4, 3, 0]],
          [[4, 4, 0], [3, 0, 4], [0, 4, 4]], [[0, 3, 4], [4, 0, 4], [4, 4, 0]], [[4, 4, 0], [4, 0, 3], [0, 4, 4]],
          [[0, 4, 4], [4, 0, 4], [4, 3, 0]], [[3, 4, 0], [4, 0, 4], [0, 4, 4]], [[0, 4, 3], [4, 0, 4], [4, 4, 0]],
          [[4, 4, 0], [4, 0, 4], [0, 4, 3]], [[0, 4, 4], [4, 0, 4], [3, 4, 0]], [[4, 4, 0], [4, 0, 4], [0, 4, 4]],
          [[0, 4, 4], [4, 0, 4], [4, 4, 0]], [[4, 4, 0], [4, 0, 4], [0, 4, 4]], [[0, 4, 4], [4, 0, 4], [4, 4, 0]],
          [[0, 3, 0], [3, 0, 3], [3, 4, 3]], [[3, 3, 0], [4, 0, 3], [3, 3, 0]], [[3, 4, 3], [3, 0, 3], [0, 3, 0]],
          [[0, 3, 3], [3, 0, 4], [0, 3, 3]], [[0, 3, 0], [3, 0, 3], [3, 4, 4]], [[3, 3, 0], [4, 0, 3], [4, 3, 0]],
          [[4, 4, 3], [3, 0, 3], [0, 3, 0]], [[0, 3, 4], [3, 0, 4], [0, 3, 3]], [[0, 3, 0], [3, 0, 4], [3, 4, 3]],
          [[3, 3, 0], [4, 0, 3], [3, 4, 0]], [[3, 4, 3], [4, 0, 3], [0, 3, 0]], [[0, 4, 3], [3, 0, 4], [0, 3, 3]],
          [[0, 3, 0], [3, 0, 4], [3, 4, 4]], [[3, 3, 0], [4, 0, 3], [4, 4, 0]], [[4, 4, 3], [4, 0, 3], [0, 3, 0]],
          [[0, 4, 4], [3, 0, 4], [0, 3, 3]], [[0, 3, 0], [3, 0, 3], [4, 4, 4]], [[4, 3, 0], [4, 0, 3], [4, 3, 0]],
          [[4, 4, 4], [3, 0, 3], [0, 3, 0]], [[0, 3, 4], [3, 0, 4], [0, 3, 4]], [[0, 3, 0], [3, 0, 4], [4, 4, 4]],
          [[4, 3, 0], [4, 0, 3], [4, 4, 0]], [[4, 4, 4], [4, 0, 3], [0, 3, 0]], [[0, 4, 4], [3, 0, 4], [0, 3, 4]],
          [[0, 4, 3], [3, 4, 0], [0, 0, 0]], [[0, 3, 0], [0, 4, 4], [0, 0, 3]], [[0, 0, 0], [0, 4, 3], [3, 4, 0]],
          [[3, 0, 0], [4, 4, 0], [0, 3, 0]], [[0, 3, 0], [4, 0, 4], [4, 4, 4]], [[4, 4, 0], [4, 0, 3], [4, 4, 0]],
          [[4, 4, 4], [4, 0, 4], [0, 3, 0]], [[0, 4, 4], [3, 0, 4], [0, 4, 4]]]
filteredDLs = []
for dl in allDLs:
    if submatrix(waller(startstate), waller(dl)):
        filteredDLs.append(dl)


# checks for possible deadlocks
def deadlock(dlstate):
    for dl in filteredDLs:
        if submatrix(dlstate, np.array(dl, dtype=np.uint8)):
            return True
    return False


# get player's index
def pij(pstate):
    return np.where((pstate == 1) | (pstate == 2))


# current state's *push* children. tentative: can try backward search with *pull* children as well
def pushChildren(pstate):
    pi, pj = pij(pstate)
    ch, cw = pstate.shape
    childs = []
    for nb1, nb2 in (((pi - 1, pj), (pi - 2, pj)), ((pi + 1, pj), (pi + 2, pj)), ((pi, pj - 1), (pi, pj - 2)),
                     ((pi, pj + 1), (pi, pj + 2))):
        i1, j1 = nb1
        i2, j2 = nb2

        if 0 <= i1 < ch and 0 <= j1 < cw:
            if pstate[i1, j1] in (0, 5):
                cstate = dc(pstate)
                cstate[pi, pj] = 0 if pstate[pi, pj] == 1 else 5
                cstate[i1, j1] = 1 if pstate[i1, j1] == 0 else 2
                if not deadlock(cstate):
                    childs.append(cstate)
            elif pstate[i1, j1] in (4, 6):
                if 0 <= i2 < ch and 0 <= j2 < cw:
                    if pstate[i2, j2] in (0, 5):
                        cstate = dc(pstate)
                        cstate[pi, pj] = 0 if pstate[pi, pj] == 1 else 5
                        cstate[i1, j1] = 1 if pstate[i1, j1] == 4 else 2
                        cstate[i2, j2] = 4 if pstate[i2, j2] == 0 else 6
                        if not deadlock(cstate):
                            childs.append(cstate)
    return dc(childs)


childs = pushChildren(startstate)
for row in startstate:
    print(row)
print()
print()

for child in childs:
    for row in child:
        ...
        print(row)
    print()
print(len(childs))


def pullChildren(pstate):
    ...  # tentative
