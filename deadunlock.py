def gridSearch2(g, p):
    g_sze = len(g)
    p_sze = len(p)
    candidates = []
    for r in range(g_sze - p_sze + 1):
        idx = 0
        while idx < g_sze - p_sze:
            ptr = g[r].find(p[0], idx)
            if ptr < 0:
                break
            candidates.append((r, ptr+idx))
            idx = idx + ptr + 1
        while len(candidates) > 0:
            r, idx = candidates.pop(0)
            rslt = True
            for pr in range(1, p_sze):
                if g[r + pr].find(p[pr], idx) != idx:
                    rslt = False
                    break
            if rslt:
                return True
    return False


def rotated(array_2d):
    list_of_tuples = zip(*array_2d[::-1])
    return [list(elem) for elem in list_of_tuples]


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
    return arr


DLs = [["**", "*$"], ["*$", "*$"], ["$$", "*$"], ["*$", "$*"],
       ["##", "#$"], ["#$", "#$"], ["$$", "#$"], ["$$", "$$"], ["#$", "$#"], [" #", "#$"],
       ["## ", "# #", " $#"], ["## ", "# #", " $$"], ["## ", "# $", " $#"], ["## ", "# $", " $$"],
       ["#$ ", "# $", " $$"], ["$# ", "# $", " $$"], ["$$ ", "# $", " $$"], ["#$ ", "$ $", " $$"], ["$$ ", "$ $", " $$"],
       [" # ", "# #", "#$#"], [" # ", "# #", "#$$"], [" # ", "# $", "#$#"], [" # ", "# $", "#$$"], [" # ", "# #", "$$$"],
       [" # ", "# $", "$$$"], [" $#", "#$ ", "   "], [" # ", "$ $", "$$$"]]

allDLs = []

for dl in DLs:
    ors = [dl]
    for _ in range(3):
        ors.append(["".join(r) for r in rotated(ors[-1])])
    for or_ in ors:
        if or_ not in allDLs:
            allDLs.append((inter(or_)))


print(allDLs)