import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from crew import game_dev_crew
from logging_config import setup_logging, get_logger, log_safe

# Load environment variables
load_dotenv()

def setup_logging():
    """Set up logging configuration for the project."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', './logs/crewai_game_dev.log')

    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Clear any existing handlers to avoid conflicts
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Create file handler with UTF-8 encoding
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(file_formatter)
    except Exception as e:
        print(f"Warning: Could not create file handler: {e}")
        file_handler = None

    # Create console handler with UTF-8 encoding
    try:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(console_formatter)

        # Try to set UTF-8 encoding for console output
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass  # Ignore if reconfigure fails

    except Exception as e:
        print(f"Warning: Could not create console handler: {e}")
        console_handler = None

    # Configure root logger
    handlers = []
    if file_handler:
        handlers.append(file_handler)
    if console_handler:
        handlers.append(console_handler)

    if handlers:
        logging.basicConfig(
            level=getattr(logging, log_level),
            handlers=handlers,
            force=True  # Force reconfiguration
        )
    else:
        # Fallback to basic configuration
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            force=True
        )

    # Test logging setup
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized successfully")

    return True

def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == 'your_gemini_api_key_here':
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the required API keys.")
        print("See .env file for instructions on obtaining API keys.")
        return False

    return True

def main():
    """Main function to run the CrewAI idle game development workflow."""

    # Setup logging
    setup_logging()
    logger = get_logger(__name__)

    print("🎮 CrewAI Idle Game Development Project")
    print("=" * 50)

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Game project specifications
    game_specs = {
        "game_title": os.getenv('GAME_TITLE', 'Idle Adventure'),
        "game_version": os.getenv('GAME_VERSION', '1.0.0'),
        "target_platforms": ["Windows", "macOS", "Linux"],
        "gui_framework": "tkinter",
        "features": [
            "Resource generation and management",
            "Multi-tier upgrade systems",
            "Achievement system with rewards",
            "Save/load functionality",
            "Automation features",
            "Prestige/rebirth mechanics",
            "Visual animations and effects",
            "Sound effects and music",
            "Statistics tracking",
            "Settings and customization"
        ],
        "technical_requirements": [
            "Object-oriented architecture",
            "Modular design patterns",
            "Error handling and logging",
            "Performance optimization",
            "Cross-platform compatibility",
            "Automated testing suite"
        ]
    }

    log_safe(logger, "info", "Starting idle game development workflow...")
    print(f"[ROCKET] Starting development of '{game_specs['game_title']}'")
    print(f"[LIST] Target platforms: {', '.join(game_specs['target_platforms'])}")
    print(f"[TOOLS] GUI Framework: {game_specs['gui_framework']}")
    print(f"[TIME] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 50)

    try:
        # Execute the crew workflow
        result = game_dev_crew.kickoff(inputs=game_specs)

        print("\n" + "=" * 50)
        print("[OK] IDLE GAME DEVELOPMENT COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"[TIME] Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n[CHART] Development Summary:")
        print(result)

        log_safe(logger, "info", "Idle game development workflow completed successfully")

    except Exception as e:
        print(f"\n[ERROR] Error during development workflow: {e}")
        log_safe(logger, "error", f"Workflow execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()