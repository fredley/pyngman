"""

HangmanClass.py - plays hangman, used for testing pyngman
By Tom Medley - 2012 - http://www.tommedley.com

Simple implementation of hangman, for automated testing

This code is released under the GNU GPL-3.0:
http://www.opensource.org/licenses/GPL-3.0

"""
class Hangman:
    startLives=10
    word=''
    lives=startLives
    state=''
    def init(self,gameWord):
        self.word = gameWord
        self.lives = self.startLives
        self.state = '.'*len(gameWord)
        return self.state
    def guess(self,char):
        if lives == 0 return "gameover"
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
        