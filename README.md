# sokoproject
**Artificial Intelligence CSD311 project to make a sokoban solver**


06/09 sokoban fully playable now, haven't implemented loss condition if box cornered yet

07/09 loss condition if box cornered into non-target cell

09/09 no real progress, optimised the pygame bits a bunch and handcrafted the textures to perfection (doesn't help with ai btw)

18/11 big changes: translated whole project into the numpy environment to make use of sliding windows, conditional setitem etc. etc., much more solid checks for deadlock as a result, using numba to leverage the numpy shift, core function down to ~0.003s per call. node visiting rate itself stands to be seen. project more or less unrecognizable since the first commits.
