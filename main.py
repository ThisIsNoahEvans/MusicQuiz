import json

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
    
    print(f'Welcome, {name}! Let\'s get you into your first game.')

# The main menu
# To be displayed after setup/a game
def mainMenu(name):
    print(f'--- MAIN MENU ---\nHi, {name}!\nChoose a playlist:\n1 - Pop\n2 - Alternative\n3 - Rock')

# Run the initial launch sequence
# when the Python file is run
launch()

