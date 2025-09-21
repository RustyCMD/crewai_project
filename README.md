# CrewAI Idle Game Development Project

A comprehensive CrewAI project for developing a full-featured Python idle/incremental game using Google's Gemini 2.5 Pro API.

## 🎮 Project Overview

This project uses CrewAI to orchestrate a team of AI agents that collaborate to develop a complete idle game with advanced features including resource management, upgrade systems, achievements, save/load functionality, and more.

## 🤖 AI Agents

- **Senior Game Architect**: Designs core architecture and complex systems
- **Junior Game Developer**: Implements features and UI components  
- **Game QA Engineer**: Tests game balance and quality assurance
- **Game DevOps Engineer**: Handles packaging and deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd crewai_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env` file and update with your API key
   - Get your Gemini API key from: https://makersuite.google.com/app/apikey
   - Replace `your_gemini_api_key_here` with your actual API key

4. **Run the development workflow:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
crewai_project/
├── agents/                 # AI agent definitions
│   ├── junior_agent.py    # Junior game developer
│   ├── senior_agent.py    # Senior game architect
│   ├── qa_agent.py        # QA engineer
│   └── devops_agent.py    # DevOps engineer
├── tasks.py               # Game development tasks
├── crew.py                # Crew configuration
├── main.py                # Main execution script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## 🎯 Game Features

The AI agents will develop a comprehensive idle game with:

### Core Systems
- **Resource Management**: Multiple resource types with generation rates
- **Upgrade Systems**: Multi-tier upgrades with dependencies
- **Save/Load System**: Persistent game state with JSON serialization
- **Game Loop**: Proper timing and automation mechanics

### Advanced Features
- **Achievement System**: Various achievement types with rewards
- **Visual Feedback**: Animations and effects for user actions
- **Automation**: Auto-clickers and auto-upgraders
- **Prestige System**: Long-term progression mechanics
- **Modern GUI**: Responsive interface using tkinter

### Quality Assurance
- **Comprehensive Testing**: Automated test suites
- **Game Balance**: Progression analysis and optimization
- **Performance**: Memory and CPU optimization
- **Cross-Platform**: Windows, macOS, and Linux support

## 🛠️ Development Workflow

1. **Architecture Phase**: Senior agent designs core systems
2. **Implementation Phase**: Junior agent builds features and UI
3. **Testing Phase**: QA agent validates quality and balance
4. **Deployment Phase**: DevOps agent packages for distribution

## 📊 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GAME_TITLE`: Name of the game (default: "Idle Adventure")
- `LOG_LEVEL`: Logging level (default: "INFO")
- `DEVELOPMENT_MODE`: Enable development features (default: "true")

### Game Configuration

The game specifications can be customized in `main.py`:
- Target platforms
- GUI framework choice
- Feature requirements
- Technical specifications

## 🔧 Customization

### Adding New Agents

1. Create a new agent file in `agents/`
2. Configure with Gemini LLM and appropriate tools
3. Add to crew configuration in `crew.py`

### Modifying Tasks

Update `tasks.py` to customize:
- Task descriptions and requirements
- Expected outputs and deliverables
- Agent assignments

### Extending Features

The modular architecture allows easy extension:
- Add new game mechanics
- Integrate additional AI tools
- Customize UI frameworks

## 📝 Logging

Logs are written to:
- Console output (real-time)
- `./logs/crewai_game_dev.log` (persistent)

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the logs for error details
2. Verify API key configuration
3. Ensure all dependencies are installed
4. Review the CrewAI documentation

## 🔗 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Python Game Development](https://realpython.com/pygame-a-primer/)
