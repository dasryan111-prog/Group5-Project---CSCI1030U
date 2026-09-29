The player and movement slice focuses on the basic player and its movement throughout the dungeon. The data required for this slice consists of player health, player attack damage, the current room, the adjacent rooms, and room descriptions.
Steps:
1. Create the player with base statistics
2. Create rooms / dungeon layout
3. Display the player's current room and adjacent rooms
4. Ask the player what room they wish to enter
5. Check if the direction is valid
6. Move the player into the room
7. Repeat steps 3-6 until the player loses or escapes

The items and inventory slice focuses on the items that the player can find throughout the mansion and the ability of the player to collect and use those items. The data required for this slice consists of the player's inventory, item information, item types, item effects, and the items available in each room.
Steps:
1. Create the player's inventory as an empty list
2. Create the items and their information
3. Place items in different rooms
4. Display the item menu after the player enters a room
5. Allow the player to view their inventory
6. Check if the current room contains any items
7. Allow the player to pick up an available item
8. Add the selected item to the player's inventory
9. Remove the picked-up item from the room
10. Allow the player to use an item from their inventory
11. Apply the item's effect to the player
12. Remove the item from the inventory when it is used
13. Return the player to exploration
14. Repeat steps 4-13 until the game ends