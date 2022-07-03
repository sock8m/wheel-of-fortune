from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    opendict = open(dictionaryloc)
    readdict = opendict.read().splitlines()
    opendict.close()
    # Store each word in a list.
    for word in readdict:
        dictionary.append(word)
      
    
def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file

        
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location 

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location 
    openwheel = open(wheeltextloc)
    readwheel = openwheel.read().splitlines()
    openwheel.close()
    # Store each word in a list.
    for category in readwheel:
        wheellist.append(category)
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    for i in range(0,len(players)):
        players[i]["name"] = str(input(f"Enter the name of player {i+1}: "))

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    #choose random word from dictionary
    roundWord = random.choice(dictionary)
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = []
    for i in range(0,len(roundWord)):
        roundUnderscoreWord.append("_")
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    for i in range(0,len(players)):
        players[i]["roundtotal"] = 0
    # Return the starting player number (random)
    initPlayer = random.choice([0,1,2])
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundWord, blankWord = getWord()

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    # Get random value for wheellist
    wheelRoll = random.choice(wheellist)
    print(f"You rolled: {wheelRoll}")
    stillinTurn = True
    # Check for bankrupcy, and take action.
    if wheelRoll == "BANKRUPT":
        players[playerNum]["roundtotal"] = 0
        stillinTurn = False
    # Check for loose turn
    elif wheelRoll == "LOSE A TURN":
        stillinTurn = False
    # Get amount from wheel if not loose turn or bankruptcy
    elif wheelRoll[0] == "$":
    # Ask user for letter guess
        letterguess = str(input("Guess a letter!: ")).lower()
    # Use guessletter function to see if guess is in word, and return count
        validguess, count, consonantT = guessletter(letterguess, playerNum)
    # Change player round total if they guess right.
        if not validguess:
            stillinTurn = False
        elif validguess and consonantT == "C":
            players[playerNum]["roundtotal"] += int(wheelRoll[1:])
            print(blankWord)
        elif validguess and consonantT == "V":
            print("you guessed a vowel!")
            stillinTurn = False
    else:
        print("there is an error with the wheel roll values!")   
    return stillinTurn

def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundWord

    goodGuess = False
    count = 0
    VorC = "not in word"
    # parameters:  take in a letter guess and player number
    for letternum in range(0,len(roundWord)):
    # Change position of found letter in blankWord to the letter instead of underscore 
        if roundWord[letternum] == letter:
            blankWord[letternum] = letter
    # return goodGuess= true if it was a correct guess
            goodGuess = True
    # return count of letters in word. 
            count += 1
    # ensure letter is a consonate.
            if letter not in vowels:
                VorC = "C"
            elif letter in vowels:
                VorC = "V"
            else: 
                VorC = "not in word"
                print("check input letter for errors!")
    if goodGuess == False:
        print("This letter is not in the word.")

    return goodGuess, count, VorC

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    if players[playerNum]["roundtotal"] > vowelcost:
        vowelGuess = str(input(f"Guess a vowel, player {playerNum+1}: ")).lower()
        players[playerNum]["roundtotal"] -= vowelcost
    # Use guessLetter function to see if the letter is in the file
        goodGuess, countV, vowelT = guessletter(vowelGuess, playerNum)
    # Ensure letter is a vowel
        if vowelT == "V":
            goodGuess = True
            print(blankWord)
        elif vowelT == "C":
            goodGuess = False
            print("you guessed a consonant!")
    # If letter is in the file let goodGuess = True
    return goodGuess
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    wordGuess = str(input(f"Guess the word, player {playerNum+1}! ")).lower()
    if wordGuess == roundWord:
    # Fill in blankList with all letters, instead of underscores if correct 
        blankWord = []
        for letter in roundWord:
            blankWord.append(letter)
    else:
        print("Wrong guess!")
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    displayRoundTotal = players[playerNum]["roundtotal"]
    print(f"Hello, player {playerNum+1}! You have ${displayRoundTotal}.")
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinTurn = True
    while stillinTurn:
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        choice = str(input("Will you (S)pin the wheel, (B)uy vowel, or (G)uess the word? "))

        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.strip().upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    endofroundWord = ""
    for i in blankWord:
        endofroundWord += i
    if endofroundWord == roundWord: 
        return False
    else:
        return True
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    currentPlayer = initPlayer
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    continueTurn = True
    while continueTurn:
        continueTurn = wofTurn(currentPlayer)
        if continueTurn == False:
            break
        # updates current player at the end of the turn
        if currentPlayer == 2:
            currentPlayer = 0
        else:
            currentPlayer += 1

    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    print(f"This round has ended! The word is {roundWord}")
    moneyKept = players[currentPlayer]["roundtotal"]
    players[currentPlayer]["gametotal"] += moneyKept
    print(f"{players[currentPlayer]['name']} has won ${moneyKept}.")
    print(f"Totals: {players[0]['name']} with ${players[0]['gametotal']}")
    print(f"Totals: {players[1]['name']} with ${players[1]['gametotal']}")
    print(f"Totals: {players[2]['name']} with ${players[2]['gametotal']}")

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global players
    global finalprize
    winplayer = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing.
    maxGT = 0
    for item in players.keys():
        money = players[item]["gametotal"]
        if money > maxGT: 
            maxGT = money
            FRplayer = item
    # Print out instructions for that player and who the player is.
    print(f"Welcome to the final round, {players[FRplayer]['name']}.")
    print("You have 3 consonant and 1 vowel guesses.")
    print("You get the letters R, S, T, L, N, and E for free.")
    print("Guess the word and win the grand prize!")
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    roundWord, blankWord = getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    for i in ("r", "s", "t", "l", "n", "e"):
        guessletter(i, FRplayer)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f"Here is your hint: {blankWord}")
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    print(f"Guess 3 consonants and 1 vowel.")
    consonantG = 0
    vowelG = 0
    guessingIncomplete = True
    while guessingIncomplete:
        letter = str(input(f"Guess letter: ")).lower()
        _,_,VorC = guessletter(letter, FRplayer)
        if VorC == "C" and consonantG < 3:
            print("This is in the word")
            print(blankWord)
            consonantG += 1
        elif VorC == "C" and consonantG >= 3:
            print("You have already guessed 3 consonants.")
        elif VorC == "V" and vowelG < 1:
            print("you guessed a vowel")
            print(blankWord)
            vowelG += 1
        elif VorC == "V" and vowelG >= 1:
            print("You have already guessed 1 vowel.")
        else: print("error!")

        if consonantG >= 3 and vowelG >= 1:
            guessingIncomplete = False
    
    # Print out the current blankWord again
    # Remember guessletter should fill in pthe letters with the positions in blankWord
    # Get user to guess word
    print("Time to guess the word!")
    frWordGuess = guessWord(FRplayer)
    # If they do, add finalprize and gametotal and print out that the player won 
    if frWordGuess:
        players[FRplayer]['gametotal'] += finalprize
        print(f"You won! Enjoy your total prize of ${players[FRplayer]['gametotal']}")
    else:
        print(f"You lost! However, you still won a total of ${players[FRplayer]['gametotal']}.")

def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
