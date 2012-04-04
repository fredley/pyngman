"""

hangman.py - plays hangman, used for testing pyngman
By Tom Medley - 2012 - http://www.tommedley.com

Picks a word from dictionaries generated by pyngman, and plays a game of hangman
with it.

This code is released under the GNU GPL-3.0:
http://www.opensource.org/licenses/GPL-3.0

"""

import random, sys, os

dictLocation = './pyngman_temp'
minLength = 3
startLives = 10

def init(length = 0,word='',minimal=False):
    if word != '':
        length = len(word)
    else:
        #sort out length
        if length == 0:
            #find max length
            maxLength = minLength
            for i in range(minLength,50):
                if os.path.exists(dictLocation + '/wordlist'+str(i)+'.txt'):
                    maxLength = i
            #pick a length
            while True:
                length = random.randint(minLength,maxLength)
                if os.path.exists(dictLocation + '/wordlist'+str(length)+'.txt'):
                    break
        #get a word from pyngman wordlist
        fileLocation = dictLocation + '/wordlist'+str(length)+'.txt'
        try:
            wordListFile = open(fileLocation,'r')
        except IOError as e:
            return "Wordlist not found for length "+str(length)
        wordCount = file_len(fileLocation)
        wordIndex = random.randint(0,wordCount)
        i = 0
        for line in wordListFile:
            if i == wordIndex:
                word = line.strip()
                break
            i = i+1
    #create temp game file to store word, state, liveshttp://www.reddit.com/r/pics/comments/ro3xb/after_the_removal_of_a_coat_of_dark_varnish_and/
    stateFile = open(dictLocation + '/hangman_state.txt','w')
    stateFile.write(word+':'+'.'*length+':'+str(startLives))
    if minimal:
        return '.'*length
    else:
        return "New game: "+'.'*length+" You have "+str(startLives)+" lives"
    
def guess(char,minimal=False):
    #load state
    stateFile = open(dictLocation + '/hangman_state.txt','r')
    state = stateFile.readline()
    stateFile.close()
    (word,_,state) = state.partition(':')
    (state,_,lives) = state.partition(':')
    lives = int(lives)
    #apply guess
    correct = False
    #save state
    stateFile = open(dictLocation + '/hangman_state.txt','w')
    stateFile.write(word+':'+state+':'+str(lives - 1))
    if len(char) > 1:
        #whole word guess
        if word == char:
            #correct
            if minimal:
                return "win"
            else:
                return "You win, the word is: "+word
        else:
            #incorrect guess
            if minimal:
                return state
            else:
                return "Incorrect guess, you lose a life"
    if char in word and char not in state:
        correct = True
        newState = ''
        for i in range(0,len(word)):
            if word[i] == char:
                newState = newState + char
            else:
                newState = newState + state[i]
        state = newState
        if '.' not in state:
            #all letters found, win
            if minimal:
                return "win"
            else:
                return "You win, the word is: "+word
    else: 
        lives = lives - 1
    if lives == 0:
        if minimal:
            return "lose"
        else:
            return "You lose! The word was: "+word
    #save state
    stateFile = open(dictLocation + '/hangman_state.txt','w')
    stateFile.write(word+':'+state+':'+str(lives))
    #print new state
    if minimal:
        return state
    else:
        if minimal:
            return state
        elif correct:
            return "Correct letter! State is now: "+state+" and you have "+str(lives)+" lives"
        else:
            return "Incorrect, you lose a life. State is: "+state+" and you have "+str(lives)+" lives"
    
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def usage(reason=''):
    """ Print a usage statement """
    if reason != "":
        print reason
        print
    print "usage:"
    print
    print "  hangman -init [-m] [<word> | <length>]"
    print "    Initialize a game. If length is supplied then a word of the"
    print "    appropriate length is chosen. If word is supplied, that word is used."
    print "    If -m is supplied, minimal output will be returned"
    print
    print "  hangman -guess [-m] <character> | <word>"
    print "    Make a guess. If input is more than 1 character long it is counted"
    print "    as a whole word guess. If -m is supplied, minimal output will be returned."
    
#main
if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 2:
        usage("Please specify an operation:")
    elif sys.argv[1] == '-init':
        if argc == 4 and sys.argv[2] == '-m':
            if sys.argv[3].isalpha():
                print init(0,sys.argv[3],True)
            elif sys.argv[3].isdigit():
                print init(int(sys.argv[3]),'',True)
            else:
                usage()
        if argc == 3:
            if sys.argv[2] == '-m':
                print init(0,'',True)
            elif sys.argv[2].isalpha():
                print init(0,sys.argv[2])
            elif sys.argv[2].isdigit():
                print init(int(sys.argv[2]))
            else:
                usage("Invalid arguments supplied")
        elif argc == 2:
            print init()
        else:
            usage("Invalid arguments supplied:")
    elif sys.argv[1] == '-guess' and argc == 3:
        print guess(sys.argv[2])
    elif sys.argv[1] == '-guess' and sys.argv[2] == '-m' and argc == 4:
        print guess(sys.argv[3],True)
    else:
        usage("Invalid arguments supplied:")

        
class Hangman:
    """ Hangman class for easy testing """
    word=''
    lives=0
    state=''
    def init(self,gameWord):
        global startLives
        self.word = gameWord
        self.lives = startLives
        self.state = '.'*len(gameWord)
        return self.state
    def guess(self,char):
        if self.lives == 0: return "gameover"
        if len(char) > 1 and char == self.word: return "win"
        elif len(char) > 1: return self.miss()
        if char in self.state: return self.miss()
        if char in self.word:
            i = 0
            newState = ''
            for letter in self.word:
                if self.word[i] == char:
                    newState = newState + char
                else:
                    newState = newState + self.state[i]
                i = i + 1
            self.state = newState
            if '.' not in self.state: return "win"
            else: return self.state
        else:
            return self.miss()
    def miss(self):
        self.lives = self.lives - 1
        if self.lives == 0: return "lose"
        else: return self.state