"""

pyngman.py - an optimal hangman playing python script
By Tom Medley - 2012 - http://www.tommedley.com

Processes a dictionary to generate lists of words, and calculates the best next
guess for a given board state.

This code is released under the GNU GPL-3.0:
http://www.opensource.org/licenses/GPL-3.0

"""

import zipfile
import sys, os, re, shutil

dictLocation = './pyngman_temp'
minLength = 3

def init(inputZip,useProper):
    """ Initialize word list files from a dictionary source """
    #unpack dictionary
    f = open(inputZip,'rb')
    dictionaryZip = zipfile.ZipFile(f)
    dictionaryZip.extractall(dictLocation)
    #find dic and aff files
    fileList = os.listdir(dictLocation)
    for candidate in fileList:
        if candidate.endswith('.aff'):
            affFile = open(dictLocation+'/'+candidate,'r')
        if candidate.endswith('.dic'):
            dicFile = open(dictLocation+'/'+candidate,'r')
    if not affFile or not dicFile:
        return "Couldn't find neccessary dictionary files"
    print "Found dictionary, processing rules..."
    #parse rule file
    pfx = dict()
    sfx = dict()
    currentRuleName = ""
    currentIsPFX = True
    currentRules = list()
    for rule in affFile:
        if rule[0] == '#': continue
        (ruleType,_,remainder) = rule.partition(' ')
        if ruleType not in ('PFX','SFX'): continue
        currentIsPFX = ruleType == 'PFX'
        (ruleName,_,ruleBody) = remainder.partition(' ')
        if currentRuleName != ruleName:
            #finished parsing this rule, commit to dict
            if currentIsPFX:
                pfx[currentRuleName] = currentRules
            else:
                sfx[currentRuleName] = currentRules
            currentRuleName = ruleName
            currentRules = list()
        currentRules.append(ruleBody)
        
    print "Expanding wordlist..."
    #expand wordlist using suffices
    #create files: one file for each length of words 3+, one word per line
    wordList = list()
    for word in dicFile:
        (stem,_,rules) = word.partition('/')
        if not stem.isalpha(): continue
        if not useProper and not stem.strip().islower(): continue
        if rules == "":
            #no rules for this word
            if len(stem) >= minLength:
                wordList.append(stem.lower())
        else:
            wordList.extend(applyRules(stem.lower(),rules,pfx,sfx))
    print "Printing wordlists..."
    #make unique
    wordList = list(set(wordList))
    lengths = set()
    for word in wordList:
        lengths.add(len(word))
    for i in lengths:
        outputFile = open(dictLocation + '/wordlist'+str(i)+'.txt','w')
        #Stupidely inefficient, but I don't care
        for word in wordList:
            if len(word) == i:
                outputFile.write(word+'\n')

def state(currstate,triedLetters='',minimal=False):
    """ Work out the next best guess for a given game state """
    wordLength = len(currstate)
    fileLocation = dictLocation + '/wordlist'+str(wordLength)+'.txt'
    #Sort out the contents of triedLetters
    letters = set()
    for char in currstate: letters.add(char.lower())
    for char in triedLetters: letters.add(char.lower())
    letters.remove('.')
    triedLetters = ''
    for char in letters: triedLetters = triedLetters + char
    if triedLetters != '':
        regex = currstate.replace('.','[^'+triedLetters+']')
    else:
        regex = currstate
    try:
        wordListFile = open(fileLocation,'r')
    except IOError as e:
        print "Counldn't find wordlist file, did you run -init?"
        return
    candidateList = list()
    for line in wordListFile:
        if re.match(regex,line):
            candidateList.append(line)
    if len(candidateList) == 0:
        if minimal:
            return "pyngman-fail"
        else:
            return "No words possible!"
    if len(candidateList) == 1:
        if minimal:
            return candidateList[0].strip()
        else:
            return "The only possible word is: "+candidateList[0].strip()
    letterCounter = dict()
    #find letter probabilities
    for word in candidateList:
        #use a set to make sure we're only counting a letter once per word
        chars = set()
        for char in word.strip():
            if char in triedLetters: continue
            chars.add(char)
        for char in chars:
            if char in letterCounter:
                letterCounter[char] = letterCounter[char] + 1
            else:
                letterCounter[char] = 1
    letterCounter = sortDict(letterCounter)
    if not minimal: return "Your best next guess is: "+letterCounter[0]
    return letterCounter[0]

def tidy():
    """ remove temp files """
    shutil.rmtree(dictLocation)

def applyRules(word,rules,pfx,sfx):
    """ 
        Helper function to apply a rules to a word, 
        generating a list of output words 
    """
    #split rules up
    resultList = list()
    if len(word) >= minLength:
        resultList.append(word)
    ruleList = list()
    for char in rules:
        isPrefix = False
        if char in pfx:
            ruleList = pfx[char]
            isPrefix = True
        elif char in sfx:
            ruleList = sfx[char]
        else:
            continue
        #apply the first rule that matches
        for rule in ruleList:
            ruleElements = rule.split()
            if(len(ruleElements) != 3): continue
            replaces = ruleElements[0]
            replacement = ruleElements[1]
            regex = '^.*' + ruleElements[2] + '$'
            #ignore possessive rules
            if not replacement.isalpha(): continue
            if re.match(regex,word) != None:
                #match!
                if replaces == '0':
                    if isPrefix:
                        replaced = replacement + word
                    else:
                        replaced = word + replacement
                    if(len(replaced) >= minLength):
                        resultList.append(replaced)
                else:
                    if isPrefix:
                        replaced = word.replace(replaces,replacement,1)
                    else:
                        #hack to get around lack of rtl str.replace
                        replaced = word[::-1].replace(replaces[::-1],replacement[::-1],1)[::-1]
                    if len(replaced) >= minLength:
                        resultList.append(replaced)
                break
    return resultList

def containsAny(str,chars):
    """ Check if str contains any of the characters in chars """
    return 1 in [c in str for c in chars]

def sortDict(d,desc = True):
    """ Sort a dict's keys by its values """
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    if desc:
        backitems.reverse()
    return [ backitems[i][1] for i in range(0,len(backitems))]

def usage(reason = ""):
    """ Print a usage statement """
    if reason != "":
        print reason
        print
    print "usage:"
    print
    print "  pyngman -init [-p] <input file>"
    print "    Initialize pyngman with the given zipped dictionary, <input file>."
    print "    <input file> must be a zip containing a .dic and a .aff. If -p is set,"
    print "    Proper nouns will be included, otherwise they will be excluded"
    print
    print "  pyngman -state [-m] <input phrase> [<tried letters>]"
    print "    Return the best guess for the given phrase. Input the phrase with . for"
    print "    an unknown letter, or for the letter itself otherwise."
    print "    e.g.: .o..l."
    print "    <tried letters> should be a list of letters called, e.g. eoslm. If it is"
    print "    not included, only those letters in <input phrase> wil be counted as called"
    print 
    print "    Example: pyngman -state .o..l. eoslm"
    print 
    print "    If -m is set, minimal output will be provided (useful for scripting)"
    print
    print "  pyngman -tidy"
    print "    Delete the files created by pyngman, reset the dictionary"

#main
if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 2:
        usage("Please specify an operation:")
    elif sys.argv[1] == '-init':
        if argc == 4 and sys.argv[2] == '-p':
            init(sys.argv[3],True)
        elif argc == 3:
            init(sys.argv[2],False)
        else:
            usage("Invalid arguments supplied:")
    elif sys.argv[1] == '-state':
        if argc == 3:
            print state(sys.argv[2])
        elif argc == 5 and sys.argv[2] == '-m':
            print state(sys.argv[3],sys.argv[4],True)
        elif argc == 4:
            if sys.argv[2] == '-m':
                print state(sys.argv[3],'',True)
            else:
                print state(sys.argv[2],sys.argv[3])
        else:
            usage()
    elif sys.argv[1] == '-tidy' and argc == 2:
        tidy()
    else:
        usage("Invalid arguments supplied:")
    

