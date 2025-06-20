"""
AI Panel Module
Provides AI feature configuration and management for PyShell.
"""

import json
import os
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from rich.console import Console

console = Console()
AI_CONFIG_FILE = "ai_config.json"

def load_ai_config():
    """Load AI feature configuration from JSON file."""
    if os.path.exists(AI_CONFIG_FILE):
        try:
            with open(AI_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"smart_suggestions": False}

def save_ai_config(config):
    """Save AI feature configuration to JSON file."""
    with open(AI_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def show_config_panel():
    """Show checklist to toggle AI features ON or OFF."""
    config = load_ai_config()
    default_values = [key for key, value in config.items() if value]

    results = checkboxlist_dialog(
        title="⚙️ AI Configuration",
        text="Use SPACE to toggle features ON/OFF. Press ENTER to save.",
        values=[
            ("smart_suggestions", "💡 Live Smart Suggestions"),
        ],
        default_values=default_values
    ).run()

    if results is not None:
        config["smart_suggestions"] = "smart_suggestions" in results
        save_ai_config(config)
        status = "ON" if config["smart_suggestions"] else "OFF"
        console.print(f"\n[bold green]Live Smart Suggestions are now {status}[/bold green]")

def show_ai_features():
    """Show the AI features menu."""
    from features import nl_to_code, error_explainer, snippet_search, code_refactor
    
    AI_FEATURES = [
        ("nl", "🧠 NL to Code", nl_to_code.run),
        ("explain", "❌ Error Explainer", error_explainer.run),
        ("snippet", "📚 Snippet Search", snippet_search.run),
        ("refactor", "🧹 Code Refactor", code_refactor.run),
        ("back", "↩️ Back to Main Menu", None)
    ]
    
    while True:
        choice = radiolist_dialog(
            title="🤖 AI Features",
            text="Select an AI feature to run:",
            values=[(key, label) for key, label, _ in AI_FEATURES],
        ).run()

        if choice is None or choice == "back":
            break

        # Find and run the selected feature
        for key, label, func in AI_FEATURES:
            if key == choice and func:
                try:
                    func()
                except Exception as e:
                    console.print(f"[bold red]Error in {label}: {e}[/bold red]")
                input("\nPress Enter to return to the AI features menu...")
                break

def show_ai_panel():
    """Main AI panel with options to configure or run features."""
    while True:
        choice = radiolist_dialog(
            title="🤖 PyShell AI Panel",
            text="Choose an option:",
            values=[
                ("features", "🚀 Run AI Features"),
                ("config", "⚙️ Configure AI Settings"),
                ("exit", "↩️ Return to Shell")
            ],
        ).run()

        if choice == "features":
            show_ai_features()
        elif choice == "config":
            show_config_panel()
        elif choice == "exit" or choice is None:
            break

def is_feature_enabled(feature_name):
    """Check if a specific AI feature is enabled in the config."""
    config = load_ai_config()
    return config.get(feature_name, False) 