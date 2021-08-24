import json

# Check if setup needs to be run.
# Else, present the main menu.
def launch():


def setup() :
    print('--- WELCOME TO MUSIC QUIZ! ---\nReady to test your music knowledge?\n\n')
    print('To set up your profile, we need a name and PIN code from you. This will keep your progress private so only you can play Music Quiz.')
    createProfile()

def createProfile():
    name = input('Enter your name: ')
    pinSet = False
    while not pinSet:
        try:
            pin = int(input('Enter a 4-digit PIN code: '))
            if (len(str(pin))) != 4:
                print('Your code wasn\'t 4 digits. Try again.')
            else:
                pinSet = True
        except:
            print('You didn\'t enter a valid PIN code. Try again.')
    
    print(f'Welcome, {name}! Let\'s get you into your first game.')

def mainMenu(name):
    print(f'--- MAIN MENU ---\nHi, {name}!\nChoose a playlist:\n1 - Pop\n2 - Alternative\n3 - Rock')

setup()

