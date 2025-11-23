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
        # This frame will hold all other UI components.
        # It allows for easier management of layout and theming.
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid within the main frame
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Placeholder for other UI Components ---
        # Examples:
        # self.resource_display = ResourceDisplay(self.main_frame)
        # self.resource_display.grid(row=0, column=0, sticky="nsew")
        # 
        # self.action_panel = ActionPanel(self.main_frame)
        # self.action_panel.grid(row=0, column=1, sticky="nsew")

        # --- Theme Integration ---
        # Styles can be applied here or loaded from a separate theme file.
        # Example:
        # style = ttk.Style()
        # style.theme_use("clam") # or other themes like 'default', 'alt', 'classic'
        # You might want to define custom styles for game elements.

    def add_component(self, component, row, column, sticky="nsew", **grid_options):
        """
        Helper method to add UI components to the main frame.
        Ensures components are managed within the main_frame's grid.
        """
        component.grid(row=row, column=column, sticky=sticky, **grid_options)
        # Configure row/column weights for the component's grid if needed by the component itself
        # For example, if component is a Frame:
        # component.grid_rowconfigure(0, weight=1)
        # component.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = MainWindow()
    # Example of adding a placeholder label
    placeholder_label = ttk.Label(app.main_frame, text="Main Game Window - UI Components will be added here.")
    placeholder_label.grid(row=0, column=0, padx=20, pady=20)

    app.mainloop()
