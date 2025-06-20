import os
import time
import psutil
import json
import pyperclip
import random
import string
import threading
import msvcrt
import config
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from ai_panel import show_ai_panel, is_feature_enabled
from rich.live import Live
from rich.table import Table
from prompt_toolkit.formatted_text import HTML
from features.smart_suggestions import get_live_suggestion

# Dependencies
from weather import Weather
from tasks import Task
from linux_commands import Commands
from git_commands import Git
from terminals import Terminal
from equations import Equations
from statistics_menu import show_statistics_menu
from graphs import GraphPlotter

console = Console()
USER_FILE = "users.json"
lock = threading.Lock()

# Animated ASCII Art for PyShell
ASCII_ART = [
    " ____        ____  _          _ _ ",
    "|  _ \\ _   _/ ___|| |__   ___| | |",
    "| |_) | | | \\___ \\| '_ \\ / _ \\ | |",
    "|  __/| |_| |___) | | | |  __/ | |",
    "|_|    \\__, |____/|_| |_|\\___|_|_|",
    "       |___/"
]

COLOR_WAVE = [
    "deep_pink3", "hot_pink", "magenta", "purple", 
    "blue_violet", "royal_blue1", "cyan", "turquoise2",
    "spring_green3", "lime", "yellow", "orange1",
    "red", "dark_red", "deep_pink2", "medium_purple"
]

def animate_ascii_art_wave():
    """Animate the PyShell ASCII art with color wave effect."""
    for frame in range(7):  # 7 frames
        console.clear()
        for idx, line in enumerate(ASCII_ART):
            wave_offset = (frame + idx) % len(COLOR_WAVE)
            styled_line = Text()
            for i, char in enumerate(line):
                color = COLOR_WAVE[(wave_offset + i) % len(COLOR_WAVE)]
                styled_line.append(char, style=color)
            console.print(styled_line)
        time.sleep(0.07)
    console.clear()
    # Final static display with gradient effect
    final_colors = ["deep_pink3", "hot_pink", "magenta", "purple", "blue_violet", "royal_blue1"]
    for i, line in enumerate(ASCII_ART):
        color = final_colors[i % len(final_colors)]
        console.print(Text(line, style=f"bold {color}"))

def show_command_feedback(cmd):
    """Show visual feedback for command execution."""
    table = Table.grid(padding=(0, 1))
    table.add_column("Status", style="cyan")
    table.add_column("Command", style="green")
    table.add_row("", cmd)
    with Live(table, refresh_per_second=10):
        time.sleep(0.1)  # Brief pause for visual feedback

def show_smart_suggestion():
    """Show a random smart suggestion to the user."""
    suggestions = [
        "Try 'git status' to check repository state",
        "Use 'weather' to get local forecast",
        "Run 'stats' for statistical calculations",
        "Type '~ai' to configure AI features"
    ]
    suggestion = random.choice(suggestions)
    console.print(f"\n[bold green]💡 {suggestion}[/bold green]")

def load_users():
    """Load user data from JSON file."""
    with lock:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                return json.load(file)
    return {}

def save_users(users):
    """Save user data to JSON file."""
    with lock:
        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)

def clipboard_copy(text):
    """Copy text to clipboard."""
    with lock:
        pyperclip.copy(text)
        console.print("Text copied to clipboard!", style="bold green")

def clipboard_paste():
    """Display clipboard content."""
    with lock:
        console.print(f"Clipboard Content: {pyperclip.paste()}", style="bold yellow")

def register_user():
    """Register a new user."""
    users = load_users()
    username = Prompt.ask("Enter new username")
    role = Prompt.ask("Assign role (admin/user)", choices=["admin", "user"], default="user")
    if username in users:
        console.print("User already exists!", style="bold red")
        return register_user()
    password = Prompt.ask("Enter password", password=True)
    users[username] = {"password": password, "role": role}
    save_users(users)
    console.print("User registered successfully!", style="bold green")
    return username, role

def login_user():
    """Authenticate existing user."""
    users = load_users()
    username = Prompt.ask("Enter username")
    password = Prompt.ask("Enter password", password=True)
    if username in users and users[username]["password"] == password:
        console.print("Login successful!", style="bold green")
        return username, users[username]["role"]
    else:
        console.print("Invalid credentials!", style="bold red")
        return login_user()

def list_processes(*args):
    """List running processes."""
    for proc in psutil.process_iter(['pid', 'name']):
        console.print(f"{proc.info['pid']} - {proc.info['name']}")

def kill_process(args):
    """Kill a process by PID."""
    if not args:
        console.print("Usage: kill <PID>", style="bold red")
        return
    try:
        psutil.Process(int(args[0])).terminate()
        console.print(f"Process {args[0]} terminated", style="bold red")
    except Exception as e:
        console.print(str(e), style="bold red")

def generate_password(*args):
    """Generate a random password."""
    length = Prompt.ask("Enter password length (default 12)", default="12")
    try:
        length = int(length)
    except ValueError:
        console.print("Invalid input. Using default length (12)", style="bold red")
        length = 12
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    console.print(f"Generated Password: {password}", style="bold green")
    clipboard_copy(password)

def display_prompt(username):
    """Display the terminal prompt based on current layout."""
    terminal = Terminal()
    if config.current_terminal_layout == 1:  
        terminal.terminal_1()
    elif config.current_terminal_layout == 2:
        terminal.terminal_2()
    elif config.current_terminal_layout == 3:
        terminal.terminal_3()
    elif config.current_terminal_layout == 4:
        terminal.terminal_4()
    elif config.current_terminal_layout == 5:
        terminal.terminal_5()
    elif config.current_terminal_layout == 6:
        terminal.terminal_6()
    elif config.current_terminal_layout == 7:
        terminal.terminal_7()
    elif config.current_terminal_layout == 8:
        terminal.terminal_8()
        
    prompt = terminal.get_prompt()
    console.print(f"{prompt}", justify="left")

def clear(*args):
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_suggestions():
    """Display helpful suggestions to the user."""
    suggestions = """
# Welcome to PyShell!

Here are some things you can try:

• File: rename, move, copy, delete, create, list, edit, cd  
• Processes: list, kill  
• Network: info  
• Clipboard: copy, paste  
• Password: generate  
• Math: calculator, math-help, equation, differential, stats  
• Weather: get weather  
• Tasks: schedule, list, unschedule, stop  
• Terminal: change style  
• Games: play games  
• Graphs: plot  
• Git: status, branches, create, switch, delete, merge, clone, add, commit, push, pull, stash, undo, recover, dashboard, auto_merge, voice, reminder, offline_sync, history, help  
• Music: play a song  
• Other: clear, exit  
"""
    panel = Panel.fit(Markdown(suggestions), title="💡 Suggestions", border_style="yellow", padding=(1, 2))
    console.print(panel)

def show_help(commands_dict):
    """Display a list of all available commands."""
    console.print("\n[bold cyan]Available Commands:[/bold cyan]")
    for command in sorted(commands_dict.keys()):
        console.print(f"- {command}")
    console.print("\nType `~ai` to access AI features.")

def main():
    """Main application entry point."""
    console.clear()
    animate_ascii_art_wave()
    
    username, role = register_user() if Prompt.ask("New user?", choices=["y", "n"]) == "y" else login_user()

    # Initialize command objects
    cmds = Commands()
    task = Task()
    weather = Weather()
    terminal = Terminal()
    git = Git()
    eq = Equations()
    graph = GraphPlotter()
    
    # Command dictionary
    commands = {
        "rename": cmds.rename_item,
        "move": cmds.move_file,
        "copy": cmds.copy_file,
        "processes": list_processes,
        "kill": kill_process,
        "network": cmds.network_info,
        "copytext": clipboard_copy,
        "paste": clipboard_paste,
        "password": generate_password,
        "calc": cmds.calculator,
        "stats": lambda args: show_statistics_menu(),
        "equation": eq.solve_equation,
        "differential": lambda args: eq.solve_differential(args),
        "math-help": cmds.math_help,
        "weather": weather.get_weather,
        "schedule": task.schedule_task,  
        "tasks": task.list_scheduled_tasks,  
        "unschedule": task.remove_scheduled_task,
        "stop": task.stop_running_tasks,
        "cls": clear,
        "terminal": lambda args: terminal.show_terminal_themes(),
        "games": lambda *args: console.print('Game feature not implemented.'),
        "plot": lambda args: graph.run(),
        "help": lambda *args: show_help(commands),
        "exit": lambda _: exit(),
    }
    
    # Start task scheduler
    scheduler_thread = threading.Thread(target=Task().run_scheduler, daemon=True)
    scheduler_thread.start()
    
    show_suggestions()
    
    # Define required arguments for each command
    command_args = {
        "rename": ["<old_name>", "<new_name>"],
        "move": ["<source>", "<destination>"],
        "copy": ["<source>", "<destination>"],
        "kill": ["<PID>"],
        "copytext": ["<text>"],
        "equation": ["<equation>"],
        "differential": ["<equation>"],
        "weather": ["<location>"],
        "schedule": ["<task_name>", "<time>"],
        "unschedule": ["<task_name>"],
        "git-create": ["<branch_name>"],
        "git-switch": ["<branch_name>"],
        "git-merge": ["<branch_name>"],
        "git-delete": ["<branch_name>"],
        "git-clone": ["<repository_url>"],
        "git-add": ["<file>"],
        "git-commit": ["<message>"],
        "play": ["<song_name>"]
    }

    class CommandCompleter(Completer):
        """Command completion handler."""
        def get_completions(self, document, complete_event):
            text = document.text_before_cursor
            words = text.split()
            if len(words) == 1:
                for cmd in commands.keys():
                    if cmd.startswith(words[0]):
                        yield Completion(cmd, start_position=-len(words[0]))
            elif len(words) == 2 and words[0] in command_args:
                for arg in command_args[words[0]]:
                    if arg.startswith(words[1]):
                        yield Completion(arg, start_position=-len(words[1]))

    def get_bottom_toolbar():
        """Get bottom toolbar with live suggestions."""
        if is_feature_enabled("smart_suggestions"):
            return HTML(get_live_suggestion(session.default_buffer.text, commands, command_args))
        return None

    session = PromptSession(
        completer=CommandCompleter(),
        bottom_toolbar=get_bottom_toolbar,
        refresh_interval=0.5
    )
    
    # Main command loop
    while True:
        display_prompt(username)
        try:
            user_input = session.prompt("").strip().lower()
            if not user_input:
                continue
            command = user_input.split()
            cmd, *args = command
            start_time = time.time()
            
            # Show command feedback
            show_command_feedback(cmd)
            
            if cmd == "~ai":
                show_ai_panel()
                continue
            if cmd in commands:
                commands[cmd](args)
            else:
                if cmd == "ls":
                    cmds.list_files()
                elif cmd == "touch" and args:
                    cmds.create_file(args[0])
                elif cmd == "rm" and args:
                    cmds.delete_file(args[0])
                elif cmd == "mkdir" and args:
                    cmds.create_folder(args[0])
                elif cmd == "rmdir" and args:
                    cmds.delete_folder(args[0])
                elif cmd == "cd" and args:
                    cmds.change_directory(args[0])
                elif cmd == "edit" and args:
                    cmds.text_editor(args[0])
                elif cmd == "sysinfo":
                    cmds.system_info()
                elif cmd == "exit":
                    console.print("Exiting PyShell...", style="bold red")
                    break
                else:
                    console.print("Invalid command!", style="bold red")
            
            exec_time = time.time() - start_time
            console.print(f"Execution time: {exec_time:.4f} seconds", style="bold yellow")
            
            # Show smart suggestion occasionally
            if random.random() < 0.3:  # 30% chance
                show_smart_suggestion()
                
            time.sleep(1)
        except KeyboardInterrupt:
            console.print("\nUse 'exit' to quit", style="bold yellow")
        except Exception as e:
            console.print(f"Error: {str(e)}", style="bold red")

if __name__ == "__main__":
    main()
