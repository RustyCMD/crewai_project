import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from crew import game_dev_crew

# Load environment variables
load_dotenv()

def setup_logging():
    """Set up logging configuration for the project."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', './logs/crewai_game_dev.log')

    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

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
    logger = logging.getLogger(__name__)

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

    logger.info("Starting idle game development workflow...")
    print(f"🚀 Starting development of '{game_specs['game_title']}'")
    print(f"📋 Target platforms: {', '.join(game_specs['target_platforms'])}")
    print(f"🛠️  GUI Framework: {game_specs['gui_framework']}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 50)

    try:
        # Execute the crew workflow
        result = game_dev_crew.kickoff(inputs=game_specs)

        print("\n" + "=" * 50)
        print("✅ IDLE GAME DEVELOPMENT COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📊 Development Summary:")
        print(result)

        logger.info("Idle game development workflow completed successfully")

    except Exception as e:
        print(f"\n❌ Error during development workflow: {e}")
        logger.error(f"Workflow execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()