# theme_manager.py

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, style):
        """
        Initializes the ThemeManager with a ttk.Style object.

        Args:
            style (ttk.Style): The ttk.Style object to manage themes for.
        """
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
        """Loads the default theme ('clam') upon initialization."""
        self.apply_theme("default")

    def apply_theme(self, theme_name):
        """
        Applies a specified theme to the GUI.

        Args:
            theme_name (str): The name of the theme to apply (e.g., 'default', 'dark').

        Returns:
            bool: True if the theme was applied successfully, False otherwise.
        """
        if theme_name in self.available_themes:
            ttk_theme = self.available_themes[theme_name]
            try:
                self.style.theme_use(ttk_theme)
                self.current_theme = theme_name
                print(f"Theme applied: {theme_name} (ttk: {ttk_theme})")
                return True
            except tk.TclError:
                print(f"Warning: ttk theme '{ttk_theme}' not found. Using fallback.")
                # Fallback to a known theme if the requested one is not available
                try:
                    self.style.theme_use("clam")
                    self.current_theme = "default"
                    print("Fallback theme 'clam' applied.")
                    return True
                except tk.TclError:
                    print("Error: Fallback theme 'clam' also not found. Styling may be inconsistent.")
                    return False
        else:
            print(f"Error: Theme '{theme_name}' not found. Available themes: {list(self.available_themes.keys())}")
            return False

    def add_custom_theme(self, name, ttk_theme_name):
        """
        Adds a new custom theme to the available themes.

        Args:
            name (str): The internal name for the custom theme.
            ttk_theme_name (str): The actual ttk theme name to use.
        """
        if name not in self.available_themes:
            self.available_themes[name] = ttk_theme_name
            print(f"Custom theme '{name}' added, mapping to ttk theme '{ttk_theme_name}'.")
        else:
            print(f"Warning: Theme '{name}' already exists. Overwriting.")
            self.available_themes[name] = ttk_theme_name

    def define_widget_style(self, style_name, widget_class, **options):
        """
        Defines or modifies a specific widget style.

        Args:
            style_name (str): The name of the style to define (e.g., 'Game.TButton').
            widget_class (str): The widget class this style applies to (e.g., 'TButton').
            **options: Style configuration options (e.g., foreground, background, font).
        """
        try:
            self.style.configure(f"{style_name}.{widget_class}", **options)
            print(f"Defined style '{style_name}.{widget_class}' with options: {options}")
        except Exception as e:
            print(f"Error defining style '{style_name}.{widget_class}': {e}")

# --- Example Usage --- (This would typically be integrated into the main application setup)
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Theme Manager Demo")
#     style = ttk.Style(root)
#
#     theme_manager = ThemeManager(style)
#
#     # Add a custom theme (assuming 'vista' is available on the system)
#     # theme_manager.add_custom_theme("vista_like", "vista")
#
#     # Define a custom style for buttons
#     theme_manager.define_widget_style("GameButton", "TButton",
#                                       foreground="#FFFFFF",
#                                       background="#4CAF50",
#                                       font=("Helvetica", 12, "bold"))
#
#     # Create some widgets to test styling
#     label = ttk.Label(root, text="Welcome to the Game!")
#     label.pack(pady=10)
#
#     # Using the custom style for a button
#     # Note: To use 'GameButton.TButton', you need to explicitly use it when creating the widget:
#     # custom_button = ttk.Button(root, text="Custom Styled Button", style="GameButton.TButton")
#     # For demonstration, let's just use a standard button and switch themes.
#     button = ttk.Button(root, text="Click Me")
#     button.pack(pady=5)
#
#     # Example of switching themes
#     def switch_theme(theme_name):
#         theme_manager.apply_theme(theme_name)
#         # Re-apply custom styles if they depend on the theme, or if they were overridden
#         theme_manager.define_widget_style("GameButton", "TButton",
#                                           foreground="#FFFFFF",
#                                           background="#4CAF50",
#                                           font=("Helvetica", 12, "bold"))
#         # Update button style if it was created before theme switch
#         button.configure(style=f"{theme_manager.current_theme}.TButton") # This might not work as expected for custom styles, often requires re-creation or specific handling
#         print(f"Current button style: {button.cget('style')}")
#
#     theme_buttons_frame = ttk.Frame(root)
#     theme_buttons_frame.pack(pady=10)
#
#     for theme in theme_manager.available_themes:
#         btn = ttk.Button(theme_buttons_frame, text=f"Use {theme.capitalize()} Theme", command=lambda t=theme: switch_theme(t))
#         btn.pack(side=tk.LEFT, padx=5)
#
#     root.mainloop()
