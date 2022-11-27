import numpy as np
import matplotlib.pyplot as plt


def waller(m):
    mcopy = np.copy(m)
    for celltype in (2, 3, 5, 6, 7):
        mcopy[mcopy == celltype] = 1
    return mcopy


state = np.array([[1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1]
               , [1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 1, 1, 1, 1]
               , [1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 1, 1, 1, 1]
               , [1, 1, 1, 1, 1, 1, 4, 4, 4, 1, 6, 4, 4, 4, 1, 1, 1]
               , [1, 1, 1, 1, 1, 4, 4, 6, 5, 6, 5, 1, 1, 4, 4, 1, 1]
               , [1, 1, 1, 1, 4, 4, 6, 5, 6, 5, 7, 1, 1, 1, 4, 4, 4]
               , [1, 1, 1, 4, 4, 6, 5, 6, 5, 7, 1, 1, 7, 5, 1, 4, 4]
               , [1, 1, 4, 4, 6, 5, 6, 5, 7, 1, 1, 7, 5, 6, 5, 6, 4]
               , [4, 4, 4, 6, 5, 6, 5, 7, 1, 1, 7, 5, 6, 5, 6, 4, 4]
               , [4, 4, 6, 5, 6, 5, 7, 1, 1, 7, 5, 6, 5, 6, 4, 4, 4]
               , [4, 6, 5, 6, 5, 7, 1, 1, 7, 5, 6, 5, 6, 4, 4, 1, 1]
               , [4, 4, 1, 5, 7, 1, 1, 7, 5, 6, 5, 6, 4, 4, 1, 1, 1]
               , [4, 4, 4, 1, 1, 1, 7, 5, 6, 5, 6, 4, 4, 1, 1, 1, 1]
               , [1, 1, 4, 4, 2, 1, 5, 6, 5, 6, 4, 4, 1, 1, 1, 1, 1]
               , [1, 1, 1, 4, 4, 4, 6, 1, 4, 4, 4, 1, 1, 1, 1, 1, 1]
               , [1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1]
               , [1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1]
               , [1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]])


plt.imshow(state, "gray", vmin=1, vmax=7)
plt.show()
plt.imshow(waller(state), "gray", vmin=1, vmax=7)
plt.show()

print(waller(state))