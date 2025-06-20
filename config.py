"""
PyShell Configuration File
Contains all configuration settings for the PyShell application.
"""

# Terminal Layout Configuration
current_terminal_layout = 2

# AI Features Configuration
ai_features = {
    "smart_suggestions": True,
    "auto_complete": True,
    "syntax_highlighting": True
}

# User Interface Configuration
ui_config = {
    "show_execution_time": True,
    "show_suggestions": True,
    "suggestion_frequency": 0.3,  # 30% chance
    "refresh_interval": 0.5
}

# File Paths
USER_FILE = "users.json"
HISTORY_FILE = "history.json"
AI_CONFIG_FILE = "ai_config.json"

# Default Settings
DEFAULT_TERMINAL_LAYOUT = 2
DEFAULT_USER_ROLE = "user"
