# Game Performance Profiler

import time
from collections import defaultdict

class Profiler:
    def __init__(self):
        """
        Initializes the Profiler.
        This class will monitor and profile performance, recording timings and metrics.
        """
        self.timers = {}  # Stores start times for timers
        self.metrics = defaultdict(lambda: {'calls': 0, 'total_time': 0.0, 'avg_time': 0.0})
        self.start_time = None
        print("Profiler initialized.")

    def start_timer(self, timer_name):
        """
        Starts a named timer.
        Args:
            timer_name (str): The name of the timer to start.
        """
        if timer_name in self.timers:
            print(f"Warning: Timer '{timer_name}' already started. Restarting.")
        self.timers[timer_name] = time.time()
        # print(f"Timer '{timer_name}' started.")

    def stop_timer(self, timer_name):
        """
        Stops a named timer and records its duration.
        Args:
            timer_name (str): The name of the timer to stop.
        Returns:
            float: The duration of the timer in seconds, or None if the timer was not started.
        """
        if timer_name not in self.timers:
            print(f"Error: Timer '{timer_name}' not started.")
            return None

        end_time = time.time()
        duration = end_time - self.timers[timer_name]
        del self.timers[timer_name]  # Remove timer once stopped

        # Update metrics
        self.metrics[timer_name]['calls'] += 1
        self.metrics[timer_name]['total_time'] += duration
        self.metrics[timer_name]['avg_time'] = self.metrics[timer_name]['total_time'] / self.metrics[timer_name]['calls']
        
        # print(f"Timer '{timer_name}' stopped. Duration: {duration:.6f}s")
        return duration

    def record_metric(self, metric_name, value):
        """
        Records a specific performance metric value directly.
        This is useful for metrics that aren't simple time intervals, like FPS or memory usage.
        Args:
            metric_name (str): The name of the metric.
            value (float or int): The value of the metric.
        """
        # For simplicity, we'll just store the last value for these types of metrics.
        # A more advanced system might store a history.
        self.metrics[metric_name]['total_time'] = value # Re-using total_time to store the last recorded value
        self.metrics[metric_name]['calls'] += 1 # Increment call count to indicate it was recorded
        # print(f"Recorded metric '{metric_name}': {value}")

    def get_profiler_results(self):
        """
        Returns the collected profiling data.
        """
        print("Retrieving profiler results...")
        # Ensure avg_time is calculated correctly for all entries, especially non-timed ones
        results = {}
        for name, data in self.metrics.items():
            # Handle potential division by zero if calls is 0 (shouldn't happen if recorded)
            avg_time = data['total_time'] / data['calls'] if data['calls'] > 0 else 0
            results[name] = {
                'calls': data['calls'],
                'total_time': data['total_time'],
                'avg_time': avg_time
            }
        return results

    def start_overall_profiling(self):
        """
        Starts an overall timer for the entire profiling session.
        """
        self.start_time = time.time()
        print("Overall profiling session started.")

    def stop_overall_profiling(self):
        """
        Stops the overall timer and returns the total duration.
        """
        if self.start_time is None:
            print("Error: Overall profiling was not started.")
            return None
        end_time = time.time()
        duration = end_time - self.start_time
        self.start_time = None
        print(f"Overall profiling session stopped. Total duration: {duration:.6f}s")
        # Record this duration as a metric
        self.record_metric("total_session_time", duration)
        return duration

# --- Example Usage ---
if __name__ == "__main__":
    profiler = Profiler()
    
    profiler.start_overall_profiling()

    # Simulate some game operations
    profiler.start_timer("game_loop")
    time.sleep(0.1)
    
    profiler.start_timer("update_player_position")
    time.sleep(0.05)
    profiler.stop_timer("update_player_position")

    profiler.start_timer("render_frame")
    time.sleep(0.08)
    profiler.stop_timer("render_frame")

    profiler.start_timer("update_player_position") # Called again
    time.sleep(0.05)
    profiler.stop_timer("update_player_position")

    profiler.start_timer("calculate_ai")
    time.sleep(0.15)
    profiler.stop_timer("calculate_ai")

    profiler.start_timer("render_frame") # Called again
    time.sleep(0.08)
    profiler.stop_timer("render_frame")

    profiler.stop_timer("game_loop")

    # Record a non-timing metric like FPS (simulated)
    simulated_fps = 60.5
    profiler.record_metric("simulated_fps", simulated_fps)

    # Stop the overall session
    profiler.stop_overall_profiling()

    # Get and print results
    results = profiler.get_profiler_results()
    print("\n--- Profiler Results ---")
    for name, data in results.items():
        print(f"{name}: Calls={data['calls']}, Total Time={data['total_time']:.6f}s, Avg Time={data['avg_time']:.6f}s")
    print("----------------------")