# sokofan
**Artificial Intelligence CSD311 project to make a sokoban solver**

A* with tree pruning using a decently sized deadlock database. The more complicated prunes such as corrals are beyond the scope of a single dude carrying a semester group project.

18/11 massive change/total redo: children generator complete and so much neater, translated whole project into the numpy environment to make use of sliding windows etc. etc., much more solid checks for deadlock as a result, using numba to leverage the numpy shift, child generator down to ~0.003s per call. node visiting rate itself stands to be seen. heuristics yet to be defined. project more or less unrecognizable since the first commits.

27/11: simple heuristic, passable solve times on smaller levels. the bottleneck is the heap operations themselves unfortunately.
