import pyngman, sys, os
from HangmanClass import Hangman

dictLocation = './pyngman_temp'
minLength = 3
hm = Hangman()

def testWord(word, debug=False):
    nextState = hm.init(word)
    if debug: print "Initial State: "+nextState
    tries = 0
    triedLetters = ''
    while(True):
        nextGuess = pyngman.state(nextState,triedLetters,True)
        triedLetters = triedLetters + nextGuess
        if nextGuess == 'pyngman-fail':
            print 'Pyngman word error, word probably not in dictionary'
            return (False,tries)
        if debug: print "Pyngman guess: "+nextGuess
        nextState = hm.guess(nextGuess)
        if debug: print "Result: "+nextState
        tries = tries + 1
        if nextState == "win":
            return (True,tries)
        elif nextState == "lose":
            return (False,tries)
            
def testDictionary(debug=False):
    #open dictionary, test every word
    won = 0
    lost = 0
    words = 0
    for i in range (minLength,30):
        if os.path.exists(dictLocation + '/wordlist'+str(i)+'.txt'):
            print "Testing words of length",i
            wordListFile = open(dictLocation + '/wordlist'+str(i)+'.txt','r')
            for line in wordListFile:
                (result,_) = testWord(line.strip(),debug)
                if result: won = won + 1
                else: 
                    lost = lost + 1
                    print line.strip()
                words = words + 1
    print words,"words tried, Won:",won,"Lost:",lost
            
if __name__ == "__main__":
    debug = False
    argc = len(sys.argv)
    if argc >= 2 and sys.argv[1] == '-d':
        print "Debugging on"
        debug = True
    if argc == 2 and debug: testDictionary(True)
    if argc == 1: testDictionary()
    if argc == 2 and not debug: testWord(argv[1],debug)
    if argc == 3 and debug: testWord(argv[2],debug)
    
