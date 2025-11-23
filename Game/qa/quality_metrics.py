# Game/qa/quality_metrics.py

import os
from radon.complexity import cc_rank, cc_visit
from radon.metrics import mi_rank, mi_visit
from radon.raw import analyze as analyze_raw

# Placeholder for PEP 8 compliance checking. 
# This would typically involve a linter like flake8 or pylint.
# For simplicity, we'll just outline the idea here.
def check_pep8_compliance(file_path):
    """Checks PEP 8 compliance for a given file. (Placeholder)

    Args:
        file_path (str): The path to the Python file to check.

    Returns:
        dict: A dictionary containing PEP 8 compliance results.
              Returns a placeholder message if not fully implemented.
    """
    print(f"\n--- Checking PEP 8 compliance for {file_path} ---")
    # In a real implementation, you would run a tool like flake8:
    # try:
    #     from flake8.api import legacy as flake8
    #     style_guide = flake8.get_style_guide()
    #     # The result object contains errors, but direct integration can be complex.
    #     # For a simpler approach, you might run flake8 as a subprocess and parse its output.
    #     print("Note: PEP 8 compliance check is a placeholder and requires external tools like flake8.")
    #     return {"status": "Placeholder", "message": "Requires flake8 installation and execution."}
    # except ImportError:
    #     print("Error: flake8 library not found. Please install it (`pip install flake8`).")
    #     return {"status": "Error", "message": "flake8 not installed."}
    
    # Placeholder implementation:
    return {
        "status": "Placeholder",
        "message": "PEP 8 compliance check requires integration with a linter like flake8."
    }

def analyze_code_complexity(file_path):
    """Analyzes cyclomatic complexity of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        list: A list of complexity metrics for functions and methods.
    """
    print(f"\n--- Analyzing cyclomatic complexity for {file_path} ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        complexity = cc_visit(source_code)
        print(f"Cyclomatic Complexity Analysis Results for {file_path}:")
        for item in complexity:
            print(f"  - Name: {item.name}, Complexity: {item.complexity} ({cc_rank(item.complexity)}), Line: {item.lineno}")
        return complexity
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error analyzing complexity for {file_path}: {e}")
        return []

def analyze_maintainability_index(file_path):
    """Analyzes Maintainability Index (MI) of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing MI results.
    """
    print(f"\n--- Analyzing Maintainability Index for {file_path} ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        mi = mi_visit(source_code, cc=True) # cc=True includes cyclomatic complexity in MI calculation
        print(f"Maintainability Index Analysis Results for {file_path}:")
        print(f"  - MI Score: {mi:.2f} ({mi_rank(mi)})\n")
        return {"score": mi, "rank": mi_rank(mi)}
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except Exception as e:
        print(f"Error analyzing maintainability index for {file_path}: {e}")
        return {}

def analyze_raw_metrics(file_path):
    """Analyzes raw metrics (lines of code, blank lines, comments) of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing raw metrics.
    """
    print(f"\n--- Analyzing raw metrics for {file_path} ---")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        raw_metrics = analyze_raw(source_code)
        print(f"Raw Metrics Analysis Results for {file_path}:")
        print(f"  - Total Lines: {raw_metrics.lines}\n  - Logical Lines: {raw_metrics.loc}\n  - Blank Lines: {raw_metrics.blank}\n  - Comment Lines: {raw_metrics.comments}")
        return {
            "total_lines": raw_metrics.lines,
            "loc": raw_metrics.loc,
            "blank": raw_metrics.blank,
            "comments": raw_metrics.comments
        }
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except Exception as e:
        print(f"Error analyzing raw metrics for {file_path}: {e}")
        return {}

def generate_quality_report(file_path):
    """Generates a comprehensive quality report for a given Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A consolidated report including complexity, MI, raw metrics, and PEP 8 status.
    """
    print(f"\n{'='*50}\nGenerating Quality Report for: {file_path}\n{'='*50}")
    
    report = {
        "file": file_path,
        "pep8": check_pep8_compliance(file_path),
        "complexity": analyze_code_complexity(file_path),
        "maintainability_index": analyze_maintainability_index(file_path),
        "raw_metrics": analyze_raw_metrics(file_path)
    }
    
    print(f"\n{'='*50}\nQuality Report Summary for {file_path}\n{'='*50}")
    print(f"PEP 8 Status: {report['pep8']['status']} - {report['pep8']['message']}")
    
    if report['maintainability_index']:
        mi_score = report['maintainability_index']['score']
        mi_rank = report['maintainability_index']['rank']
        print(f"Maintainability Index: {mi_score:.2f} ({mi_rank})")
    else:
        print("Maintainability Index: N/A")

    if report['raw_metrics']:
        print(f"Lines of Code (LOC): {report['raw_metrics']['loc']}")
        print(f"Comment Lines: {report['raw_metrics']['comments']}")
    else:
        print("Raw Metrics: N/A")
        
    print(f"\n--- End of Report ---\\n")
    return report

if __name__ == "__main__":
    # Example usage:
    # Create a dummy Python file for testing if it doesn't exist
    DUMMY_FILE = "temp_game_module.py"
    if not os.path.exists(DUMMY_FILE):
        print(f"Creating dummy file: {DUMMY_FILE} for demonstration.")
        with open(DUMMY_FILE, "w", encoding="utf-8") as f:
            f.write("""\n# This is a dummy Python file for quality metrics testing.\n\ndef calculate_sum(a, b):\n    # Calculates the sum of two numbers.\n    result = a + b\n    return result\n\nclass GameLogic:\n    def __init__(self, level):\n        self.level = level\n\n    def get_level_info(self):\n        # Returns information about the current level.\n        if self.level > 10:\n            print(\"High level!\")\n            return \"Advanced\"\n        else:\n            return \"Beginner\"\n\n# Example of a more complex function\ndef process_data(data_list):\n    total = 0\n    for item in data_list:\n        if isinstance(item, (int, float)):\n            total += item\n        elif isinstance(item, str):\n            try:\n                total += float(item) # Try converting strings to float\n            except ValueError:\n                print(f\"Warning: Could not convert '{item}' to float.\")\n    return total\n""")

    # Analyze the dummy file
    generate_quality_report(DUMMY_FILE)
    
    # Clean up the dummy file
    # Uncomment the following lines to remove the file after execution
    # if os.path.exists(DUMMY_FILE):
    #     os.remove(DUMMY_FILE)
    #     print(f"\nRemoved dummy file: {DUMMY_FILE}")
