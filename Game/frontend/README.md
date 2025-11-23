# Idle Game GUI Framework - Frontend Components

This document outlines the frontend GUI framework and its components for the idle game.

## Components

### 1. `main_window.py`

**Description:** The main application window and layout manager. It serves as the primary container for all other UI components.

**Content:**
```python
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Idle Game")
        self.geometry("800x600") # Default window size

        # Configure grid for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Main Frame ---
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def add_component(self, component, row, column, sticky="nsew", **grid_options):
        """
        Helper method to add UI components to the main frame.
        """
        component.grid(row=row, column=column, sticky=sticky, **grid_options)

if __name__ == "__main__":
    app = MainWindow()
    placeholder_label = ttk.Label(app.main_frame, text="Main Game Window - UI Components will be added here.")
    placeholder_label.grid(row=0, column=0, padx=20, pady=20)
    app.mainloop()
```

### 2. `resource_display.py`

**Description:** Visualizes the player's resources (e.g., gold, wood). Designed for real-time updates.

**Content:**
```python
# Game/frontend/resource_display.py

import tkinter as tk
from tkinter import ttk

class ResourceDisplay(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.resource_labels = {}
        self.resource_values = {}

    def add_resource(self, resource_name, initial_value=0):
        """Adds a new resource display label."""
        if resource_name not in self.resource_labels:
            row_num = len(self.resource_labels)
            
            name_label = ttk.Label(self, text=f"{resource_name.capitalize()}:")
            name_label.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
            
            value_label = ttk.Label(self, text=str(initial_value))
            value_label.grid(row=row_num, column=1, sticky="e", padx=5, pady=2)
            
            self.resource_labels[resource_name] = {
                "name": name_label,
                "value": value_label
            }
            self.resource_values[resource_name] = initial_value
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

    def update_resource(self, resource_name, new_value):
        """Updates the display for a specific resource."""
        if resource_name in self.resource_labels:
            self.resource_values[resource_name] = new_value
            self.resource_labels[resource_name]["value"].config(text=str(new_value))
        else:
            print(f"Warning: Resource '{resource_name}' not found. Adding it.")
            self.add_resource(resource_name, new_value)

    def update_resources(self, resources_data):
        """Updates multiple resources based on a dictionary."""
        for resource_name, value in resources_data.items():
            self.update_resource(resource_name, value)

    def get_resource_value(self, resource_name):
        """Returns the current value of a resource."""
        return self.resource_values.get(resource_name, None)
```

### 3. `upgrade_panel.py`

**Description:** Interface and controls for player upgrades.

**Content:**
```python
# Game/frontend/upgrade_panel.py

import tkinter as tk
from tkinter import ttk

class UpgradePanel(ttk.Frame):
    def __init__(self, parent, backend_api, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.backend_api = backend_api 

        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Upgrades", font=('Arial', 16, 'bold')).grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.upgrades_frame = ttk.Frame(self, padding="10")
        self.upgrades_frame.grid(row=1, column=0, sticky="nsew")
        self.upgrades_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.upgrades_frame, text="Available Upgrades will be listed here.").grid(row=0, column=0, pady=5)

    def refresh_upgrades(self):
        """Refreshes the display of available upgrades and their costs."""
        for widget in self.upgrades_frame.winfo_children():
            if widget.winfo_class() != "TLabel":
                widget.destroy()

        available_upgrades = [
            {"name": "Faster Production", "cost": 100, "level": 1, "id": "prod_speed_1"},
            {"name": "More Storage", "cost": 150, "level": 1, "id": "storage_1"},
        ]

        for i, upgrade in enumerate(available_upgrades):
            row_frame = ttk.Frame(self.upgrades_frame, relief="groove", borderwidth=1)
            row_frame.grid(row=i+1, column=0, pady=5, padx=5, sticky="ew")
            row_frame.grid_columnconfigure(2, weight=1)

            ttk.Label(row_frame, text=f"Level {upgrade['level']}:").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(row_frame, text=upgrade['name']).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            cost_label = ttk.Label(row_frame, text=f"Cost: {upgrade['cost']}")
            cost_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

            purchase_button = ttk.Button(row_frame, text="Buy", command=lambda u_id=upgrade['id'], u_cost=upgrade['cost']: self.purchase_upgrade(u_id, u_cost))
            purchase_button.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(self, text="Refresh Upgrades", command=self.refresh_upgrades).grid(row=2, column=0, pady=10)

    def purchase_upgrade(self, upgrade_id, cost):
        print(f"Attempting to purchase upgrade: {upgrade_id} with cost: {cost}")
        # TODO: Implement backend communication
        print(f"Simulated purchase of {upgrade_id}. Refreshing...")
        self.refresh_upgrades()
```

### 4. `game_controls.py`

**Description:** Provides Start/Stop, Save/Load controls.

**Content:**
```python
import tkinter as tk
from tkinter import ttk

class GameControls(ttk.Frame):
    def __init__(self, parent, game_logic_interface, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.game_logic = game_logic_interface

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.start_button = ttk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.stop_button = ttk.Button(self, text="Stop Game", command=self.stop_game)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.save_button = ttk.Button(self, text="Save Game", command=self.save_game)
        self.save_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.load_button = ttk.Button(self, text="Load Game", command=self.load_game)
        self.load_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    def start_game(self):
        print("Attempting to start game...")
        if hasattr(self.game_logic, 'start_game'):
            self.game_logic.start_game()
            print("Start game command sent.")
        else:
            print("Error: start_game method not found.")

    def stop_game(self):
        print("Attempting to stop game...")
        if hasattr(self.game_logic, 'stop_game'):
            self.game_logic.stop_game()
            print("Stop game command sent.")
        else:
            print("Error: stop_game method not found.")

    def save_game(self):
        print("Attempting to save game...")
        if hasattr(self.game_logic, 'save_game'):
            self.game_logic.save_game()
            print("Save game command sent.")
        else:
            print("Error: save_game method not found.")

    def load_game(self):
        print("Attempting to load game...")
        if hasattr(self.game_logic, 'load_game'):
            self.game_logic.load_game()
            print("Load game command sent.")
        else:
            print("Error: load_game method not found.")
```

### 5. `theme_manager.py`

**Description:** Manages visual themes and styling for the GUI.

**Content:**
```python
# theme_manager.py

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, style):
        self.style = style
        self.available_themes = {
            "default": "clam",
            "alt_default": "alt",
            "classic": "classic",
            "dark": "dark"
        }
        self.current_theme = None
        self.load_default_theme()

    def load_default_theme(self):
        self.apply_theme("default")

    def apply_theme(self, theme_name):
        if theme_name in self.available_themes:
            ttk_theme = self.available_themes[theme_name]
            try:
                self.style.theme_use(ttk_theme)
                self.current_theme = theme_name
                print(f"Theme applied: {theme_name} (ttk: {ttk_theme})")
                return True
            except tk.TclError:
                print(f"Warning: ttk theme '{ttk_theme}' not found. Using fallback.")
                try:
                    self.style.theme_use("clam")
                    self.current_theme = "default"
                    print("Fallback theme 'clam' applied.")
                    return True
                except tk.TclError:
                    print("Error: Fallback theme 'clam' also not found.")
                    return False
        else:
            print(f"Error: Theme '{theme_name}' not found. Available: {list(self.available_themes.keys())}")
            return False

    def add_custom_theme(self, name, ttk_theme_name):
        if name not in self.available_themes:
            self.available_themes[name] = ttk_theme_name
            print(f"Custom theme '{name}' added.")
        else:
            print(f"Warning: Theme '{name}' already exists. Overwriting.")
            self.available_themes[name] = ttk_theme_name

    def define_widget_style(self, style_name, widget_class, **options):
        try:
            self.style.configure(f"{style_name}.{widget_class}", **options)
            print(f"Defined style '{style_name}.{widget_class}'.")
        except Exception as e:
            print(f"Error defining style '{style_name}.{widget_class}': {e}")
```

### 6. `animation_system.py`

**Description:** Handles UI animations and visual effects.

**Content:**
```python
# Game Animation System

import tkinter as tk

class AnimationSystem:
    def __init__(self):
        pass

    def fade_in(self, widget, duration=500, start_opacity=0.0, end_opacity=1.0):
        print(f"Starting fade-in animation for {widget}...")
        widget.attributes('-alpha', end_opacity)
        print(f"Fade-in animation complete for {widget}.")

    def fade_out(self, widget, duration=500, start_opacity=1.0, end_opacity=0.0):
        print(f"Starting fade-out animation for {widget}...")
        widget.attributes('-alpha', end_opacity)
        print(f"Fade-out animation complete for {widget}.")

    def slide_in(self, widget, direction="left", duration=500, offset=50):
        print(f"Starting slide-in animation for {widget} from {direction}...")
        print(f"Slide-in animation complete for {widget}.")

    def slide_out(self, widget, direction="left", duration=500, offset=50):
        print(f"Starting slide-out animation for {widget} towards {direction}...")
        print(f"Slide-out animation complete for {widget}.")
```

---

## Collaboration Logs

**To Backend Agent:**
*   `Requesting API specifications and data structure details for the idle game GUI. Please provide information on how the frontend will interact with the backend for game state, resources, upgrades, etc.`

**To Integration Agent:**
*   `Frontend development is underway. Initial components main_window.py and resource_display.py are being developed. Requesting definition of component interfaces and dependencies for future integration.`

**To QA Agent:**
*   `Request code reviews for the following UI components: main_window.py, resource_display.py, upgrade_panel.py, game_controls.py, theme_manager.py, animation_system.py. Please ensure comprehensive testing of functionality, layout, and responsiveness.`

---

## Integration Points

*   **`MainWindow`**: Acts as the main container. Integrates other components using its grid layout and `add_component` method.
*   **`ResourceDisplay`**: Integrates into `MainWindow`. Expects data updates from backend/game state.
*   **`UpgradePanel`**: Integrates into `MainWindow`. Requires a `backend_api` object for interactions. Needs to refresh display based on backend data.
*   **`GameControls`**: Integrates into `MainWindow`. Requires a `game_logic_interface` for game actions (start, stop, save, load).
*   **`ThemeManager`**: Initialized with `ttk.Style`. Used by `MainWindow` and other components for theming.
*   **`AnimationSystem`**: Used by various components to apply visual effects. Integration depends on which components require animations.

---

## Performance Considerations

*   **`MainWindow`**: Ensure grid configurations are efficient for responsiveness. Avoid overly complex nested frames.
*   **`ResourceDisplay`**: Batch resource updates if performance becomes an issue with frequent updates.
*   **`UpgradePanel`**: Optimize dynamic widget creation/destruction for `refresh_upgrades`. Consider caching or more efficient update mechanisms.
*   **`AnimationSystem`**: Animations can be CPU-intensive. Use `widget.after()` for scheduling. The current fade animations rely on `-alpha`, which may have inconsistent support/performance. Profile complex animations.

---

## Code Review Feedback

*   No code review feedback has been received from the QA Agent yet. Feedback will be incorporated upon receipt.