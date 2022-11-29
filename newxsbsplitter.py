import os

read = open("testExamples.xsb").read().split("\n\n")

for lvl in read:
    name, level = lvl.split("\n")[0], lvl.split("\n")[1:]

    maxlen = max([len(row) for row in level])

    for i in range(len(level)):
        level[i] += (maxlen - len(level[i])) * " "

    newfile = open(f"newxsbs2/{name.split(';')[1].split()[-1]}.xsb", "w")
    newfile.writelines("; " + name.split(";")[1] + "\n\n")
    for row in level:
        newfile.writelines(row + "\n")
