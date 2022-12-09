# sokofan
**Artificial Intelligence CSD311 project to make a sokoban solver**

![sokogif](https://user-images.githubusercontent.com/111729660/204851864-7b40b1f4-6470-489c-89e6-76e887693169.gif)

A* with tree pruning using a decently sized deadlock database. The more complicated prunes such as corrals are beyond the scope of a single dude carrying a semester group project. The textures too I have designed myself ❤️

18/11 massive change/total redo: children generator complete and so much neater, translated whole project into the numpy environment to make use of sliding windows etc. etc., much more solid checks for deadlock as a result, using numba to leverage the numpy shift, child generator down to ~0.003s per call. node visiting rate itself stands to be seen. heuristics yet to be defined. project more or less unrecognizable since the first commits.

27/11: simple heuristic, passable solve times on smaller levels. the bottleneck is the heap operations themselves unfortunately.

Room for improvement: the deadlock database comparer could treat 0 (empty) space as -1 (any), indicating that even if the empty cell were any other cell, the submatrix is still a deadlock. this would up the probability of detecting deadlocks significantly. Additionally I don't believe my wallock check is *correct* in that I wouldn't bet my money on it even though it has served well on all test cases. I had to throw it together on a weekend evening because the group project ended up being just me doing all of it.
