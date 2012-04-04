#pyngman
###An optimal hangman-guessing python script, by Tom Medley

##Usage

1. Get a [Dictionary](http://en-gb.pyxidium.co.uk/dictionary/OOo.php)
2. Run `python pyngman.py -init path-to-dict.zip`
3. Run `python pyngman.py -state ..e..y estry`, where ..e..y is the state of the
game, and estry are the letters you've already used. pyngman will tell you what 
your optimal next move is.

##Dictionaries

pyngman is designed to work with a `.zip` dictionary file, such as the ones
available at [Pyxidium](http://en-gb.pyxidium.co.uk/dictionary/OOo.php) for
Open Office. I have tested the script with their en-GB dictionary.

The script will parse the dictionary into a complete list of words, removing 
words deemed 'invalid' for hangman, such as those containing apostrophes or 
dashes.

##Do More

Included is a simple tool for playing Hangman games - `hangman.py`. `hangman.py`
requires pyngman to have been initialized before it works. It can be used with 
`test.py` to run a test against the dictionary to see what pyngman's odds are of
winning. In my testing this has been pretty good, ~500 losses per 80k words, or
a failure rate of 0.000625%. 

##License

pyngman was created by [Tom Medley](http://www.tommedley.com), and is released 
under the GNU GPL v3.0. It comes with no warranty.
