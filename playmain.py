import pygame

# read and save .xsb as 2d list
chosen = "1/1"
level = open(f"xsbs/{chosen}.xsb").read().split("\n\n")
lname = chosen.split("/")[0] + "/" + level[0].split("; ")[1]
level = [list(thing) for thing in level[1].split("\n")]
w = len(level[0])
h = len(level)

# init pygame
csize = 32
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(((w + 1) * csize, (h+1) * csize))
pygame.display.set_caption(lname)

# pygame resources
font = pygame.font.SysFont("Courier", 20, bold=True)

player = pygame.image.load("resources/robot_on_ground.png").convert()
player_on_target = pygame.image.load("resources/robot_on_target.png").convert()
wall = pygame.image.load("resources/wall.png").convert()
box = pygame.image.load("resources/box.png").convert()
empty_target = pygame.image.load("resources/empty_target.png").convert()
full_target = pygame.image.load("resources/full_target.png").convert()
full_ground = pygame.image.load("resources/full_ground.png").convert()
icon = pygame.transform.scale(pygame.image.load("resources/icon.png").convert(), (csize, csize))

# counting number of targets
wincondition = 0
for line in level:
    for cell in line:
        if cell == "." or cell == "*" or cell == "+":
            wincondition += 1

wins = 0
losses = 0
resets = 0

def level_reset(winbool):
    global losses, wins, resets, moves
    lvl = open(f"xsbs/{chosen}.xsb").read().split("\n\n")
    lvl = [list(thing) for thing in lvl[1].split("\n")]

    if winbool:
        wins += 1
    else:
        losses += 1

    resets = wins + losses
    print(f"wins: {wins}, losses: {losses}, total: {resets}")
    moves = 0
    return lvl

moves = 0
running = True
while 1:
    if not running:
        break
    win = False

    # counting how many boxes have been delivered
    placed = 0
    for line in level:
        for cell in line:
            if cell == "*":
                placed += 1

    # win and end game if all boxes placed
    if placed == wincondition:
        win = True
        level = level_reset(win)

    # lose and reset game if any box is cornered in non-target cell
    for i in range(w):
        for j in range(h-1):
            if level[j][i] == "$":
                if j+1 <= h and level[j+1][i] == "#":
                    if (i+1 <= h and level[j][i+1] == "#") or (i-1 >= 0 and level[j][i-1] == "#"):
                        level = level_reset(False)
                elif j-1 >= 0 and level[j-1][i] == "#":
                    if (i+1 <= h and level[j][i+1] == "#") or (i-1 >= 0 and level[j][i-1] == "#"):
                        level = level_reset(False)

    screen.fill((155, 173, 183))

    # background
    screen.blit(full_ground, (0, 0))

    # naming rows and columns with letters a-z and A-Z
    for i in range(1, w + 1):
        letter = font.render(chr(i + 64), True, (0, 0, 0))
        rect = pygame.Rect(i * csize, 0, csize, csize)
        pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
        screen.blit(letter, (i * csize + 10, 4))
    for j in range(1, h):
        letter = font.render(chr(j + 96), True, (0, 0, 0))
        rect = pygame.Rect(0, j * csize, csize, csize)
        pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
        screen.blit(letter, (10, j * csize + 4))

    # corner icon
    screen.blit(icon, (0, 0))

    # displaying moves, wins, losses
    moves_ = font.render(f"moves: {moves}", True, (0, 0, 0))
    screen.blit(moves_, (8, h*csize+3))

    # going through the 2d list and rendering the ascii characters as their respective textures
    pi, pj = 0, 0
    for i in range(w):
        for j in range(h - 1):
            ci = (i + 1) * csize
            cj = (j + 1) * csize
            cell = level[j][i]
            if cell == "@":
                pi, pj = i, j
                screen.blit(player, (ci, cj))
            elif cell == "+":
                screen.blit(player_on_target, (ci, cj))
                pi, pj = i, j
            elif cell == "#":
                screen.blit(wall, (ci, cj))
            elif cell == "$":
                screen.blit(box, (ci, cj))
            elif cell == ".":
                screen.blit(empty_target, (ci, cj))
            elif cell == "*":
                screen.blit(full_target, (ci, cj))

    # event manager 🤓
    pygame.event.set_allowed([pygame.KEYDOWN])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # reset
            if event.key == pygame.K_r:
                level = level_reset(False)
            # up
            if event.key == pygame.K_UP:
                if pj - 1 >= 0:
                    ucell = level[pj - 1][pi]
                    currc = " " if level[pj][pi] == "@" else "."
                    if ucell == " ":
                        level[pj - 1][pi] = "@"
                        level[pj][pi] = currc
                        moves += 1
                    elif ucell == ".":
                        level[pj - 1][pi] = "+"
                        level[pj][pi] = currc
                        moves += 1
                    elif (ucell == "$" or ucell == "*") and pj - 2 >= 0:
                        if level[pj - 2][pi] == " ":
                            level[pj - 2][pi] = "$"
                            level[pj - 1][pi] = "@" if ucell == "$" else "+"
                            moves += 1
                            level[pj][pi] = currc
                        elif level[pj - 2][pi] == ".":
                            level[pj - 2][pi] = "*"
                            level[pj - 1][pi] = "@" if ucell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
            # down
            elif event.key == pygame.K_DOWN:
                if pj + 1 <= h:
                    dcell = level[pj + 1][pi]
                    currc = " " if level[pj][pi] == "@" else "."
                    if dcell == " ":
                        level[pj + 1][pi] = "@"
                        level[pj][pi] = currc
                        moves += 1
                    elif dcell == ".":
                        level[pj + 1][pi] = "+"
                        level[pj][pi] = currc
                        moves += 1
                    elif (dcell == "$" or dcell == "*") and pj + 2 <= h:
                        if level[pj + 2][pi] == " ":
                            level[pj + 2][pi] = "$"
                            level[pj + 1][pi] = "@" if dcell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
                        elif level[pj + 2][pi] == ".":
                            level[pj + 2][pi] = "*"
                            level[pj + 1][pi] = "@" if dcell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
            # left
            elif event.key == pygame.K_LEFT:
                if pi - 1 >= 0:
                    lcell = level[pj][pi - 1]
                    currc = " " if level[pj][pi] == "@" else "."
                    if lcell == " ":
                        level[pj][pi - 1] = "@"
                        level[pj][pi] = currc
                        moves += 1
                    elif lcell == ".":
                        level[pj][pi - 1] = "+"
                        level[pj][pi] = currc
                        moves += 1
                    elif (lcell == "$" or lcell == "*") and pi - 2 >= 0:
                        if level[pj][pi - 2] == " ":
                            level[pj][pi - 2] = "$"
                            level[pj][pi - 1] = "@" if lcell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
                        elif level[pj][pi - 2] == ".":
                            level[pj][pi - 2] = "*"
                            level[pj][pi - 1] = "@" if lcell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
            # right
            elif event.key == pygame.K_RIGHT:
                if pi + 1 <= w:
                    rcell = level[pj][pi + 1]
                    currc = " " if level[pj][pi] == "@" else "."
                    if rcell == " ":
                        level[pj][pi + 1] = "@"
                        level[pj][pi] = currc
                        moves += 1
                    elif rcell == ".":
                        level[pj][pi + 1] = "+"
                        level[pj][pi] = currc
                        moves += 1
                    elif (rcell == "$" or rcell == "*") and pi + 2 <= w:
                        if level[pj][pi + 2] == " ":
                            level[pj][pi + 2] = "$"
                            level[pj][pi + 1] = "@" if rcell == "$" else "+"
                            level[pj][pi] = currc
                            moves += 1
                        elif level[pj][pi + 2] == ".":
                            level[pj][pi + 2] = "*"
                            level[pj][pi + 1] = "@" if rcell == "$" else "+"
                            level[pj][pi] = currc
                        moves += 1

    pygame.time.Clock().tick(45)
    pygame.display.flip()
