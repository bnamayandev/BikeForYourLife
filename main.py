#-----------------------------------------------------------------------------
# Name:        Python Assignment 2: Bike for your Life!
# Purpose:     Adding Logging to previous code
#
# Author:      Benjamin Namayandeh
# Created:     2-May-2022
# Updated:     3-Jun-2022
#-----------------------------------------------------------------------------

# modules 
import logging
import sys
import replit
import time
import threading
from getkey import getkey, keys
import passages
from colorama import init, Fore, Back, Style

#init logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# create trials list
trials = []

# Class required to move monster on its own
class GameState:
  def __init__(self, correctWords, currentWord, passage, progressBarTop, progressBarBottom, wpm, progress, icon):
    '''
    intializing gameState (basically the thing that makes monster move)

    Parameters
    ----------
    correctWords : list
        words that have been inputted correctly

    currentWord: string
      The current character which is being typed

    passage: list
      What is remaining of the passage left to write (minus current word)

    progressBarTop: list
      where the monster and bike are situated

    progressBarBottom: list
      The underscores below the bike and the monster

    wpm: int
      the users wpm rate

    progress: float
      how much of the passage the user has completed(as a decima)

    icon: string
      the icon that the monster is using

    Returns
    -------
    None

    '''
    self.correctWords = correctWords
    self.passage = passage
    self.progressBarTop = progressBarTop
    self.progressBarBottom = progressBarBottom
    self.wpm = wpm
    self.progress = progress
    self.icon = icon

  def getCurrentWord(self):
    '''
    Gets the letter/character that the user is currently trying to type in

    Parameters
    ----------
    self: class
      The class and the functions within it

    Returns
    -------
    The letter/character that the user is currently trying to type in

    '''
    # an index error means that there is no letter left i.e. the user has finished the level successfully
    try:
      return self.passage[0].lower()
    except IndexError:
      replit.clear()

      return 'escaped'
      print("You have escaped...\n[PRESS ENTER]")
      input()


def print_with_color(string, color, **kwargs):
  '''
  Function that lets you print words with different colors

  Parameters
  ----------
  string : string
      The wprd/phrase that will be changed to a different color

  color: string
    What color 'string' will be changed to

  Returns
  -------
  return the string with the color applied

  '''
  brightness=Style.NORMAL
  return print(f"{brightness}{color}{string}{Style.RESET_ALL}", end = "", **kwargs)


def moveMonster(gameState, rest):
  '''
  Function that moves the monster at different speeds based on level

  Parameters
  ----------
  gameState : class
      all the variables assosciated with gameState

  rest: float
    the constant amount of time that the monster move

  Returns
  -------
  None

  '''
  # Grace period
  time.sleep(3)

  # while game running (essentially)
  while (len(gameState.passage) != 0) and (gameState.icon in gameState.progressBarTop):
    time.sleep(rest) 

    # Add a space before the monster, and delete a space after the monster so that it looks like it moved closer to the bike
    gameState.progressBarTop.insert(0, " ")
    gameState.progressBarTop.pop(gameState.progressBarTop.index("🚲")-1)
    replit.clear()

    #Outputs
    print_with_color(f"{''.join(gameState.correctWords)}", Fore.GREEN)
    print_with_color(gameState.getCurrentWord(), Back.YELLOW)
    print(f"{''.join(gameState.passage[1:])}\n")
    print(f"\n\n{gameState.wpm} Words Per Minute")
    print(f"{gameState.progress}% done\n\n")

    print(f"{''.join(gameState.progressBarTop)}")
    print(f"{''.join(gameState.progressBarBottom)}\n")

  replit.clear()

def pedal(passage, monster, monsterSpeed):
  '''
  The main function of the program (is only a function because there are 3 levels and all 3 go through the same process)

  Parameters
  ----------
  passage : list
      the list of words that create the passage the user is trying to type

  monster: string
    the icon of the monster

  monsterSpeed: int
    the speed at which the monster advances

  Returns
  -------
  returns "lost" if the user was caught, this makes it possible to keep trying until user wins.

  '''

  # Varibles
  bike = "🚲"
  progressBarTop = [monster, bike]
  progressBarBottom = [ "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "___","🚩"]
  # Count down
  input("\n\n[press enter to begin]\n")
  replit.clear()
  for i in range(3):
    print(3-i)
    time.sleep(0.5)
    replit.clear()

  # start clock, used to calculate WPM
  start = time.time()

  # choose random passage from list
  passage = list(passage.lower())
  correctWords = []
  currentWord = ''
  wpm = 0
  progress = 0
  charsInPassage = len(passage)
  logging.debug(passage)
  print(f"{''.join(passage)}\n")

  # Display word per minute (at 0 when you begin)
  print(f"\n\n0 Words Per Minute")

  # Display Percentage (at 0 when you begin)
  print(f"0% done\n\n")

  # show progress bar
  print(f"{''.join(progressBarTop)}")
  print(f"{''.join(progressBarBottom)}\n")

   # create thread to move monster seperatley and at a constant rate
  gameState = GameState(correctWords, currentWord, passage, progressBarTop, progressBarBottom, wpm, progress, monster)
  thread = threading.Thread(target = moveMonster, args = (gameState, monsterSpeed))
  thread.start()

  # while user has nor finished level, or lost
  while (len(gameState.passage) != 0) and (gameState.icon in gameState.progressBarTop):
    #if statement to make sure that the highlighting stays on the last letter of the paragraph and doesn't extend past the writing and duplicate the last letter
    if len(passage) == 1:
      gameState.currentWord = passage[0].lower()
    else:
      gameState.currentWord = passage[1].lower()

    # get user input
    key = getkey().lower()

      # print all the characters before current letter in green, the letter you're on in yellow, and the ones left to spell in white.
    if key == passage[0].lower():
      correctWords.append(passage.pop(0))
      replit.clear()
      print_with_color(f"{''.join(correctWords)}", Fore.GREEN)

      # Print current word with a yellow highlight to differentiate it
      #if statement so there isn't a repeated last character at the end of the paragraph
      if len(passage) > 0:
        print_with_color(gameState.getCurrentWord(), Back.YELLOW)

      #Join rest of the passage to the end of current word
      print(f"{''.join(passage[1:])}\n")


    # if input doesn't match required input highlight the current word in red instead of yellow
    elif key != passage[0].lower():
      # refresh screen
      replit.clear()

      # print passage
      print_with_color(f"{''.join(correctWords)}", Fore.GREEN)
      print_with_color(gameState.getCurrentWord(), Back.RED)
      print(f"{''.join(passage[1:])}\n")


    # Get wpm by checking # of spaces in 'correctWords'
    wordsDone = 1 #to account for final word
    for letter in correctWords:
      if letter == " ":
        wordsDone += 1

    # Calculaitng Words per minute
    currentTime = time.time() - start
    gameState.wpm = round((wordsDone/currentTime)*60)
    print(f"\n\n{gameState.wpm} Words Per Minute")
    trials.append(gameState.wpm)

    # Calculating percentage done
    percent = len(correctWords)/charsInPassage
    logging.debug(len(correctWords))
    logging.debug(charsInPassage)
    gameState.progress = round(percent*100)
    print(f"{gameState.progress}% done\n\n")

    #change bike position on the progress bar
    posBike = round(percent*len(progressBarBottom))
    if progressBarTop.index(bike) < posBike:
      logging.debug(progressBarTop.index(monster))
      try:
        progressBarTop.insert(progressBarTop.index(monster)+1, " ")
      except ValueError:
        return 'lost'

    #print progress bar
    print(f"{''.join(progressBarTop)}")
    print(f"{''.join(progressBarBottom)}\n")

    #end program if monster catches you
    if (gameState.icon not in gameState.progressBarTop):
      thread.join()
      replit.clear()
      return 'lost'

  # end thread
  thread.join()

def averageWPM(trials):
  '''
  used to calculate the average WPM that the user is typing at that specific point

  Parameters
  ----------
  trails : list
      all the wpm that the user has typed at throughout the game

  Returns
  -------
  returns 'ZeroDivisionError' if there is nothing in the list
  returns the average words per minute rounded to 2 decimals

  '''

  logging.debug(trials)
  logging.debug(len(trials))

  if len(trials) == 0:
    return 'ZeroDivisionError'

  else:
    wpm = 0
    for trial in trials:
      wpm += trial
    wpm = wpm/(len(trials))
    return round(wpm,2)

###############################
#######START OF PROGRAM########
###############################


####Assertions####
#assert averageWPM([5]) == 5
#assert averageWPM([1,2,3,4,5]) == 3
#assert averageWPM([]) == "ZeroDivisionError"
#assert averageWPM(["None", "None"]) == "TypeError"

####creating and object to test class functions
classAssertions = GameState("None", "None", "I", "None", "None", "None", "None", "None", )
assert classAssertions.getCurrentWord() == "i"

classAssertions = GameState("None", "None", "2020 was the year corona virus began", "None", "None", "None", "None", "None", )
assert classAssertions.getCurrentWord() == "2"

#Failures
classAssertions = GameState("None", "None", "...", "None", "None", "None", "None", "None", )
assert classAssertions.getCurrentWord() == "."

classAssertions = GameState("None", "None", "", "None", "None", "None", "None", "None", )
assert classAssertions.getCurrentWord() == "escaped"


#Title Screen
print_with_color('''
██████╗░██╗██╗░░██╗███████╗  ███████╗░█████╗░██████╗░  
██╔══██╗██║██║░██╔╝██╔════╝  ██╔════╝██╔══██╗██╔══██╗  
██████╦╝██║█████═╝░█████╗░░  █████╗░░██║░░██║██████╔╝  
██╔══██╗██║██╔═██╗░██╔══╝░░  ██╔══╝░░██║░░██║██╔══██╗  
██████╦╝██║██║░╚██╗███████╗  ██║░░░░░╚█████╔╝██║░░██║  
╚═════╝░╚═╝╚═╝░░╚═╝╚══════╝  ╚═╝░░░░░░╚════╝░╚═╝░░╚═╝  

██╗░░░██╗░█████╗░██╗░░░██╗██████╗░  ██╗░░░░░██╗███████╗███████╗
╚██╗░██╔╝██╔══██╗██║░░░██║██╔══██╗  ██║░░░░░██║██╔════╝██╔════╝
░╚████╔╝░██║░░██║██║░░░██║██████╔╝  ██║░░░░░██║█████╗░░█████╗░░
░░╚██╔╝░░██║░░██║██║░░░██║██╔══██╗  ██║░░░░░██║██╔══╝░░██╔══╝░░
░░░██║░░░╚█████╔╝╚██████╔╝██║░░██║  ███████╗██║██║░░░░░███████╗
░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝  ╚══════╝╚═╝╚═╝░░░░░╚══════╝
''', Fore.BLUE)
print_with_color('''
▒█▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ 　 ▒█▀▀▀ ▒█▄░▒█ ▀▀█▀▀ ▒█▀▀▀ ▒█▀▀█ 　 
▒█▄▄█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ 　 ▒█▀▀▀ ▒█▒█▒█ ░▒█░░ ▒█▀▀▀ ▒█▄▄▀ 　 
▒█░░░ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ 　 ▒█▄▄▄ ▒█░░▀█ ░▒█░░ ▒█▄▄▄ ▒█░▒█ 　 

▀▀█▀▀ ▒█▀▀▀█ 　 ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█ ▀█▀ ▒█▄░▒█ 
░▒█░░ ▒█░░▒█ 　 ▒█▀▀▄ ▒█▀▀▀ ▒█░▄▄ ▒█░ ▒█▒█▒█ 
░▒█░░ ▒█▄▄▄█ 　 ▒█▄▄█ ▒█▄▄▄ ▒█▄▄█ ▄█▄ ▒█░░▀█\n\n\n\n''', Fore.RED)
input()
replit.clear()

# print expositon
print('''The year is 2222, and monsters have taken over the world. Only you remain, Bry Sickle, the fastest (and now only) cyclist in the world. You must bike away from the monsters in order to survive.''')

# Loop until win or close
while pedal(passages.passages[0], "👾", 2) == 'lost':
  print("You were caught, what would you like to do\n1. Restart level\n2. Exit Game")
  choice = input("Enter corresponding number: ")
  #make sure choice is valid
  while choice != '1' or choice !='2':
    if choice == '1':
      print("\n[RESTARTED]")
      break
    elif choice == '2':
      sys.exit()
    else:
      choice = input("Enter a valid choice: ")

print_with_color(f"You are currently typing at {averageWPM(trials)} WPM\n", Back.GREEN)
print("You seem to have lost it. You enter an abandoned building and choose to look inside. Instantly you see a map labeled with the building you're in and a place labeled 'CURE!!!' just a little ways away. You decide to investigate, but just as you hop onto your bike you're seen by another monster.")

# Loop until win or close
while pedal(passages.passages[1], "👹", 1.6)== 'lost':
  print("You were caught, what would you like to do\n1. Restart level\n2. Exit Game")
  choice = input("Enter corresponding number: ")
  #make sure choice valid
  while choice != '1' or choice !='2':
    if choice == '1':
      print("\n[RESTARTED]")
      break
    elif choice == '2':
      sys.exit()
    else:
      choice = input("Enter a valid choice: ")
replit.clear()

print_with_color(f"You are currently typing at {averageWPM(trials)} WPM\n", Back.GREEN)
print("You appear to have lost the monster. You arrive at the place labeled 'CURE!!!' on the map, and it seems to be a gated farmyard with a small shed in the distance. You hear something behind you and turn around to see largest monster ever. You instantly begin pedaling to the shed, maybe you can hope to escape it there...")

# Loop until win or close
while pedal(passages.passages[2], "👽", 1.3)== 'lost':
  print("You were caught, what would you like to do\n1. Restart level\n2. Exit Game")
  choice = input("Enter corresponding number: ")
  #make sure choice valid
  while choice != '1' or choice !='2':
    if choice == '1':
      replit.clear()
      print("\n[RESTARTED]")
      break
    elif choice == '2':
      sys.exit()
    else:
      choice = input("Enter a valid choice: ")

print("You hop off your bike and enter the shack panting. You see a button labelled 'PRESS!!!' and pick it up. You cautiously press it and hear loud shrieks coming from outside the shed you look outside to see all the monsters lying dead. maybe they were infused with plotde vice, a special thing that kills them or something...\n")
print(f"You have saved the world while writing/pedalling at an average of {averageWPM(trials)}WPM!")