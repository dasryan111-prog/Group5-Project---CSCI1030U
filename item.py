# Item class that stores information about individual items
class Item:
    def __init__(self, name, description, item_type, value):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.value = value

    # Converts the item into a dictionary for saving
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type,
            "value": self.value
        }

    # Loads item data from a dictionary
    def from_dict(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.item_type = data["item_type"]
        self.value = data["value"]