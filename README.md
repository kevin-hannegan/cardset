# cardset
This repository enables users to spider solitare from the command line, and allows automation of gameply. Directions for how to play spider solitare can be found here: https://en.wikipedia.org/wiki/Spider_(solitaire).

The repository consists of three working files:
1. carset.py: contains objects (e.g., card, deck) and methods (e.g., suffle) require for base of gameplay
2. spidergame.py: This is a command line game of spider.  just "python spidergame.py" to play!
3. spiderplayer.py:  This routine plugs into the spidergame and automates moves.  For a given delt game, it recursively walks from all possible games and identifies winning move sequences.  It currently has a couple bugs that I will return to later.

Next steps:

 - Rather than dumping recorded move sequences into a logfile, these data should be moved to a database for study.
 - Identify stratgies to win games on first try ( as a human would want).  With a database, analysis of winning moves sequences and higher probably strategies should be identifiable. 

I would be really curious about others' potential improvements!
