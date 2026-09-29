"""Entry point for the group project.

`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward. Replace the placeholder below with your own core loop.
"""

game_on = True

player = {
    "health": 100,
    "attack_damage": 5,
    "current_room": "entrance"
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

def move_player():
    current_room = rooms[player["current_room"]]
    print("\nCurrent room:", player["current_room"])
    print("Available Directions: \n")
    for choice in current_room:
        print(choice)
    direction = input("Choose the direction you wish to move: ").lower()
    if direction in current_room:
        player["current_room"] = current_room[direction]
    else:
        print("You can't go that way!")

def main():
    game_on = True
    while game_on:
        move_player()
        if player["current_room"] == "office" or player["current_room"] == "dark_room":
            print("You were caught out by a sudden trap. You lose.")
            play_again = input("Press 'y' to play again, and anything else to quit")
            if play_again == 'y':
                game_on = True
                player["current_room"] = "entrance"
            else:
                game_on = False
                print("Thanks for playing")
        elif player["current_room"] == "tunnel":
            print("You escaped, congratulations!")
            play_again = input("Press 'y' to play again, and anything else to quit")
            if play_again == 'y':
                game_on = True
                player["current_room"] = "entrance"
            else:
                game_on = False
                print("Thanks for playing")


if __name__ == '__main__':
    main()
