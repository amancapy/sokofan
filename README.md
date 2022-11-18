# sokoproject
**Artificial Intelligence CSD311 project to devise an agent that can solve any Sokoban level**


06/09 sokoban fully playable now, haven't implemented loss condition if box cornered yet - capy

07/09 loss condition if box cornered into non-target cell - capy

09/09 no real progress, optimised the pygame bits a bunch and handcrafted the textures to perfection (doesn't help with ai btw) - capy

18/11 big changes: coerced whole project to numpy environment to make use of sliding windows, much more solid checks for deadlock as a result, using numba to leverage the numpy shift, core function down to ~0.003s per call; closer to ideal than not.
