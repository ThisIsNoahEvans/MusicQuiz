import json # Read JSON data
import os # Clear the screen
import sys # Exit the program
import re # Verify inputs
import time # Delays
import random # Pick random songs
from colorama import Fore, Style # Print in colours

global currentUser
currentUser = ''

# Clear everything on the screen
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear') # Windows - cls // UNIX - clear

# Check if setup needs to be run.
# Else, present the main menu.
def launch():
    with open('config.json') as config: # Open the config file
        data = json.load(config) # Load the file contents as JSON
        if data['setup-complete'] == True: # If setup is complete
            config.close() # Close the file
            login() # Launch the login process
        else: # Setup is not complete
            config.close() # Close the file
            setup() # Run setup

# Run on launch: ask the user to authenticate
def login():
    clearScreen()
    print(f'{Fore.GREEN}--- HELLO! ---\nWelcome back to MusicQuiz.{Style.RESET_ALL}')

    ## Get the JSON user data
    userData = open('user-data.json', 'r') # Open the user data file
    dataJSON = json.load(userData) # Load the file contents as JSON
    userData.close() # Close the JSON file
    users = dataJSON['users'] # A dict with all of the user data
    usernames = {}
    for user in users:
        usernames[user['name']] = user['pin'] # Add each user's name & PIN to the dict
        

    validUsername = False
    while not validUsername:
        try:
            username = input(f'{Fore.MAGENTA}:: Enter your username: {Style.RESET_ALL}')
            if username not in usernames:
                print(f'{Fore.RED}Sorry, that isn\'t a registered user.\nIf you haven\'t played MusicQuiz before, get someone who has to log in and add your account.\n{Style.RESET_ALL}')
            else:
                validUsername = True
        except:
            print(f'{Fore.RED}There was an error with your input. Try again.\n{Style.RESET_ALL}')
    

    correctPIN = int(usernames[username]) # Get the correct PIN from the user data
    validPIN = False
    while not validPIN:
        try:
            pin = int(input(f'{Fore.MAGENTA}:: Enter your PIN: {Style.RESET_ALL}'))
            if pin != correctPIN:
                print(f'{Fore.RED}Sorry, that isn\'t your PIN. Try again.\n{Style.RESET_ALL}')
            else:
                validPIN = True
        except:
            print(f'{Fore.RED}There was an error with your input. Try again.\n{Style.RESET_ALL}')

    # Run the main menu with the username
    global currentUser
    currentUser = username
    mainMenu()

            
    
# Will run on first launch
# Prints welcome message, creates profile, and marks setup as complete
def setup():
    clearScreen()
    print(f'{Fore.BLUE}--- WELCOME TO MUSICQUIZ! ---{Style.RESET_ALL}\nReady to test your music knowledge?\n\nTo set up your profile, we need a name and PIN code from you. This will keep your progress separate, so multiple people can play MusicQuiz.')
    input(f'{Fore.MAGENTA}:: Press enter to continue.{Style.RESET_ALL}')
    createProfile(fromSetup=True) # Create the first profile

    config = open('config.json', 'r') # Open the config file
    data = json.load(config) # Load the file contents as JSON
    config.close() # Close the file
    data['setup-complete'] = True # Set setup-complete to true (completed)
    config = open('config.json', 'w') # Open the file in write
    json.dump(data, config) # Dump the updated JSON data
    config.close() # Close the file
    mainMenu()

# Create a profile by taking a name and PIN
def createProfile(fromSetup):
    clearScreen()
    print(f'{Fore.BLUE}--- PROFILE SETUP ---{Style.RESET_ALL}\nYour username will be used to log you in.\nPlease enter it without any spaces or special characters.')
    
    nameSet = False
    while not nameSet:
        try:
            name = input(f'{Fore.MAGENTA}:: Enter your username: {Style.RESET_ALL}')
            regexp = re.compile('[^0-9a-zA-Z]+') # Compile the RegEx filter of valid chars
            if regexp.search(name): # If the name contains invalid chars
                print(f'{Fore.RED}Sorry, that username contains invalid characters.\nYou can only use alphanumeric characters (A-Z, 1-9).\n{Style.RESET_ALL}')
            else: # Correct username
                nameSet = True
        except:
            print(f'{Fore.RED}You didn\'t enter a valid username. Try again.\n{Style.RESET_ALL}')
    
    pinSet = False
    while not pinSet:
        try:
            pin = int(input(f'{Fore.MAGENTA}:: Enter a 4-digit PIN code: {Style.RESET_ALL}')) # Ask for an int
            if (len(str(pin))) != 4: # PIN is not 4 digits
                print(f'{Fore.RED}Your code wasn\'t 4 digits. Try again.{Style.RESET_ALL}')
            else: # Pin is 4 digits
                pinSet = True # Exit the while loop
        except: # Error with value - likely entered non-numeric characters
            print(f'{Fore.RED}You didn\'t enter a valid PIN code. Try again.{Style.RESET_ALL}')
    
    ## Get the JSON user data
    userData = open('user-data.json', 'r') # Open the user data file
    dataJSON = json.load(userData) # Load the file contents as JSON
    userData.close() # Close the JSON file

    ## Get the new user's ID from the config JSON file
    config = open('config.json', 'r') # Open the config file
    configJSON = json.load(config) # Load the file contents as JSON
    config.close() # Close the JSON file
    userID = int(configJSON['lastUserID']) + 1 # Add 1 to the previous user ID

    dataJSON['users'].append({"id":userID, "name":name, "topScore":0, "gamesPlayed":0, "pin":pin, "correctSongs":[]}) # Add the user data to the JSON array
    
    # Save the new lastUserID
    configJSON['lastUserID'] = userID # Update the last user ID in the config JSON
    config = open('config.json', 'w') # Open the config file in write
    json.dump(configJSON, config) # Dump the updated JSON data
    config.close() # Close the JSON file

    # Save the updated user data (with new user)
    userData = open('user-data.json', 'w') # Open the user data file in write
    json.dump(dataJSON, userData) # Dump the updated JSON data
    userData.close() # Close the JSON file
    
    if fromSetup == True:
        print(f'{Fore.GREEN}Welcome, {name}! Let\'s get you into your first game.{Style.RESET_ALL}')
        global currentUser
        currentUser = name
        time.sleep(2)
    else:
        print(f'{Fore.GREEN}Welcome, {name}! Your profile is now active.{Style.RESET_ALL}')
        currentUser = name
        time.sleep(2)
        mainMenu()
        

# The main menu
# To be displayed after setup/a game
def mainMenu():
    clearScreen()
    print(f'{Fore.BLUE}--- MAIN MENU ---\nHi, {currentUser}!{Style.RESET_ALL}\n1 - New Game\n2 - View Top Scores\n3 - Switch Player\n4 - Add Player\n5 - Settings\n6 - Quit')
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(f'{Fore.MAGENTA}:: Enter an option: {Style.RESET_ALL}'))
            if not 1 <= choice <= 6:
                print(f'{Fore.RED}That isn\'t a valid option. Try again.{Style.RESET_ALL}')
            else:
                menuInput = True
        except:
            print(f'{Fore.RED}That isn\'t a valid option. Try again.{Style.RESET_ALL}')
    
    if choice == 1:
        # New Game
        mainGame()
    elif choice == 2:
        # Top Scores
        pass
    elif choice == 3:
        # Switch Player
        login()
    elif choice == 4:
        # Add Player
        createProfile(fromSetup=False)
    elif choice == 5:
        # Settings
        settings()
    elif choice == 6:
        # Quit
        clearScreen()
        print('Goodbye! Thank you for playing.')
        sys.exit()

# The actual game
def mainGame():
    clearScreen()
    print(f'{Fore.BLUE}--- NEW GAME ---{Style.RESET_ALL}\nTime to play a game of MusicQuiz!\nYou will be given the artist and album name, plus the first letter of each word in the song title.\nYou will have two chances to guess the correct title.\n')
    input(f'{Fore.MAGENTA}:: Press enter to start the game.{Style.RESET_ALL}')
    config = open('config.json', 'r') # Open the config file
    configJSON = json.load(config) # Load the file contents as JSON
    config.close() # Close the JSON file
    gameLength = configJSON['songsPerGame'] # Get the songs per game choice

    songsFile = open('songs.json', 'r') # Open the songs file
    songs = json.load(songsFile) # Load the file contents as JSON
    songsFile.close() # Close the JSON file

    songNum = 0
    score = 0

    for song in range(gameLength): # For each song in the game
        clearScreen()
        songNum = songNum + 1
        attempts = 0
        correctSongs = 0
        chosenSong = random.choice(songs)
        songID = chosenSong['id']
        songTitle = chosenSong['title']
        songArtist = chosenSong['artist']
        songAlbum = chosenSong['album']
        songTitleLength = len(songTitle)

        wordsInTitle = songTitle.split()
        letters = [word[0] for word in wordsInTitle]
        firstLetters = " ".join(letters)
        print(f'SONG {songNum}/{gameLength}:\n\n{Fore.LIGHTBLUE_EX}Album: {songAlbum}\nArtist: {songArtist}\nTitle: {firstLetters}\nTitle Character Count: {songTitleLength}{Style.RESET_ALL}')
    

        menuInput = False
        while not menuInput:
            try:
                answer = input(f'{Fore.MAGENTA}:: Enter the full name of this song: {Style.RESET_ALL}')
                attempts = attempts + 1
                if answer.lower() != songTitle.lower():
                    print(f'{Fore.RED}Incorrect!{Style.RESET_ALL}')
                    if attempts == 1:
                        print('You have one more attempt.')
                    elif attempts == 2:
                        print(f'Game over!\nYour score was {score}.')
                        input('Press enter to return to the main menu.')
                        mainMenu()
                else: # Correct
                    correctSongs = correctSongs + 1
                    if attempts == 1:
                        score = score + 3
                    elif attempts == 2:
                        score = score + 1
                    print(f'{Fore.GREEN}Correct, well done!\nScore: {score}{Style.RESET_ALL}')
                    if songNum != gameLength:
                        input('Press enter to begin the next song.')
                        menuInput = True
                    else:
                        menuInput = True
            except:
                print(f'{Fore.RED}There was an error with your input. Try again.{Style.RESET_ALL}')
        
    clearScreen()
    print(f'{Fore.GREEN}GAME COMPLETE!{Style.RESET_ALL}\nYour score was {correctSongs}/{gameLength} - {(correctSongs / gameLength) * 100}.\nThank you for playing MusicQuiz!')
    input(f'{Fore.MAGENTA}Press enter to return to the main menu.{Style.RESET_ALL}')
    mainMenu()        


def settings():
    clearScreen()
    print(f'{Fore.BLUE}--- SETTINGS ---{Style.RESET_ALL}\nChoose an option:\n1 - Change Songs Per Game\n2 - Remove All Data\n3 - About')
    
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(f'{Fore.MAGENTA}:: Enter an option: {Style.RESET_ALL}'))
            if not 1 <= choice <= 4:
                print(f'{Fore.RED}That isn\'t a valid option. Try again.{Style.RESET_ALL}')
            else:
                menuInput = True
        except:
            print(f'{Fore.RED}That isn\'t a valid option. Try again.{Style.RESET_ALL}')
    
    if choice == 1:
        # Songs Per Game
        songsPerGame()
    elif choice == 2:
        # Remove All Data
        removeAllData()
    elif choice == 3:
        # About - UNFINISHED
        print('UNFINISHED')


# Custom amount of songs per game
def songsPerGame():
    clearScreen()

    config = open('config.json', 'r') # Open the config file
    configJSON = json.load(config) # Load the file contents as JSON
    config.close() # Close the JSON file
    currentChoice = configJSON['songsPerGame']

    print(f'{Fore.BLUE}--- SONGS PER GAME ---{Style.RESET_ALL}\nEach game can have between 5 and 20 songs.\nThe default is 10. Current choice: {currentChoice}.')
    
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(f'{Fore.MAGENTA}:: Pick your game length: {Style.RESET_ALL}'))
            if not 5 <= choice <= 20:
                print(f'{Fore.RED}Your choice must be between 5 and 20 songs.{Style.RESET_ALL}')
            else:
                menuInput = True
        except:
            print(f'{Fore.RED}That isn\'t a valid number. Try again.{Style.RESET_ALL}')


    configJSON['songsPerGame'] = choice # Update the songs per game in the config JSON
    config = open('config.json', 'w') # Open the config file in write
    json.dump(configJSON, config) # Dump the updated JSON data
    config.close() # Close the JSON file

    print(f'{Fore.GREEN}\nGames will now last for {choice} songs.\nReturning to the main menu...{Style.RESET_ALL}')
    time.sleep(1)
    mainMenu()  

# Remove and reset the game
def removeAllData():
    clearScreen()
    print(f'{Fore.BLUE}--- REMOVE ALL DATA ---{Style.RESET_ALL}\nAll of your data from MusicQuiz will be removed.\nThis cannot be undone.')

    defaultConfig = '{"setup-complete": false, "lastUserID": 0, "songsPerGame": 10}'
    defaultUsers = '{"users": []}'

    menuInput = False
    while not menuInput:
        try:
            choice = input(f'{Fore.MAGENTA}:: Type `DELETE` to confirm that you would like to remove all data and reset MusicQuiz. {Style.RESET_ALL}')
            if choice == 'DELETE':
                config = open('config.json', 'w') # Open the config file in write
                config.seek(0)
                config.write(defaultConfig)
                config.truncate()
                config.close()
                
                userConfig = open('user-data.json', 'w') # Open the config file in write
                userConfig.seek(0)
                userConfig.write(defaultUsers)
                userConfig.truncate()
                userConfig.close()

                print(f'{Fore.GREEN}All data has been deleted.\n\nThank you for playing MusicQuiz.{Style.RESET_ALL}')
                menuInput = True
            else:
                print(f'{Fore.RED}Deletion cancelled. Returning to the main menu...{Style.RESET_ALL}')
                time.sleep(1)
                mainMenu()
                menuInput = True
        except:
            print(f'{Fore.RED}There was an error with your input.{Style.RESET_ALL}')

# Run the initial launch sequence
# when the Python file is run
launch()


