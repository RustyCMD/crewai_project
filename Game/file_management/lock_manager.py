# Game/file_management/lock_manager.py

import threading
import logging
from typing import Dict, Optional

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileLockManager:
    """
    Manages file locks to prevent concurrent write conflicts.
    Supports exclusive write locks.
    """
    def __init__(self):
        # Dictionary to store locks: {file_path: threading.Lock()}
        self.file_locks: Dict[str, threading.Lock] = {}
        # Dictionary to store lock status: {file_path: agent_name or None}
        self.lock_status: Dict[str, Optional[str]] = {}
        self.manager_lock = threading.Lock() # Lock for accessing self.file_locks and self.lock_status
        logging.info("FileLockManager initialized.")

    def acquire_lock(self, file_path: str, agent_name: str) -> bool:
        """
        Acquires an exclusive write lock for a given file.

        Args:
            file_path: The path to the file to lock.
            agent_name: The name of the agent attempting to acquire the lock.

        Returns:
            True if the lock was acquired successfully, False otherwise.
        """
        with self.manager_lock:
            if file_path not in self.file_locks:
                self.file_locks[file_path] = threading.Lock()
                self.lock_status[file_path] = None
                logging.info(f"Created lock for file: {file_path}")

            file_lock = self.file_locks[file_path]

            # Attempt to acquire the underlying threading.Lock
            # We use a timeout to prevent indefinite blocking if another agent is holding it
            # In a real distributed system, this would be more complex (e.g., using a distributed lock service)
            lock_acquired = file_lock.acquire(blocking=False)

            if lock_acquired:
                self.lock_status[file_path] = agent_name
                logging.info(f"Agent '{agent_name}' acquired lock for file: {file_path}")
                return True
            else:
                current_holder = self.lock_status.get(file_path, "Unknown")
                logging.warning(f"Agent '{agent_name}' failed to acquire lock for file: {file_path}. Currently held by '{current_holder}'.")
                return False

    def release_lock(self, file_path: str, agent_name: str) -> bool:
        """
        Releases the exclusive write lock for a given file.

        Args:
            file_path: The path to the file to unlock.
            agent_name: The name of the agent attempting to release the lock.

        Returns:
            True if the lock was released successfully, False otherwise.
        """
        with self.manager_lock:
            if file_path not in self.file_locks:
                logging.warning(f"Attempted to release lock for non-existent file: {file_path}")
                return False

            current_holder = self.lock_status.get(file_path)
            if current_holder != agent_name:
                logging.error(f"Agent '{agent_name}' attempted to release lock for file '{file_path}' but it is held by '{current_holder}'.")
                return False

            file_lock = self.file_locks[file_path]
            try:
                file_lock.release()
                self.lock_status[file_path] = None
                logging.info(f"Agent '{agent_name}' released lock for file: {file_path}")
                # Optional: Clean up lock if no longer needed, though keeping it might be useful for status checks
                # del self.file_locks[file_path]
                # del self.lock_status[file_path]
                return True
            except RuntimeError:
                logging.error(f"Agent '{agent_name}' attempted to release an unlocked file: {file_path}")
                return False

    def is_locked(self, file_path: str) -> bool:
        """
        Checks if a file is currently locked.

        Args:
            file_path: The path to the file to check.

        Returns:
            True if the file is locked, False otherwise.
        """
        with self.manager_lock:
            # A file is considered locked if its underlying threading.Lock is not free.
            # Note: This check is a snapshot and might be outdated immediately after.
            if file_path in self.file_locks:
                return not self.file_locks[file_path].locked() # Returns True if NOT locked, so we invert it
            return False # If no lock entry exists, it's not locked

    def get_lock_holder(self, file_path: str) -> Optional[str]:
        """
        Gets the name of the agent currently holding the lock for a file.

        Args:
            file_path: The path to the file.

        Returns:
            The name of the agent holding the lock, or None if the file is not locked.
        """
        with self.manager_lock:
            return self.lock_status.get(file_path)

# --- Example Usage ---
# This section demonstrates how the FileLockManager might be used.
# In a real collaborative environment, this would be managed by a central coordinator or service.

if __name__ == "__main__":
    lock_manager = FileLockManager()
    agent1 = "Alice"
    agent2 = "Bob"
    test_file = "Game/data/config.yaml"

    print(f"--- Testing lock acquisition for {test_file} ---")

    # Agent 1 tries to acquire lock
    print(f"\n{agent1} attempting to acquire lock...")
    if lock_manager.acquire_lock(test_file, agent1):
        print(f"Lock acquired by {agent1}.")
        print(f"Is '{test_file}' locked? {lock_manager.is_locked(test_file)}")
        print(f"Lock holder: {lock_manager.get_lock_holder(test_file)}")

        # Agent 2 tries to acquire the same lock (should fail)
        print(f"\n{agent2} attempting to acquire lock...")
        if lock_manager.acquire_lock(test_file, agent2):
            print(f"Lock acquired by {agent2}. (This should not happen in exclusive mode)")
        else:
            print(f"Failed to acquire lock for {agent2}. File is locked by {lock_manager.get_lock_holder(test_file)}.")
            print(f"Is '{test_file}' locked? {lock_manager.is_locked(test_file)}")

        # Agent 1 releases the lock
        print(f"\n{agent1} releasing lock...")
        if lock_manager.release_lock(test_file, agent1):
            print(f"Lock released by {agent1}.")
            print(f"Is '{test_file}' locked? {lock_manager.is_locked(test_file)}")
            print(f"Lock holder: {lock_manager.get_lock_holder(test_file)}")
        else:
            print(f"Failed to release lock by {agent1}.")

        # Agent 2 tries to acquire lock again (should succeed now)
        print(f"\n{agent2} attempting to acquire lock again...")
        if lock_manager.acquire_lock(test_file, agent2):
            print(f"Lock acquired by {agent2}.")
            print(f"Is '{test_file}' locked? {lock_manager.is_locked(test_file)}")
            print(f"Lock holder: {lock_manager.get_lock_holder(test_file)}")

            # Agent 2 releases the lock
            print(f"\n{agent2} releasing lock...")
            if lock_manager.release_lock(test_file, agent2):
                print(f"Lock released by {agent2}.")
                print(f"Is '{test_file}' locked? {lock_manager.is_locked(test_file)}")
                print(f"Lock holder: {lock_manager.get_lock_holder(test_file)}")
            else:
                print(f"Failed to release lock by {agent2}.")
        else:
            print(f"Failed to acquire lock for {agent2} even after release.")

    else:
        print(f"Initial lock acquisition failed for {agent1}.")

    print("\n--- Testing releasing a lock not held ---")
    print(f"{agent1} attempting to release lock for non-existent file...")
    lock_manager.release_lock("non_existent_file.txt", agent1)

    print(f"\n{agent1} attempting to release lock for '{test_file}' (not holding it)...")
    lock_manager.release_lock(test_file, agent1)
