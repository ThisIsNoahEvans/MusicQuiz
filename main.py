import json
import os
import sys

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

# Check if setup needs to be run.
# Else, present the main menu.
def launch():
    with open('config.json') as config: # Open the config file
        data = json.load(config) # Load the file contents as JSON
        if data['setup-complete'] == True: # If setup is complete
            config.close() # Close the file
            mainMenu('name') # Show the main menu
        else: # Setup is not complete
            config.close() # Close the file
            setup() # Run setup

            
    
# Will run on first launch
# Prints welcome message, creates profile, and marks setup as complete
def setup() :
    clearScreen()
    print('--- WELCOME TO MUSIC QUIZ! ---\nReady to test your music knowledge?\n\n')
    print('To set up your profile, we need a name and PIN code from you. This will keep your progress private so only you can play Music Quiz.')
    createProfile()

    config = open('config.json', 'r') # Open the config file
    data = json.load(config) # Load the file contents as JSON
    config.close() # Close the file
    data['setup-complete'] = True # Set setup-complete to true (completed)
    config = open('config.json', 'w') # Open the file in write
    json.dump(data, config) # Dump the updated JSON data
    config.close() # Close the file

# Create a profile by taking a name and PIN
def createProfile():
    name = input('Enter your name: ')
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
    
    print(f'Welcome, {name}! Let\'s get you into your first game.')

# The main menu
# To be displayed after setup/a game
def mainMenu(name):
    clearScreen()
    print(f'--- MAIN MENU ---\nHi, {name}!\n1 - New Game\n2 - Settings\n3 - Add Player\n4 - Quit')
    menuInput = False
    while not menuInput:
        try:
            choice = int(input(':: Enter an option: '))
            if not 1 <= choice <= 4:
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


def settings():
    clearScreen()
    print(f'--- SETTINGS ---\nChoose an option:\n1 - Configure Game Settings\n2 - Delete Player\n3 - Remove All Data\n4 - About')


# Run the initial launch sequence
# when the Python file is run
launch()


