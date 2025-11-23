import tkinter as tk
from tkinter import ttk

class GameControls(ttk.Frame):
    def __init__(self, parent, game_logic_interface, *args, **kwargs):
        """
        GameControls frame containing buttons for game interaction.

        Args:
            parent: The parent widget.
            game_logic_interface: An object that provides methods to interact with the game's backend logic
                                  (e.g., start_game, stop_game, save_game, load_game).
            *args, **kwargs: Additional arguments for the ttk.Frame.
        """
        super().__init__(parent, *args, **kwargs)
        self.game_logic = game_logic_interface

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # --- Game Control Buttons ---
        self.start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.stop_button = ttk.Button(self, text="Stop Game", command=self.stop_game)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.save_button = ttk.Button(self, text="Save Game", command=self.save_game)
        self.save_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.load_button = ttk.Button(self, text="Load Game", command=self.load_game)
        self.load_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    def start_game(self):
        """Initiates the game start process via the game logic interface."""
        print("Attempting to start game...")
        if hasattr(self.game_logic, 'start_game'):
            self.game_logic.start_game()
            print("Start game command sent.")
        else:
            print("Error: start_game method not found in game_logic_interface.")

    def stop_game(self):
        """Initiates the game stop process via the game logic interface."""
        print("Attempting to stop game...")
        if hasattr(self.game_logic, 'stop_game'):
            self.game_logic.stop_game()
            print("Stop game command sent.")
        else:
            print("Error: stop_game method not found in game_logic_interface.")

    def save_game(self):
        """Initiates the game save process via the game logic interface."""
        print("Attempting to save game...")
        if hasattr(self.game_logic, 'save_game'):
            self.game_logic.save_game()
            print("Save game command sent.")
        else:
            print("Error: save_game method not found in game_logic_interface.")

    def load_game(self):
        """Initiates the game load process via the game logic interface."""
        print("Attempting to load game...")
        if hasattr(self.game_logic, 'load_game'):
            self.game_logic.load_game()
            print("Load game command sent.")
        else:
            print("Error: load_game method not found in game_logic_interface.")

# --- Example Usage (for demonstration within a hypothetical main window) ---
if __name__ == "__main__":
    # This is a mock game logic interface for demonstration purposes.
    # In a real application, this would be an instance of your GameEngine or similar.
    class MockGameLogic:
        def start_game(self):
            print("MockGameLogic: Game started!")
        def stop_game(self):
            print("MockGameLogic: Game stopped.")
        def save_game(self):
            print("MockGameLogic: Game saved.")
        def load_game(self):
            print("MockGameLogic: Game loaded.")

    root = tk.Tk()
    root.title("Game Controls Demo")
    root.geometry("400x100")

    mock_logic = MockGameLogic()
    controls_frame = GameControls(root, mock_logic, relief=tk.RAISED, borderwidth=2)
    controls_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()