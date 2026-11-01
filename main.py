import argparse
import os

from player import Player
player = Player()

"""Entry point for the group project.

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
        "east": "office"
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
    "health_potion": {
        "description": "Restores 25 health.",
        "type": "healing",
        "value": 25
    },
    "sword": {
        "description": "A sharp sword that increases damage.",
        "type": "weapon",
        "value": 5
    }
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
    current_room = rooms[player["current_room"]]
    print("\nCurrent room:", player["current_room"])
    print("Available Directions:")

    for choice in current_room:
        print(choice[0].upper() + " - " + choice)
    direction = input("Choose the direction you wish to move (N/S/E/W): ").strip().lower()

    directions = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west"
    }

    # Checks if the direction actually exists

    if direction in directions:
        direction = directions[direction]

        if direction in current_room:
            new_room = current_room[direction]
            player.move_to(new_room)
        else:
            print("You can't go that way!")
    else:
        print("Invalid direction.")

def display_inventory():
    print("\nInventory:")
    if len(player.inventory) == 0:
        print("Your inventory is empty")
        return
    for item in player.inventory:
        print(item + ": " + items[item]["description"])

def pick_up_item():
    available_items = room_items[player.current_room]
    if len(available_items) == 0:
        print("There are no items in this room.")
        return
    print("\nItems in this room:")
    for item in available_items:
        print(item + ": " + items[item]["description"])
    choice = input("Enter the name of an item to pick up, or press Enter to skip: ").lower()
    if choice in available_items:
        player.inventory.append(choice)
        available_items.remove(choice)
        print("You picked up the", choice + ".")
    else:
        print("That item is not in this room.")

def use_item():
    if len(player.inventory) == 0:
        print("\nYour inventory is empty.")
        return
    display_inventory()
    choice = input("Enter the name of an item to use, or press Enter to cancel: ").lower()
    if choice == "":
        return
    if choice not in player.inventory:
        print("You do not have that item.")
        return
    item = items[choice]
    if item["type"] == "healing":
        if player.health >= 100:
            print("Your health is already full.")
            return
        player.heal(item["value"])
        if player.health > 100:
            player.health = 100
        player.inventory.remove(choice)
        print("You used the " + choice + ".")
        print(f"Your health is now {player.health}")
    elif item["type"] == "weapon":
        player.attack_damage += item["value"]
        player.inventory.remove(choice)
        print("You equipped the " + choice + ".")
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
        print("\n Mansion Explorer\n")
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
    player.inventory.clear()
    player.visited_rooms.clear()
    player.visited_rooms.append("entrance")

    room_items["bedroom"] = ["sword"]
    room_items["bathroom"] = ["health_potion"]
    room_items["library"] = ["health_potion"]

def main():

    parser = argparse.ArgumentParser(description="Mansion Explorer")

    parser.add_argument("--load", action="store_true", help="Load a saved game when starting")
    parser.add_argument("--status", action="store_true", help="Display save information")

    args = parser.parse_args()

    # Displays status
    if args.status:
        try:
            player.load_from_file(room_items)
            player.status()
            
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
            print("You were caught out by a sudden trap. You lose.")

            play_again = input("Press 'y' to play again, and anything else to quit: ").lower().strip()
            if play_again == 'y':
                reset_game()
            else:
                game_on = False
                print("Thanks for playing")

        elif player.current_room == "tunnel":
            print("You escaped, congratulations!")
            play_again = input("Press 'y' to play again, and anything else to quit: ").lower().strip()
            if play_again == 'y':
                reset_game()
            else:
                game_on = False
                print("Thanks for playing")
        else:
            move_player()

            if player.current_room != "office" and player.current_room != "dark_room" and player.current_room != "tunnel":
                
                if item_menu():
                    game_on = False
                

if __name__ == '__main__':
    main()