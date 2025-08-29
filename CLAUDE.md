# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a game development project that aims to create a Streamlit-based game development agent. The agent will be specialized in educational games for children, focusing on:

- Children's games (少儿游戏)
- Digital/math games (数字游戏) - arithmetic operations (addition, subtraction, multiplication, division)
- Chinese character games (汉字 games)
- English learning games
- Game scene generation based on specified action logic

## Technology Stack

- **Framework**: Streamlit
- **AI Integration**: Supports multiple AI providers (OpenAI, Qwen, Claude)
- **Agent Framework**: Agno

## Project Structure

```
game/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script
├── config/               # Configuration module
│   ├── __init__.py
│   └── settings.py       # Application settings
├── agents/               # Agent modules
│   ├── __init__.py
│   ├── base_agent.py     # Base agent class
│   └── game_agent.py     # Game development agent
├── games/                # Game generators
│   ├── __init__.py
│   ├── math_game.py      # Math game generator
│   ├── chinese_game.py   # Chinese character game generator
│   ├── english_game.py   # English learning game generator
│   └── scene_generator.py # Game scene generator
└── utils/                # Utility modules
    ├── __init__.py
    ├── logger.py         # Logging utility
    ├── ai_providers.py   # AI provider implementations
    └── ai_manager.py     # AI provider manager
```

## Development Commands

### Setup and Running
```bash
# Start the application
./start.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Testing
```bash
# Run the application
python app.py

# Check configuration
python -c "from config.settings import Config; print(Config.validate_config())"
```

## Architecture Notes

The game development agent will need to:
1. Interface with Streamlit for the web interface
2. Connect to multiple AI providers (OpenAI, Qwen, Claude) via their APIs
3. Generate educational game content and scenes
4. Support different types of learning games (math, Chinese, English)
5. Implement game logic based on user-specified actions

## Key Features to Implement

- Multi-AI provider support with unified interface
- Educational game generation templates
- Game scene creation based on action logic
- Learning progress tracking for different subjects
- Child-friendly interface design