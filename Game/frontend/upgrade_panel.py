# Game/frontend/upgrade_panel.py

import tkinter as tk
from tkinter import ttk

class UpgradePanel(ttk.Frame):
    def __init__(self, parent, backend_api, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.backend_api = backend_api # Reference to backend functions for checking costs and applying upgrades

        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Creates the UI elements for the upgrade panel."""
        # Label for the upgrade panel
        ttk.Label(self, text="Upgrades", font=('Arial', 16, 'bold')).grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Frame to hold the list of upgrades
        self.upgrades_frame = ttk.Frame(self, padding="10")
        self.upgrades_frame.grid(row=1, column=0, sticky="nsew")
        self.upgrades_frame.grid_columnconfigure(0, weight=1)

        # Placeholder for actual upgrade display and purchase buttons
        # This section will be populated dynamically based on available upgrades
        ttk.Label(self.upgrades_frame, text="Available Upgrades will be listed here.").grid(row=0, column=0, pady=5)

    def refresh_upgrades(self):
        """Refreshes the display of available upgrades and their costs."""
        # Clear existing upgrade widgets
        for widget in self.upgrades_frame.winfo_children():
            if widget.winfo_class() != "TLabel": # Keep the title label
                widget.destroy()

        # Fetch available upgrades and their details from the backend
        # For now, using placeholder data
        available_upgrades = [
            {"name": "Faster Production", "cost": 100, "level": 1, "id": "prod_speed_1"},
            {"name": "More Storage", "cost": 150, "level": 1, "id": "storage_1"},
            # Add more upgrades as needed
        ]

        for i, upgrade in enumerate(available_upgrades):
            row_frame = ttk.Frame(self.upgrades_frame, relief="groove", borderwidth=1)
            row_frame.grid(row=i+1, column=0, pady=5, padx=5, sticky="ew")
            row_frame.grid_columnconfigure(2, weight=1) # Make name column expand

            ttk.Label(row_frame, text=f"Level {upgrade['level']}:").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(row_frame, text=upgrade['name']).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            cost_label = ttk.Label(row_frame, text=f"Cost: {upgrade['cost']}")
            cost_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

            # Purchase button
            purchase_button = ttk.Button(row_frame, text="Buy", command=lambda u_id=upgrade['id'], u_cost=upgrade['cost']: self.purchase_upgrade(u_id, u_cost))
            purchase_button.grid(row=0, column=3, padx=5, pady=5)

        # Add a refresh button (optional)
        ttk.Button(self, text="Refresh Upgrades", command=self.refresh_upgrades).grid(row=2, column=0, pady=10)

    def purchase_upgrade(self, upgrade_id, cost):
        """Handles the logic for purchasing an upgrade."""
        print(f"Attempting to purchase upgrade: {upgrade_id} with cost: {cost}")
        # TODO: Implement communication with backend to check affordability and apply upgrade
        # Example:
        # if self.backend_api.can_afford(cost):
        #     success = self.backend_api.apply_upgrade(upgrade_id)
        #     if success:
        #         print(f"Successfully purchased {upgrade_id}")
        #         self.refresh_upgrades() # Refresh to show updated costs/availability
        #     else:
        #         print(f"Failed to apply upgrade {upgrade_id}")
        # else:
        #     print("Not enough resources to purchase this upgrade.")
        
        # For now, just simulate a purchase and refresh
        print(f"Simulated purchase of {upgrade_id}. Refreshing...")
        self.refresh_upgrades() # Refresh after simulated purchase

# --- Example Usage (when integrating into the main window) ---
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Upgrade Panel Test")
#     
#     # Mock backend API for demonstration
#     class MockBackendAPI:
#         def can_afford(self, cost):
#             print(f"Mock: Checking if affordable for {cost}")
#             return True # Always affordable in mock
#         def apply_upgrade(self, upgrade_id):
#             print(f"Mock: Applying upgrade {upgrade_id}")
#             return True # Always successful in mock
#     
#     mock_api = MockBackendAPI()
#     upgrade_panel = UpgradePanel(root, mock_api)
#     upgrade_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#     
#     upgrade_panel.refresh_upgrades() # Populate with initial upgrades
#     
#     root.mainloop()
