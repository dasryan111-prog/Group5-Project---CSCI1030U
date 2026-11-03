from item import Item

class Inventory:
    def __init__(self, items=None):
        if items is not None:
            self.items = items
        else:
            self.items = []

    # Adds an item to the inventory
    def add_item(self, item):
        self.items.append(item)

    # Removes an item from the inventory
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    # Counts the number of items in the inventory using recursion
    def count_items(self, index=0):
        if index >= len(self.items):
            return 0
        return 1 + self.count_items(index + 1)

    # Displays all items in the inventory
    def display_inventory(self):
        if self.count_items() == 0:
            print("Your inventory is empty.")
            return
        for item in self.items:
            print(item.name + ": " + item.description)

    # Converts the inventory into a dictionary for saving
    def to_dict(self):
        inventory_data = []
        for item in self.items:
            inventory_data.append(item.to_dict())
        return {"items": inventory_data}

    # Loads inventory data from a dictionary
    def from_dict(self, data):
        self.items = []
        for item_data in data["items"]:
            item = Item("", "", "", 0)
            item.from_dict(item_data)
            self.items.append(item)