# Game Performance Metrics Tracker

import time
from collections import defaultdict

class PerformanceMetrics:
    def __init__(self):
        """
        Initializes the PerformanceMetrics tracker.
        This class will record and store various performance indicators over time.
        It can be extended to include functionalities for visualization and reporting.
        """
        self.metrics = defaultdict(lambda: defaultdict(list))
        self.start_time = time.time()

    def record_metric(self, name, value, timestamp=None):
        """
        Records a single performance metric.

        Args:
            name (str): The name of the metric (e.g., 'frame_rate', 'cpu_usage', 'memory_usage').
            value (float or int): The value of the metric.
            timestamp (float, optional): The time at which the metric was recorded. 
                                         Defaults to the current time.
        """
        if timestamp is None:
            timestamp = time.time() - self.start_time  # Use time elapsed since start
        self.metrics[name]['values'].append(value)
        self.metrics[name]['timestamps'].append(timestamp)
        # print(f"Recorded metric: {name} = {value} at time {timestamp:.2f}s")

    def get_metric_data(self, name):
        """
        Retrieves all recorded data for a specific metric.

        Args:
            name (str): The name of the metric to retrieve.

        Returns:
            dict: A dictionary containing 'values' and 'timestamps' lists for the metric,
                  or None if the metric has not been recorded.
        """
        if name in self.metrics:
            return {
                'values': self.metrics[name]['values'],
                'timestamps': self.metrics[name]['timestamps']
            }
        return None

    def get_all_metrics(self):
        """
        Returns all recorded metrics.

        Returns:
            dict: A dictionary where keys are metric names and values are dictionaries
                  containing 'values' and 'timestamps' lists.
        """
        return dict(self.metrics)

    def calculate_average(self, name):
        """
        Calculates the average value for a given metric.

        Args:
            name (str): The name of the metric.

        Returns:
            float: The average value of the metric, or 0 if no data is available.
        """
        data = self.get_metric_data(name)
        if data and data['values']:
            return sum(data['values']) / len(data['values'])
        return 0

    def get_trend(self, name):
        """
        Provides a basic trend indication (e.g., average of first half vs. second half).
        More sophisticated trend analysis can be added here.

        Args:
            name (str): The name of the metric.

        Returns:
            str: A string indicating the trend ('increasing', 'decreasing', 'stable', or 'N/A').
        """
        data = self.get_metric_data(name)
        if not data or len(data['values']) < 2:
            return "N/A"

        n = len(data['values'])
        midpoint = n // 2

        first_half_avg = sum(data['values'][:midpoint]) / midpoint if midpoint > 0 else 0
        second_half_avg = sum(data['values'][midpoint:]) / (n - midpoint) if (n - midpoint) > 0 else 0

        if second_half_avg > first_half_avg * 1.1:  # 10% increase
            return "increasing"
        elif second_half_avg < first_half_avg * 0.9: # 10% decrease
            return "decreasing"
        else:
            return "stable"

    def report_summary(self):
        """
        Prints a summary of the recorded performance metrics.
        """
        print("\n--- Performance Metrics Summary ---")
        if not self.metrics:
            print("No metrics recorded yet.")
            return

        for name, data in self.metrics.items():
            if not data['values']:
                print(f"- {name}: No data recorded.")
                continue

            avg_value = self.calculate_average(name)
            trend = self.get_trend(name)
            print(f"- {name}:")
            print(f"    Average: {avg_value:.4f}")
            print(f"    Count: {len(data['values'])}")
            print(f"    Trend: {trend}")
            # Optionally display min/max or other stats
            # print(f"    Min: {min(data['values']):.4f}, Max: {max(data['values']):.4f}")
        print("---------------------------------")

# --- Example Usage ---
# if __name__ == "__main__":
#     metrics_tracker = PerformanceMetrics()
#
#     # Simulate recording some metrics over time
#     for i in range(100):
#         # Simulate frame rate fluctuating
#         frame_rate = 60 - (i % 10) + (i % 5) 
#         metrics_tracker.record_metric("frame_rate", frame_rate)
#
#         # Simulate CPU usage increasing over time
#         cpu_usage = 30 + i * 0.5 
#         metrics_tracker.record_metric("cpu_usage", cpu_usage)
#
#         # Simulate memory usage fluctuating
#         memory_usage = 1024 + (i % 20) * 10 - (i % 10) * 5
#         metrics_tracker.record_metric("memory_usage", memory_usage)
#
#         time.sleep(0.05) # Simulate game loop tick
#
#     # Get specific metric data
#     frame_rate_data = metrics_tracker.get_metric_data("frame_rate")
#     if frame_rate_data:
#         print("\nFrame Rate Data:", frame_rate_data)
#
#     # Get summary report
#     metrics_tracker.report_summary()
#
#     # Check trend for a metric
#     print(f"\nTrend for CPU Usage: {metrics_tracker.get_trend('cpu_usage')}")
#     print(f"Trend for Frame Rate: {metrics_tracker.get_trend('frame_rate')}")
