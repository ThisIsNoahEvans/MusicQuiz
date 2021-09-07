import json # Read JSON data
import os # Clear the screen
import sys # Exit the program
import re # Verify inputs

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
    print('--- HELLO! ---\nWelcome back to MusicQuiz.')

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
            username = input('Enter your username: ')
            if username not in usernames:
                print('Sorry, that isn\'t a registered user.\nIf you haven\'t played MusicQuiz before, get someone who has to log in and add your account.\n')
            else:
                validUsername = True
        except:
            print('There was an error with your input. Try again.\n')
    

    correctPIN = int(usernames[username]) # Get the correct PIN from the user data
    validPIN = False
    while not validPIN:
        try:
            pin = int(input('Enter your PIN: '))
            print(f'Entered {pin}')
            if pin != correctPIN:
                print('Sorry, that isn\'t your PIN. Try again.\n')
            else:
                validPIN = True
        except:
            print('There was an error with your input. Try again.\n')

    # Run the main menu with the username
    mainMenu(username)

            
    
# Will run on first launch
# Prints welcome message, creates profile, and marks setup as complete
def setup():
    clearScreen()
    print('--- WELCOME TO MUSICQUIZ! ---\nReady to test your music knowledge?\n\nTo set up your profile, we need a name and PIN code from you. This will keep your progress separate, so multiple people can play MusicQuiz.')
    createProfile(fromSetup=True) # Create the first profile

    config = open('config.json', 'r') # Open the config file
    data = json.load(config) # Load the file contents as JSON
    config.close() # Close the file
    data['setup-complete'] = True # Set setup-complete to true (completed)
    config = open('config.json', 'w') # Open the file in write
    json.dump(data, config) # Dump the updated JSON data
    config.close() # Close the file

# Create a profile by taking a name and PIN
def createProfile(fromSetup):
    clearScreen()
    print('Let\'s set up your profile!\nYour username will be used to log you in.\nPlease enter it without any spaces or special characters.')
    
    nameSet = False
    while not nameSet:
        try:
            name = input('Enter your username: ')
            regexp = re.compile('[^0-9a-zA-Z]+') # Compile the RegEx filter of valid chars
            if regexp.search(name): # If the name contains invalid chars
                print('Sorry, that username contains invalid characters.\nYou can only use alphanumeric characters (A-Z, 1-9).\n')
            else: # Correct username
                nameSet = True
        except:
            print('You didn\'t enter a valid username. Try again.\n')
    
    pinSet = False
    while not pinSet:
        try:
            pin = int(input('Enter a 4-digit PIN code: ')) # Ask for an int
            if (len(str(pin))) != 4: # PIN is not 4 digits
                print('Your code wasn\'t 4 digits. Try again.')
            else: # Pin is 4 digits
                pinSet = True # Exit the while loop
        except: # Error with value - likely entered non-numeric characters
            print('You didn\'t enter a valid PIN code. Try again.')
    
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
        print(f'Welcome, {name}! Let\'s get you into your first game.')
    else:
        print(f'Welcome, {name}! Your profile is now active.')
        mainMenu(name)

# The main menu
# To be displayed after setup/a game
def mainMenu(name):
    clearScreen()
    print(f'--- MAIN MENU ---\nHi, {name}!\n1 - New Game\n2 - View Top Scores\n3 - Switch Player\n4 - Add Player\n5 - Settings\n6 - Quit')
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(':: Enter an option: '))
            if not 1 <= choice <= 6:
                print('That isn\'t a valid option. Try again.')
            else:
                menuInput = True
        except:
            print('That isn\'t a valid option. Try again.')
    
    if choice == 1:
        # New Game
        pass
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


def settings():
    clearScreen()
    print(f'--- SETTINGS ---\nChoose an option:\n1 - Configure Game Settings\n2 - Delete Player\n3 - Remove All Data\n4 - About')
    
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(':: Enter an option: '))
            if not 1 <= choice <= 5:
                print('That isn\'t a valid option. Try again.')
            else:
                menuInput = True
        except:
            print('That isn\'t a valid option. Try again.')
    
    if choice == 1:
        pass
    elif choice == 2:
        # Settings
        settings()
    elif choice == 3:
        pass
    elif choice == 4:
        clearScreen()
        print('Goodbye! Thank you for playing.')
        sys.exit()



# Run the initial launch sequence
# when the Python file is run
launch()


