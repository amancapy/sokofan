import pygame

level = open("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/xsbs/1/1.xsb").read().split("\n")
level = [list(thing) for thing in level]
w = len(level[0])
h = len(level)

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(((w + 1) * 26, h * 26))

font = pygame.font.SysFont("Courier", 17, bold=True)
ground = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/bg.png")
player = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/robot.png")
player_on_target = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/robot_on_target.png")
wall = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/wall.png")
box = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/box.png")
empty_target = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/empty_target.png")
full_target = pygame.image.load("C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/full_target.png")

wincondition = 0
for line in level:
    for cell in line:
        if cell == "." or cell == "*" or cell == "+":
            wincondition += 1

running = True
win = False
while running:
    placed = 0
    for line in level:
        for cell in line:
            if cell == "*":
                placed += 1
    if placed == wincondition:
        win = True
        running = False

    screen.fill((155, 173, 183))

    for i in range(1, w + 1):
        letter = font.render(chr(i + 64), True, (0, 0, 0))
        rect = pygame.Rect(i * 26, 0, 26, 26)
        pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
        screen.blit(letter, (i * 26 + 8, 3))
    for j in range(1, h):
        letter = font.render(chr(j + 96), True, (0, 0, 0))
        rect = pygame.Rect(0, j * 26, 26, 26)
        pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
        screen.blit(letter, (8, j * 26 + 3))

    rect = pygame.Rect(0, 0, 26, 26)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    for i in range(w):
        for j in range(h-1):
            ci = (i + 1) * 26
            cj = (j + 1) * 26
            cell = level[j][i]
            if cell == " ":
                screen.blit(ground, (ci, cj))
            elif cell == "@":
                screen.blit(player, (ci, cj))
            elif cell == "+":
                screen.blit(player_on_target, (ci, cj))
            elif cell == "#":
                screen.blit(wall, (ci, cj))
            elif cell == "$":
                screen.blit(box, (ci, cj))
            elif cell == ".":
                screen.blit(empty_target, (ci, cj))
            elif cell == "*":
                screen.blit(full_target, (ci, cj))

    pi, pj = 0, 0
    pfound = False
    while not pfound:
        for i in range(w):
            for j in range(h-1):
                if level[j][i] == "@" or level[j][i] == "+":
                    pi, pj = i, j
                    pfound = True
                    break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #up
            if event.key == pygame.K_UP:
                if pj-1 >= 0:
                    ucell = level[pj - 1][pi]
                    if level[pj][pi] == "@":
                        currc = " "
                    else:
                        currc = "."
                    if ucell == " ":
                        level[pj - 1][pi] = "@"
                        level[pj][pi] = currc
                    elif ucell == ".":
                        level[pj - 1][pi] = "+"
                        level[pj][pi] = currc
                    elif (ucell == "$" or ucell == "*") and pj-2 >= 0:
                        if level[pj-2][pi] == " ":
                            level[pj-2][pi] = "$"
                            level[pj-1][pi] = "@" if ucell == "$" else "+"
                            level[pj][pi] = currc
                        elif level[pj-2][pi] == ".":
                            level[pj-2][pi] = "*"
                            level[pj-1][pi] = "@" if ucell == "$" else "+"
                            level[pj][pi] = currc
            # down
            if event.key == pygame.K_DOWN:
                if pj + 1 <= h:
                    dcell = level[pj + 1][pi]
                    if level[pj][pi] == "@":
                        currc = " "
                    else:
                        currc = "."
                    if dcell == " ":
                        level[pj + 1][pi] = "@"
                        level[pj][pi] = currc
                    elif dcell == ".":
                        level[pj + 1][pi] = "+"
                        level[pj][pi] = currc
                    elif (dcell == "$" or dcell == "*") and pj + 2 <= h:
                        if level[pj + 2][pi] == " ":
                            level[pj + 2][pi] = "$"
                            level[pj + 1][pi] = "@" if dcell == "$" else "+"
                            level[pj][pi] = currc
                        elif level[pj+2][pi] == ".":
                            level[pj+2][pi] = "*"
                            level[pj+1][pi] = "@" if dcell == "$" else "+"
                            level[pj][pi] = currc
            # left
            if event.key == pygame.K_LEFT:
                if pi - 1 >= 0:
                    lcell = level[pj][pi - 1]
                    if level[pj][pi] == "@":
                        currc = " "
                    else:
                        currc = "."
                    if lcell == " ":
                        level[pj][pi-1] = "@"
                        level[pj][pi] = currc
                    elif lcell == ".":
                        level[pj][pi-1] = "+"
                        level[pj][pi] = currc
                    elif (lcell == "$" or lcell == "*") and pi - 2 >= 0:
                        if level[pj][pi-2] == " ":
                            level[pj][pi-2] = "$"
                            level[pj][pi-1] = "@" if lcell == "$" else "+"
                            level[pj][pi] = currc
                        elif level[pj][pi-2] == ".":
                            level[pj][pi-2] = "*"
                            level[pj][pi-1] = "@" if lcell == "$" else "+"
                            level[pj][pi] = currc
            # right
            if event.key == pygame.K_RIGHT:
                if pi + 1 <= w:
                    rcell = level[pj][pi + 1]
                    if level[pj][pi] == "@":
                        currc = " "
                    else:
                        currc = "."
                    if rcell == " ":
                        level[pj][pi+1] = "@"
                        level[pj][pi] = currc
                    elif rcell == ".":
                        level[pj][pi+1] = "+"
                        level[pj][pi] = currc
                    elif (rcell == "$" or rcell == "*") and pi + 2 <= w:
                        if level[pj][pi+2] == " ":
                            level[pj][pi+2] = "$"
                            level[pj][pi+1] = "@" if rcell == "$" else "+"
                            level[pj][pi] = currc
                        elif level[pj][pi+2] == ".":
                            level[pj][pi+2] = "*"
                            level[pj][pi+1] = "@" if rcell == "$" else "+"
                            level[pj][pi] = currc

    pygame.display.flip()

print("you " + ("win" if win else "lose"))