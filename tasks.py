from crewai import Task

# Game Architecture and Core Systems Task
architecture_task = Task(
    description='''Design and implement the core architecture for a comprehensive Python idle game.

    Requirements:
    1. Create the main game engine with proper MVC architecture
    2. Implement a resource management system (multiple resource types)
    3. Design a modular upgrade system with categories and dependencies
    4. Create a save/load system with JSON serialization
    5. Implement a game loop with proper timing and automation
    6. Design the main GUI framework using tkinter with modern styling

    Technical specifications:
    - Use object-oriented design with clear separation of concerns
    - Implement proper error handling and logging
    - Create extensible systems for easy feature additions
    - Ensure thread-safe operations for background processes
    - Include configuration management for game balance

    Deliverables (create all files in a "Game" folder):
    - Game/game_engine.py: Core game engine and state management
    - Game/resource_manager.py: Resource generation and management
    - Game/upgrade_system.py: Upgrade mechanics and progression
    - Game/save_manager.py: Save/load functionality
    - Game/gui_framework.py: Main GUI components and styling''',
    expected_output='''Complete core game architecture with 5 Python files implementing:
    - Modular game engine with proper state management
    - Resource system supporting multiple resource types
    - Upgrade system with categories and dependencies
    - Robust save/load functionality
    - Modern GUI framework with tkinter
    All files should be well-documented with docstrings and include error handling.'''
)

# Game Features and UI Implementation Task
features_task = Task(
    description='''Implement advanced game features and user interface components.

    Requirements:
    1. Create an achievement system with various achievement types
    2. Implement visual feedback and animations for user actions
    3. Design and build the main game interface with multiple panels
    4. Create automation features (auto-clickers, auto-upgraders)
    5. Implement prestige/rebirth mechanics for long-term progression
    6. Add sound effects and visual polish

    UI Components needed:
    - Resource display panel with real-time updates
    - Upgrade shop with categories and filtering
    - Achievement panel with progress tracking
    - Settings panel with game options
    - Statistics panel showing game metrics
    - Automation controls panel

    Technical requirements:
    - Smooth animations using tkinter or pygame
    - Responsive UI that scales with window size
    - Efficient rendering for good performance
    - Keyboard shortcuts and accessibility features
    - Visual themes and customization options''',
    expected_output='''Complete game features implementation including (create all files in the "Game" folder):
    - Game/achievement_system.py: Achievement tracking and rewards
    - Game/animation_manager.py: Visual effects and animations
    - Game/ui_components.py: All game UI panels and widgets
    - Game/automation_manager.py: Auto-features and AI helpers
    - Game/prestige_system.py: Long-term progression mechanics
    - Game/main_interface.py: Complete game interface integration
    All components should be visually appealing and user-friendly.'''
)

# Game Testing and Balance Task
testing_task = Task(
    description='''Conduct comprehensive testing and game balance validation.

    Testing requirements:
    1. Create automated test suites for all game systems
    2. Perform game balance testing and progression analysis
    3. Test save/load functionality across different scenarios
    4. Validate UI responsiveness and user experience
    5. Performance testing and optimization recommendations
    6. Edge case testing (negative values, overflow, etc.)

    Balance testing focus:
    - Resource generation rates and scaling
    - Upgrade costs and effectiveness
    - Achievement difficulty and rewards
    - Prestige timing and benefits
    - Overall game progression pacing

    Quality assurance:
    - Memory leak detection
    - Error handling validation
    - Cross-platform compatibility
    - User experience flow testing
    - Accessibility compliance''',
    expected_output='''Comprehensive testing suite and balance report including (create all files in the "Game" folder):
    - Game/test_suite.py: Automated tests for all game systems
    - Game/balance_analysis.py: Game balance testing and recommendations
    - Game/performance_report.md: Performance analysis and optimization suggestions
    - Game/bug_report.md: Identified issues and fixes
    - Game/ux_evaluation.md: User experience assessment
    - Game/test_results.json: Detailed test execution results
    All tests should pass and balance recommendations should be actionable.'''
)

# Deployment and Distribution Task
deployment_task = Task(
    description='''Handle game packaging, distribution, and deployment setup.

    Requirements:
    1. Create executable builds for Windows, macOS, and Linux
    2. Set up proper project structure and dependencies
    3. Create installation packages and auto-updater
    4. Implement crash reporting and analytics
    5. Set up version control and release pipeline
    6. Create user documentation and setup guides

    Distribution components:
    - PyInstaller configuration for cross-platform builds
    - Requirements.txt with all dependencies
    - Setup.py for pip installation
    - Docker containerization for cloud deployment
    - GitHub Actions for automated builds
    - User manual and developer documentation

    Technical deliverables:
    - Build scripts for all platforms
    - Installer packages (MSI, DMG, DEB)
    - Auto-updater system
    - Crash reporting integration
    - Analytics dashboard setup''',
    expected_output='''Complete deployment package including (create all files in the "Game" folder):
    - Game/build_scripts/: Platform-specific build configurations
    - Game/installers/: Installation packages for all platforms
    - Game/requirements.txt: Complete dependency list
    - Game/setup.py: Package installation configuration
    - Game/Dockerfile: Container deployment setup
    - Game/.github/workflows/: CI/CD pipeline configuration
    - Game/docs/: User and developer documentation
    - Game/README.md: Project overview and setup instructions
    All builds should be tested and ready for distribution.'''
)