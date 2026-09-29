"""Entry point for the group project.

`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward. Replace the placeholder below with your own core loop.
"""

game_on = True

player = {
    "health": 100,
    "attack_damage": 5,
    "current_room": "entrance",
    "inventory": []
}

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

def move_player():
    current_room = rooms[player["current_room"]]
    print("\nCurrent room:", player["current_room"])
    print("Available Directions:")
    for choice in current_room:
        print(choice)
    direction = input("Choose the direction you wish to move: ").lower()
    if direction in current_room:
        player["current_room"] = current_room[direction]
    else:
        print("You can't go that way!")

def display_inventory():
    print("\nInventory:")
    if len(player["inventory"]) == 0:
        print("Your inventory is empty")
        return
    for item in player["inventory"]:
        print(item + ": " + items["description"])

def pick_up_item():
    available_items = room_items[player["current_room"]]
    if len(available_items) == 0:
        print("There are no items in this room.")
        return
    print("\nItems in this room:")
    for item in available_items:
        print(item + ": " + items[item]["description"])
    choice = input("Enter the name of an item to pick up, or press Enter to skip: ").lower()
    if choice in available_items:
        player["inventory"].append(choice)
        available_items.remove(choice)
        print("You picked up the", choice + ".")
    else:
        print("That item is not in this room.")

def use_item():
    if len(player["inventory"]) == 0:
        print("\nYour inventory is empty.")
        return
    display_inventory()
    choice = input("Enter the name of an item to use, or press Enter to cancel: ").lower()
    if choice == "":
        return
    if choice not in player["inventory"]:
        print("You do not have that item.")
        return
    item = items[choice]
    if item["type"] == "healing":
        if player["health"] >= 100:
            print("Your health is already full.")
            return
        player["health"] += item["value"]
        if player["health"] > 100:
            player["health"] = 100
        player["inventory"].remove(choice)
        print("You used the " + choice + ".")
        print("Your health is now " + player["health"])
    elif item["type"] == "weapon":
        player["attack_damage"] += item["value"]
        player["inventory"].remove(choice)
        print("You equipped the " + choice + ".")
        print("Your attack damage is now " + player["attack_damage"])

def item_menu():
    while True:
        print("\nItem Menu\n1. View inventory\n2. Pick up an item\n3. Use an item\n4. Return to exploration")
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            display_inventory()
        elif choice == "2":
            pick_up_item()
        elif choice == "3":
            use_item()
        elif choice == "4":
            break
        else:
            print("Invalid option.")

def reset_game():
    player["health"] = 100
    player["attack_damage"] = 5
    player["current_room"] = "entrance"
    player["inventory"].clear()
    room_items["bedroom"] = ["sword"]
    room_items["bathroom"] = ["health_potion"]
    room_items["library"] = ["health_potion"]

def main():
    game_on = True
    while game_on:
        move_player()
        if player["current_room"] == "office" or player["current_room"] == "dark_room":
            print("You were caught out by a sudden trap. You lose.")
            play_again = input("Press 'y' to play again, and anything else to quit: ").lower()
            if play_again == 'y':
                reset_game()
            else:
                game_on = False
                print("Thanks for playing")
        elif player["current_room"] == "tunnel":
            print("You escaped, congratulations!")
            play_again = input("Press 'y' to play again, and anything else to quit: ").lower()
            if play_again == 'y':
                reset_game()
            else:
                game_on = False
                print("Thanks for playing")
        else:
            item_menu()

if __name__ == '__main__':
    main()