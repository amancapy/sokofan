import numpy as np
from copy import deepcopy as dc


# converts the @$# state to a numpy array
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
            for char in row]
           for row in arr]
    return np.array(arr, dtype=np.uint8)


# get player coords
def pij(startstate):
    return np.where((startstate == 1) | (startstate == 2))


# reading the #@$ file to numpyify it
file = "newxsbs2/5.xsb"
startstate = open(file).read().split("\n\n")
lname = file.split("/")[0] + "/" + startstate[0].split("; ")[1]
startstate = startstate[1].split("\n")
startstate = [list(row) for row in startstate if row]
startstate = inter(startstate)


# solution string udlrUDLR
path = open("path5.txt").read().split()[0]


visualize = True  # you will need pygame installed for this. if set false will simply print each step along the path.
valid = True

route = []
for move in path:
    ch, cw = startstate.shape
    pi, pj = pij(startstate)

    if move.lower() == "u":
        nb1, nb2 = (pi-1, pj), (pi-2, pj)
    elif move.lower() == "d":
        nb1, nb2 = (pi+1, pj), (pi+2, pj)
    elif move.lower() == "l":
        nb1, nb2 = (pi, pj-1), (pi, pj-2)
    else:  # neighbour and next-over neighbour in move direction
        nb1, nb2 = (pi, pj+1), (pi, pj+2)

    i1, j1 = nb1
    i2, j2 = nb2
    cstate = dc(startstate)
    if 0 <= i1 < ch and 0 <= j1 < cw:
        if startstate[i1, j1] in (0, 5):
            cstate[pi, pj] = 0 if startstate[pi, pj] == 1 else 5
            cstate[i1, j1] = 1 if startstate[i1, j1] == 0 else 2
        elif startstate[i1, j1] in (4, 6):
            if 0 <= i2 < ch and 0 <= j2 < cw:
                if startstate[i2, j2] in (0, 5):
                    cstate[pi, pj] = 0 if startstate[pi, pj] == 1 else 5
                    cstate[i1, j1] = 1 if startstate[i1, j1] == 4 else 2
                    cstate[i2, j2] = 4 if startstate[i2, j2] == 0 else 6
        else:
            print(startstate)
            print(f"impossible turn {move}. Exiting.")
            valid = False
            break
        startstate = cstate
        if not visualize:
            print(startstate)
        route.append(startstate)


if visualize and valid:
    import pygame

    w = len(startstate[0])
    h = len(startstate)

    csize = 32
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode(((w + 1) * csize, (h + 1) * csize))
    pygame.display.set_caption(lname)

    # pygame resources
    font = pygame.font.SysFont("Courier", 20, bold=True)

    player = pygame.image.load("../resources/robot_on_ground.png").convert()
    player_on_target = pygame.image.load("../resources/robot_on_target.png").convert()
    wall = pygame.image.load("../resources/wall.png").convert()
    box = pygame.image.load("../resources/box.png").convert()
    empty_target = pygame.image.load("../resources/empty_target.png").convert()
    full_target = pygame.image.load("../resources/full_target.png").convert()
    full_ground = pygame.image.load("../resources/full_ground.png").convert()
    icon = pygame.transform.scale(pygame.image.load("../resources/icon.png").convert(), (csize, csize))


    print(len(route))
    while 1:
        for state in route:
            pygame.event.pump()

            screen.fill((155, 173, 183))
            screen.blit(full_ground, (0, 0))

            for i in range(1, w + 1):
                letter = font.render(chr(i + 64), True, (0, 0, 0))
                rect = pygame.Rect(i * csize, 0, csize, csize)
                pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
                screen.blit(letter, (i * csize + 10, 4))
            for j in range(1, h + 1):
                letter = font.render(chr(j + 96), True, (0, 0, 0))
                rect = pygame.Rect(0, j * csize, csize, csize)
                pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
                screen.blit(letter, (10, j * csize + 4))

            screen.blit(icon, (0, 0))

            pi, pj = 0, 0
            for i in range(w):
                for j in range(h):
                    ci = (i + 1) * csize
                    cj = (j + 1) * csize
                    cell = state[j][i]
                    if cell == 1:
                        pi, pj = i, j
                        screen.blit(player, (ci, cj))
                    elif cell == 2:
                        pi, pj = i, j
                        screen.blit(player_on_target, (ci, cj))
                    elif cell == 3:
                        screen.blit(wall, (ci, cj))
                    elif cell == 4:
                        screen.blit(box, (ci, cj))
                    elif cell == 5:
                        screen.blit(empty_target, (ci, cj))
                    elif cell == 6:
                        screen.blit(full_target, (ci, cj))
            pygame.time.delay(100)
            pygame.display.update()

