# Project Status Tracker

import logging
import threading
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProjectStatusTracker:
    def __init__(self):
        self.status = "Initializing"
        self.last_updated = None
        self.update_lock = threading.Lock() # To ensure thread-safe updates
        logging.info("Project Status Tracker initialized.")

    def update_status(self, new_status):
        """Updates the project's current status.

        Args:
            new_status (str): The new status message (e.g., "In Progress", "Blocked", "Completed").
        """
        with self.update_lock:
            self.status = new_status
            self.last_updated = datetime.now()
            logging.info(f"Project status updated to: '{self.status}' at {self.last_updated}")

    def get_status(self):
        """Retrieves the current project status and last update time.

        Returns:
            dict: A dictionary containing the current status and last updated timestamp.
        """
        with self.update_lock:
            return {
                "current_status": self.status,
                "last_updated": self.last_updated
            }

    def display_status_dashboard(self):
        """Placeholder for a dashboard display function.
        In a real application, this might involve a UI element or a more complex reporting mechanism.
        """
        current_status_info = self.get_status()
        print("\n--- Project Status Dashboard ---")
        print(f"Current Status: {current_status_info['current_status']}")
        if current_status_info['last_updated']:
            print(f"Last Updated: {current_status_info['last_updated'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Last Updated: Never")
        print("----------------------------\n")

# --- Example Usage --- (This part would typically be managed by the main coordinator)
# if __name__ == "__main__":
#     tracker = ProjectStatusTracker()
#
#     # Simulate status updates
#     tracker.update_status("Development Phase")
#     import time
#     time.sleep(1) # Simulate some work time
#     tracker.update_status("Integration Testing")
#     time.sleep(0.5)
#     tracker.update_status("Refinement and Bug Fixing")
#
#     # Display the current status
#     tracker.display_status_dashboard()
#
#     # Get status programmatically
#     status_info = tracker.get_status()
#     print(f"Programmatic status retrieval: {status_info}")
