# Game Save and Load System

import json
import os

class SaveSystem:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            print(f"Created save directory: {self.save_dir}")

    def save_game(self, game_state: dict, save_name: str = "autosave"):
        """Saves the current game state to a file.

        Args:
            game_state (dict): A dictionary representing the current state of the game.
                                This should include all necessary data like player progress,
                                inventory, settings, etc.
            save_name (str): The name of the save file (without extension).
        """
        file_path = os.path.join(self.save_dir, f"{save_name}.json")
        try:
            with open(file_path, 'w') as f:
                json.dump(game_state, f, indent=4)
            print(f"Game saved successfully to {file_path}")
            return True
        except IOError as e:
            print(f"Error saving game to {file_path}: {e}")
            return False
        except TypeError as e:
            print(f"Error serializing game state: {e}. Ensure all data is JSON serializable.")
            return False

    def load_game(self, save_name: str = "autosave") -> dict or None:
        """Loads the game state from a file.

        Args:
            save_name (str): The name of the save file to load (without extension).

        Returns:
            dict or None: The loaded game state as a dictionary, or None if the save file
                          does not exist or an error occurred.
        """
        file_path = os.path.join(self.save_dir, f"{save_name}.json")
        if not os.path.exists(file_path):
            print(f"Save file not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r') as f:
                game_state = json.load(f)
            print(f"Game loaded successfully from {file_path}")
            return game_state
        except IOError as e:
            print(f"Error loading game from {file_path}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}. The save file might be corrupted.")
            return None

    def list_saves(self) -> list:
        """Lists all available save files in the save directory.

        Returns:
            list: A list of save file names (without extensions).
        """
        saves = []
        try:
            for filename in os.listdir(self.save_dir):
                if filename.endswith(".json"):
                    saves.append(os.path.splitext(filename)[0])
            return saves
        except OSError as e:
            print(f"Error listing save files in {self.save_dir}: {e}")
            return []

    def delete_save(self, save_name: str) -> bool:
        """Deletes a specific save file.

        Args:
            save_name (str): The name of the save file to delete (without extension).

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        file_path = os.path.join(self.save_dir, f"{save_name}.json")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Save file {file_path} deleted successfully.")
                return True
            except OSError as e:
                print(f"Error deleting save file {file_path}: {e}")
                return False
        else:
            print(f"Save file not found: {file_path}")
            return False

# --- Frontend API Considerations ---
# The frontend agent will interact with this system by:
# 1. Requesting a list of available save files using `list_saves()`.
# 2. Initiating a save operation, providing the current game state (as a dictionary)
#    and a save name to `save_game(game_state, save_name)`.
# 3. Initiating a load operation, providing the save name to `load_game(save_name)`.
#    The loaded game state (dictionary) will then be used to reconstruct the game.
# 4. Potentially allowing players to delete save files using `delete_save(save_name)`.

# --- Example Usage (for testing) ---
# if __name__ == "__main__":
#     saver = SaveSystem()

#     # Example game state
#     current_game_data = {
#         "player": {
#             "name": "Hero",
#             "level": 5,
#             "exp": 150,
#             "position": [100, 250],
#             "inventory": ["sword", "potion", "key"]
#         },
#         "world": {
#             "current_map": "forest",
#             "time_of_day": "noon"
#         },
#         "settings": {
#             "volume": 0.8,
#             "graphics": "high"
#         }
#     }

#     # Save the game
#     if saver.save_game(current_game_data, "my_adventure"):
#         print("Save successful.")
#     else:
#         print("Save failed.")

#     # List saves
#     print("Available saves:", saver.list_saves())

#     # Load the game
#     loaded_data = saver.load_game("my_adventure")
#     if loaded_data:
#         print("Loaded game data:", loaded_data)
#         # In a real game, you would now use loaded_data to set the game's state
#         # e.g., self.player.load(loaded_data['player'])
#     else:
#         print("Load failed.")
        
#     # Delete a save
#     # if saver.delete_save("my_adventure"):
#     #     print("Delete successful.")
#     # else:
#     #     print("Delete failed.")
#     # print("Available saves after deletion:", saver.list_saves())
