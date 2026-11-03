import json
from inventory import Inventory

# Player class that stores all player related data
class Player:
    def __init__(self, health = 100, attack_damage = 5, current_room = "entrance", visited_rooms = None, inventory = None):
        self.health = health
        self.attack_damage = attack_damage

        # Checks inventory and provides it with the according values
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory()
        self.current_room = current_room

        # Checks visited rooms and provides it with the according values
        if visited_rooms is not None:
            self.visited_rooms = visited_rooms
        else:
            self.visited_rooms = []
        if self.current_room not in self.visited_rooms:
            self.visited_rooms.append(self.current_room)

    def to_dict(self):
        return {
            "health": self.health,
            "attack_damage": self.attack_damage,
            "current_room": self.current_room,
            "inventory": self.inventory.to_dict(),
            "visited_rooms": self.visited_rooms,
        }

    def save_to_file(self, room_items):
        save_data = self.to_dict()
        save_data["room_items"] = room_items
        with open("player_save.json", "w") as file:
            json.dump(save_data, file)

    def load_from_file(self, room_items):
        with open("player_save.json", "r") as file:
            data = json.load(file)
        self.health = data["health"]
        self.attack_damage = data["attack_damage"]
        self.current_room = data["current_room"]
        self.inventory = Inventory()
        self.inventory.from_dict(data["inventory"])
        self.visited_rooms = data["visited_rooms"]
        if "room_items" in data:
            for room in room_items:
                if room in data["room_items"]:
                    room_items[room] = data["room_items"][room]

    # Applies the damage to the player
    def take_damage(self, damage):
        self.health -= damage

    # Heals the player - doesn't have to regulate health being over 100, that is done in the main game
    def heal(self, heal_amount):
        self.health += heal_amount

    # Checks if the player's health is above 0
    def is_alive(self):
        return self.health > 0

    # Checks if a certain room has already been visited
    def has_visited_room(self, room_name, index = 0):
        if index >= len(self.visited_rooms):
            return False
        if self.visited_rooms[index] == room_name:
            return True
        return self.has_visited_room(room_name, index + 1)

    # Informs the user if they have visited a room before
    def move_to(self, new_room):
        already_visited = self.has_visited_room(new_room)
        self.current_room = new_room
        if already_visited:
            print(f"You have visited this room before")
        else:
            self.visited_rooms.append(new_room)

    # Prints the player's status
    def status(self):
        print("\nPlayer Status")
        print(f"Health: {self.health}")
        print(f"Attack damage: {self.attack_damage}")
        print(f"Current room: {self.current_room}")
        print(f"Rooms visited: {self.visited_rooms}")