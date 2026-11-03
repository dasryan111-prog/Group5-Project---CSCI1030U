import argparse
import os
from player import Player
from item import Item
player = Player()

"""
Entry point for the group project.
`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward. Replace the placeholder below with your own core loop.
"""

# Rooms
rooms = {
    "entrance":{
        "north": "foyer",
    },
    "foyer": {
        "north": "lounge",
        "south": "entrance",
        "east": "kitchen",
        "west": "bedroom"
    },
    "lounge": {
        "north": "bathroom",
        "south": "foyer"
    },
    "kitchen": {
        "east": "dining_room",
        "west": "foyer"
    },
    "bedroom": {
        "east": "foyer",
        "west": "closet"
    },
    "bathroom": {
        "north": "dark_room",
        "south": "lounge"
    },
    "dining_room": {
        "north": "library",
        "south": "theatre",
        "east": "office",
        "west": "kitchen"
    },
    "closet": {
        "east": "bedroom"
    },
    # This is a trap room - entering should result in an instant loss
    "dark_room": {
        "south": "bathroom"
    },
    "library": {
        "north": "tunnel",
        "south": "dining_room"
    },
    "theatre": {
        "north": "dining_room"
    },
    # This is another trap room - entering will result in an instant loss
    "office": {
        "west": "dining_room"
    },
    # This is the exit - entering will win the game
    "tunnel": {
        "south": "library"
    }
}

items = {
    "health_potion": Item("health_potion", "Restores 25 health.", "healing", 25),
    "sword": Item("sword", "A sharp sword that increases damage.", "weapon", 5)
}

room_items = {
    "entrance": [],
    "foyer": [],
    "lounge": [],
    "kitchen": [],
    "bedroom": ["sword"],
    "bathroom": ["health_potion"],
    "dining_room": [],
    "closet": [],
    "dark_room": [],
    "library": ["health_potion"],
    "theatre": [],
    "office": [],
    "tunnel": []
}

# Handles player movement
def move_player():
    current_room = rooms[player.current_room]
    print("\nCurrent room:", player.current_room)
    print("Available Directions:")
    directions = {"1": "north", "2": "south", "3": "east", "4": "west"}
    valid_choices = []
    for number, direction in directions.items():
        if direction in current_room:
            print(number + " - " + direction.capitalize())
            valid_choices.append(number)
    direction = input("Choose a direction (enter its number): ").strip()
    # Checks if the direction actually exists
    if direction in directions:
        direction = directions[direction]
        if direction in current_room:
            new_room = current_room[direction]
            player.move_to(new_room)
            print("\nYou moved to:", player.current_room)
        else:
            print("You can't go that way!")
    else:
        print("Invalid direction.")

def display_inventory():
    print("\nInventory:")
    player.inventory.display_inventory()

def pick_up_item():
    available_items = room_items[player.current_room]
    if len(available_items) == 0:
        print("There are no items in this room.")
        return
    print("\nItems in this room:")
    for index, item in enumerate(available_items, start=1):
        print(str(index) + " - " + item + ": " + items[item].description)
    print("0 - Cancel")
    choice = input("Choose an item by number: ").strip()
    valid_choices = []
    for number in range(0, len(available_items) + 1):
        valid_choices.append(str(number))
    if choice in valid_choices:
        choice = int(choice)
        if choice == 0:
            return
        selected_item = available_items[choice - 1]
        player.inventory.add_item(items[selected_item])
        available_items.remove(selected_item)
        print("You picked up the", selected_item + ".")
    else:
        print("Invalid option.")

def use_item():
    if player.inventory.count_items() == 0:
        print("\nYour inventory is empty.")
        return
    print("\nItems in your inventory:")
    for index, item in enumerate(player.inventory.items, start=1):
        print(str(index) + " - " + item.name)
    print("0 - Cancel")
    choice = input("Choose an item to use by number: ").strip()
    valid_choices = []
    for number in range(0, len(player.inventory.items) + 1):
        valid_choices.append(str(number))
    if choice in valid_choices:
        choice = int(choice)
        if choice == 0:
            return
        item = player.inventory.items[choice - 1]
    else:
        print("Invalid option.")
        return
    if item.item_type == "healing":
        if player.health >= 100:
            print("Your health is already full.")
            return
        player.heal(item.value)
        if player.health > 100:
            player.health = 100
        player.inventory.remove_item(item)
        print("You used the " + item.name + ".")
        print(f"Your health is now {player.health}")
    elif item.item_type == "weapon":
        player.attack_damage += item.value
        player.inventory.remove_item(item)
        print("You equipped the " + item.name + ".")
        print(f"Your attack damage is now {player.attack_damage}")

def item_menu():
    while True:
        print("\nItem Menu\n1. View inventory\n2. Pick up an item\n3. Use an item\n4. Player Menu\n5. Return to exploration\n6. Save and quit game")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            display_inventory()
        elif choice == "2":
            pick_up_item()
        elif choice == "3":
            use_item()
        elif choice == "4":
            player_menu()
        elif choice == "5":
            return False
        elif choice == "6":
            player.save_to_file(room_items)
            print("Game saved.")
            return True
        else:
            print("Invalid option.")

# The main menu
def player_menu():
    while True:
        print("\n ------ Player Menu -----")
        print("1. View Player Status")
        print("2. Save game")
        print("3. Load game")
        print("4. Return to game")
        option = input("Choose an option (1-4): ").strip()
        # Displays the player's status
        if option == "1":
            player.status()
        # Saves the game
        elif option == "2":
            player.save_to_file(room_items)
            print("Game saved succesfully.")
        # Loads a game
        elif option == "3":
            try:
                player.load_from_file(room_items)
                print("Game loaded successfully")
            except FileNotFoundError:
                print("No save file found")
        # Exits the menu
        elif option == "4":
            break
        else:
            print("Invalid option")

def opening_screen():
    while True:
        print("\nMansion Explorer\n")
        print("1. Start new game")
        print("2. Load saved game")
        print("3. Quit")
        option = input("Choose an option (1-3): ").strip()
        if option == "1":
            reset_game()
            print("\nStarting new game")
            return True
        elif option == "2":
            try:
                player.load_from_file(room_items)
                print("\nGame loaded successfully!")
                return True
            except FileNotFoundError:
                print("\nNo save file found")
        elif option == "3":
            print("Thanks for playing!")
            return False
        else:
            print("Invalid choice")

def delete_save():
    try:
        os.remove("player_save.json")
    except FileNotFoundError:
        pass

def reset_game():
    delete_save()
    player.health = 100
    player.attack_damage = 5
    player.current_room = "entrance"
    player.inventory.items.clear()
    player.visited_rooms.clear()
    player.visited_rooms.append("entrance")
    room_items["bedroom"] = ["sword"]
    room_items["bathroom"] = ["health_potion"]
    room_items["library"] = ["health_potion"]

# Gives the player options after winning or losing
def end_game_menu():
    while True:
        print("\nWhat would you like to do?")
        print("1. Load saved game")
        print("2. Start a new game")
        print("3. Quit")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            try:
                player.load_from_file(room_items)
                print("\nSaved game loaded successfully!")
                return True
            except FileNotFoundError:
                print("\nNo save file found. Please choose another option.")
        elif choice == "2":
            reset_game()
            print("\nStarting a new game.")
            return True
        elif choice == "3":
            print("Thanks for playing!")
            return False
        else:
            print("Invalid option.")

def main():
    parser = argparse.ArgumentParser(description="Mansion Explorer")
    parser.add_argument("-l", "--load", action="store_true", help="Load a saved game when starting")
    parser.add_argument("-s", "--status", action="store_true", help="Display save information")
    parser.add_argument("-i", "--inventory", action="store_true", help="Display the saved inventory")
    args = parser.parse_args()
    # Displays status
    if args.status:
        try:
            player.load_from_file(room_items)
            player.status()
        except FileNotFoundError:
            print("No save found")
        return
    if args.inventory:
        try:
            player.load_from_file(room_items)
            player.inventory.display_inventory()
        except FileNotFoundError:
            print("No save found")
        return
    if args.load:
        try:
            player.load_from_file(room_items)
            print("Game loaded sucessfully.")
            game_started = True
        except FileNotFoundError:
            print("No save found, creating a new game.")
            game_started = opening_screen()
    else:
        game_started = opening_screen()
    if not game_started:
        return
    game_on = True
    while game_on:
        if player.current_room == "office" or player.current_room == "dark_room":
            print("\nYou were caught out by a sudden trap. You lose.")
            game_on = end_game_menu()
        elif player.current_room == "tunnel":
            print("You escaped, congratulations!")
            game_on = end_game_menu()
        else:
            move_player()
            if player.current_room not in ["office", "dark_room", "tunnel"]:
                if item_menu():
                    game_on = False

if __name__ == '__main__':
    main()