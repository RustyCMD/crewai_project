# Game/qa/continuous_testing.py

import os
import subprocess
import time
import sys

# --- Configuration ---
TEST_SUITE_SCRIPT = "Game/test_suite.py" # Assuming test_suite.py exists and contains all tests
WATCH_DIRECTORY = "Game/"


def run_tests():
    """Runs the test suite and returns True if all tests pass, False otherwise."""
    print(f"\n{'='*50}\nStarting test execution: {TEST_SUITE_SCRIPT}\n{'='*50}")
    try:
        # Execute the test suite script. Use sys.executable to ensure the correct Python interpreter is used.
        # capture_output=True will capture stdout and stderr.
        # text=True decodes stdout and stderr as text.
        process = subprocess.run([
            sys.executable, TEST_SUITE_SCRIPT
        ], check=True, capture_output=True, text=True)
        
        print(f"\n--- Test Output ---\n{process.stdout}\n")
        print(f"{'='*50}\nTest execution finished successfully.\n{'='*50}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- Test Failed ---\nError: {e}\n")
        print(f"--- Test Output (stderr)---\n{e.stderr}\n")
        print(f"--- Test Output (stdout)---\n{e.stdout}\n")
        print(f"{'='*50}\nTest execution failed.\n{'='*50}")
        return False
    except FileNotFoundError:
        print(f"Error: The test suite script '{TEST_SUITE_SCRIPT}' was not found.")
        print("Please ensure 'Game/test_suite.py' exists and is correctly configured.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during test execution: {e}")
        return False


def monitor_changes():
    """Monitors the specified directory for changes and triggers tests."""
    print(f"Starting continuous testing. Monitoring directory: {WATCH_DIRECTORY}")
    print("Press Ctrl+C to stop.")

    # In a real-world scenario, you would integrate this with:
    # 1. Git Hooks (pre-commit, post-commit, pre-push)
    # 2. CI/CD Pipelines (e.g., GitHub Actions, GitLab CI, Jenkins)
    #    - Triggered by push events to specific branches.
    #    - Running tests in a separate environment before merging.

    # For this simulation, we'll just run tests once and then wait for a manual trigger
    # or a simulated change.
    
    last_run_time = 0
    run_tests() # Run tests initially

    # This is a simplified loop. A real implementation would use a file system watcher
    # like `watchdog` or rely on CI/CD triggers.
    while True:
        try:
            # Simulate checking for changes. In a real system, this would be event-driven.
            # For demonstration, we'll just wait and then re-run tests periodically
            # or could be triggered by an external event.
            time.sleep(60) # Wait for 60 seconds before re-checking (simulated)
            current_time = time.time()
            # In a real watcher, you'd check if any files in WATCH_DIRECTORY have changed
            # since last_run_time. For simplicity, we'll just re-run.
            print("\nSimulating code change detection...")
            if run_tests():
                print("All tests passed after simulated change.")
            else:
                print("Some tests failed after simulated change.")
            last_run_time = current_time
        except KeyboardInterrupt:
            print("\nStopping continuous testing.")
            break
        except Exception as e:
            print(f"An error occurred during monitoring: {e}")
            time.sleep(10) # Wait a bit before retrying


if __name__ == "__main__":
    # Check if test_suite.py exists before starting
    if not os.path.exists(TEST_SUITE_SCRIPT):
        print(f"Error: The test suite script '{TEST_SUITE_SCRIPT}' does not exist.")
        print("Please create 'Game/test_suite.py' before running this script.")
        sys.exit(1)
    
    # Check if the directory to watch exists
    if not os.path.isdir(WATCH_DIRECTORY):
        print(f"Error: The watch directory '{WATCH_DIRECTORY}' does not exist.")
        print("Please ensure the 'Game' directory exists.")
        sys.exit(1)

    monitor_changes()