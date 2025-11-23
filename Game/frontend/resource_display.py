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
            
            # Resource Name Label
            name_label = ttk.Label(self, text=f"{resource_name.capitalize()}:")
            name_label.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
            
            # Resource Value Label
            value_label = ttk.Label(self, text=str(initial_value))
            value_label.grid(row=row_num, column=1, sticky="e", padx=5, pady=2)
            
            self.resource_labels[resource_name] = {
                "name": name_label,
                "value": value_label
            }
            self.resource_values[resource_name] = initial_value
            
            # Configure column weights for alignment
            self.grid_columnconfigure(0, weight=1) # Name column expands less
            self.grid_columnconfigure(1, weight=1) # Value column expands more

    def update_resource(self, resource_name, new_value):
        """Updates the display for a specific resource."""
        if resource_name in self.resource_labels:
            self.resource_values[resource_name] = new_value
            self.resource_labels[resource_name]["value"].config(text=str(new_value))
        else:
            print(f"Warning: Resource '{resource_name}' not found. Adding it.")
            self.add_resource(resource_name, new_value)

    def update_resources(self, resources_data):
        """Updates multiple resources based on a dictionary of resource_name: value."""
        for resource_name, value in resources_data.items():
            self.update_resource(resource_name, value)

    def get_resource_value(self, resource_name):
        """Returns the current value of a resource."""
        return self.resource_values.get(resource_name, None)

# --- Example Usage (for demonstration) ---
# if __name__ == '__main__':
#     root = tk.Tk()
#     root.title("Resource Display Example")
#     
#     resource_display_frame = ResourceDisplay(root, relief=tk.RIDGE, borderwidth=2)
#     resource_display_frame.pack(padx=10, pady=10, fill=tk.X)
#     
#     # Add some resources
#     resource_display_frame.add_resource("gold", 100)
#     resource_display_frame.add_resource("wood", 50)
#     resource_display_frame.add_resource("energy", 75)
#     
#     # Simulate updates
#     def simulate_updates():
#         resource_display_frame.update_resource("gold", 150)
#         resource_display_frame.update_resource("wood", 60)
#         resource_display_frame.update_resource("energy", 70)
#         # Add a new resource dynamically
#         if "stone" not in resource_display_frame.resource_values:
#             resource_display_frame.add_resource("stone", 20)
#         else:
#             resource_display_frame.update_resource("stone", 25)
#         
#         root.after(2000, simulate_updates) # Schedule next update
# 
#     root.after(1000, simulate_updates) # Start updates after 1 second
#     
#     root.mainloop()
