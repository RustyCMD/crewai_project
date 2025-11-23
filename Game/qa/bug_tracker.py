# Game/qa/bug_tracker.py

import json
from datetime import datetime

class BugTracker:
    """Manages the tracking and reporting of bugs.

    This class provides functionalities to log new bugs, update their status,
    assign them to developers, and generate reports.
    """
    def __init__(self, storage_file="bug_data.json"):
        self.storage_file = storage_file
        self.bugs = self.load_bugs()
        self.next_id = self.generate_next_id()

    def load_bugs(self):
        """Loads bugs from the JSON storage file."""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty/corrupt, start with an empty list.
            return []

    def save_bugs(self):
        """Saves the current bugs to the JSON storage file."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.bugs, f, indent=4)

    def generate_next_id(self):
        """Generates the next unique bug ID."""
        if not self.bugs:
            return 1
        # Find the maximum existing ID and add 1
        max_id = max(bug.get('id', 0) for bug in self.bugs)
        return max_id + 1

    def log_bug(self, description, severity, steps_to_reproduce, reported_by="QA Engineer"):
        """Logs a new bug with the given details.

        Args:
            description (str): A detailed description of the bug.
            severity (str): The severity level (e.g., 'Critical', 'Major', 'Minor', 'Trivial').
            steps_to_reproduce (str): Step-by-step instructions to reproduce the bug.
            reported_by (str, optional): The person who reported the bug. Defaults to "QA Engineer".

        Returns:
            dict: The newly logged bug information.
        """
        new_bug = {
            'id': self.next_id,
            'description': description,
            'severity': severity,
            'steps_to_reproduce': steps_to_reproduce,
            'status': 'Open',  # Default status
            'assigned_to': None,
            'reported_by': reported_by,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.bugs.append(new_bug)
        self.save_bugs()
        self.next_id += 1
        print(f"Bug #{new_bug['id']} logged successfully.")
        return new_bug

    def update_bug_status(self, bug_id, new_status):
        """Updates the status of an existing bug.

        Args:
            bug_id (int): The ID of the bug to update.
            new_status (str): The new status for the bug (e.g., 'Open', 'In Progress', 'Resolved', 'Closed').

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        for bug in self.bugs:
            if bug['id'] == bug_id:
                bug['status'] = new_status
                bug['updated_at'] = datetime.now().isoformat()
                self.save_bugs()
                print(f"Bug #{bug_id} status updated to '{new_status}'.")
                return True
        print(f"Error: Bug with ID {bug_id} not found.")
        return False

    def assign_bug(self, bug_id, assignee):
        """Assigns a bug to a specific developer.

        Args:
            bug_id (int): The ID of the bug to assign.
            assignee (str): The name or identifier of the developer.

        Returns:
            bool: True if the assignment was successful, False otherwise.
        """
        for bug in self.bugs:
            if bug['id'] == bug_id:
                bug['assigned_to'] = assignee
                bug['status'] = 'In Progress' # Automatically set to 'In Progress' when assigned
                bug['updated_at'] = datetime.now().isoformat()
                self.save_bugs()
                print(f"Bug #{bug_id} assigned to '{assignee}'.")
                return True
        print(f"Error: Bug with ID {bug_id} not found.")
        return False

    def get_bug_report(self, bug_id=None, status=None, assignee=None):
        """Generates a report of bugs, optionally filtered.

        Args:
            bug_id (int, optional): Filter by specific bug ID.
            status (str, optional): Filter by bug status.
            assignee (str, optional): Filter by assigned developer.

        Returns:
            list: A list of bug dictionaries matching the filter criteria.
        """
        filtered_bugs = self.bugs

        if bug_id is not None:
            filtered_bugs = [bug for bug in filtered_bugs if bug['id'] == bug_id]
        if status is not None:
            filtered_bugs = [bug for bug in filtered_bugs if bug['status'].lower() == status.lower()]
        if assignee is not None:
            filtered_bugs = [bug for bug in filtered_bugs if bug['assigned_to'] == assignee]

        if not filtered_bugs:
            print("No bugs found matching the criteria.")
            return []
            
        print(f"\n--- Bug Report (Filters: ID={bug_id}, Status={status}, Assignee={assignee}) ---")
        for bug in filtered_bugs:
            print(f"  ID: {bug['id']}, Status: {bug['status']}, Severity: {bug['severity']}, Assigned: {bug['assigned_to'] or 'Unassigned'}\n      Desc: {bug['description'][:70]}...")
        print("--------------------------------------------------")
        return filtered_bugs

    def view_all_bugs(self):
        """Prints a summary of all logged bugs."""
        self.get_bug_report()

# --- Example Usage ---
if __name__ == "__main__":
    tracker = BugTracker()

    # Log some bugs
    bug1 = tracker.log_bug(
        description="Game crashes when entering the main menu.",
        severity="Critical",
        steps_to_reproduce="1. Launch the game. 2. Click 'Main Menu'. 3. Observe crash."
    )

    bug2 = tracker.log_bug(
        description="Player character model is distorted.",
        severity="Major",
        steps_to_reproduce="1. Load into a game. 2. Observe player model."
    )

    bug3 = tracker.log_bug(
        description="UI button is misaligned.",
        severity="Minor",
        steps_to_reproduce="1. Open the settings menu. 2. Look at the 'Apply' button."
    )

    # Update status and assign bugs
    tracker.update_bug_status(bug1['id'], 'In Progress')
    tracker.assign_bug(bug1['id'], 'Alice')

    tracker.update_bug_status(bug2['id'], 'Resolved')
    tracker.assign_bug(bug2['id'], 'Bob')

    # View all bugs
    tracker.view_all_bugs()

    # Get a report for critical bugs
    tracker.get_bug_report(status='Critical')

    # Get a report for bugs assigned to Alice
    tracker.get_bug_report(assignee='Alice')

    # Get a specific bug report
    tracker.get_bug_report(bug_id=bug3['id'])

    # Example of a bug that doesn't exist
    tracker.get_bug_report(bug_id=999)
