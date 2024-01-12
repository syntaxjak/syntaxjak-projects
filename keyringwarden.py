import keyring
import random


# List of preprogrammed responses
responses = [
    "Welcome, sire, your keyrings:",
    "Yes sire, your keys are here",
    "Hail my sire, I have your keys as you requested",
    "Salutations, sire, I was not sleeping, here is your keyring"
]

# Randomly select a response
response = random.choice(responses)

def add_key():
    service = input("Enter service: ")
    name = input("Enter name: ")
    key = input("Enter key: ")
    keyring.set_password(service, name, key)
    print("Your key has been saved!")

def remove_key():
    service = input("Enter service: ")
    name = input("Enter name: ")
    try:
        keyring.delete_password(service, name)
        print("Your key has been removed!")
    except keyring.errors.PasswordDeleteError:
        print("The specified key was not found!")

def list_keys():
    print("Your key-ring:")
    # ... replace all occurences of yourkeyname with your keys name and yourservice with your services name...
    
    #yourkeyname = keyring.get_password("yourservice", "yourkeyname")
    #print("\tyourkeynames:" , yourkeyname)


while True:
    print(f'\nThe Keyring Warden greets you: "{response}"')
    print("1. Add a new key")
    print("2. Remove an existing key")
    print("3. List keys")
    print("4. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_key()
    elif choice == "2":
        remove_key()
    elif choice == "3":
        list_keys()
    elif choice == "4":
        print("Leaving The Keyring Warden.")
        break
    else:
        print("Invalid choice.")
