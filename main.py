import time
from copy import deepcopy as dc
import random
import os
import numpy as np
from heapq import heappop as hpop, heappush as hpsh, heapify as hpfy


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
    return np.array(arr)


def solved(sstate):
    return np.isin(4, sstate)


def waller(m):
    mcopy = np.copy(m)
    for celltype in (1, 2, 4, 5, 6):
        mcopy[mcopy == celltype] = 0
    return mcopy


def submatrix(mat, smat):
    return bool((np.lib.stride_tricks.sliding_window_view(mat, smat.shape).reshape(-1, *smat.shape) == smat)
                .all(axis=(1, 2)).any())


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

pick = f"xsbs/{random.randint(1, 15)}/{random.randint(1, 100)}.xsb"
while not os.path.exists(pick):
    pick = f"xsbs/{random.randint(1, 15)}/{random.randint(1, 100)}.xsb"
startstate = open(pick).read().split("\n\n")
lname = pick.split("/")[0] + "/" + startstate[0].split("; ")[1]
startstate = startstate[1].split("\n")
startstate = [list(row) for row in startstate if row]
startstate = inter(startstate)

filtDLs = []
for dl in allDLs:
    if submatrix(waller(startstate), waller(dl)):
        filtDLs.append(dl)


def deadlock(dlstate):
    for dl in filtDLs:
        if submatrix(dlstate, np.array(dl)):
            return True
    return False


def pij(pstate):
    return np.where((pstate == 1) | (pstate == 2))


print(pij(startstate))
for row in startstate:
    print(row)


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


print(len(pushChildren(startstate)))


# for child in pushChildren(startstate):
#     for row in child:
#         ...
#         print(row)
#         print()
#     print()
#     print()


def pullChildren(pstate):
    pi, pj = pij(pstate)
    ch, cw = len(pstate), len(pstate[0])
    childs = []
