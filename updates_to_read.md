# PyShell Awoken: AI-Powered & Reimagined 🚀

Welcome to the next chapter of PyShell. We've gone back to the drawing board, not just to add features, but to fundamentally evolve the command-line experience. PyShell is now a smarter, more intuitive, and deeply integrated AI-powered assistant designed for developers, students, and power users.

This document dives deep into the powerful new capabilities you can now wield.

---

## 🧠 Your Personal AI Coding Partner: A Deep Dive

The biggest leap forward is the integration of a powerful, **local Large Language Model (LLM)**. This isn't just a gimmick; it's a suite of tools designed to augment your workflow, running entirely on your machine. No data leaves your computer, no API keys are needed, and it works completely offline.

Access the AI command center with one simple command:
```sh
~ai
```
This opens the **AI Panel**, your gateway to all AI features.

### How to Set Up Your Local LLM

To unlock the AI magic, you need to tell PyShell where to find your local model.

1.  **Download a GGUF model:** PyShell uses the `llama-cpp-python` library, which requires models in the GGUF format. You can find thousands of compatible models on [Hugging Face](https://huggingface.co/models?search=gguf). We recommend starting with a smaller, quantized model like *Mistral 7B Instruct* or *Llama 3 8B Instruct*.

2.  **Update the Configuration:**
    *   Open the `local_llm_client.py` file.
    *   Find the `MODEL_PATH` variable.
    *   Update the path to point to the `.gguf` file you downloaded.

    ```python
    # Example path in local_llm_client.py
    MODEL_PATH = "C:/path/to/your/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    ```

The first time you use an AI feature, PyShell will load the model into memory. You'll see a confirmation message once it's ready.

### AI Feature Showcase:

#### 1. 💬 Natural Language to Code
Tired of forgetting command syntax? Just tell PyShell what you want to do.

*   **How to Use:**
    1.  Run `~ai` and select "NL to Code".
    2.  At the prompt, describe your task in plain English.
    3.  The AI will generate the corresponding code or command.
    4.  You'll be asked if you want to execute it.

*   **Example:**
    *   **Your Input:** `Find all python files in the current directory and count them`
    *   **AI Output:** `find . -name "*.py" | wc -l`

#### 2. 🐞 Error Explainer
Transform cryptic error messages into clear, actionable advice.

*   **How to Use:**
    1.  Run `~ai` and select "Error Explainer".
    2.  Paste the full error message you received.
    3.  The AI will provide a detailed explanation of the error and suggest a fix.

*   **Example:**
    *   **Your Input:** `NameError: name 'my_variable' is not defined`
    *   **AI Output:** `This "NameError" means you are trying to use a variable called 'my_variable' before you have assigned any value to it. To fix this, make sure you declare and initialize 'my_variable' before this line, like so: my_variable = "some_value"`

#### 3. ✨ Code Refactor
Instantly improve your code for readability, performance, and best practices.

*   **How to Use:**
    1.  Run `~ai` and select "Code Refactor".
    2.  Paste your block of code into the terminal.
    3.  Press `CTRL+D` (on Linux/macOS) or `CTRL+Z` then `Enter` (on Windows) to signal the end of your input.
    4.  The AI will return a refactored version of your code.

*   **Example:**
    *   **Your Input (a messy Python function):**
        ```python
        def f(l):
          x=[]
          for i in l:
            if i%2==0:
              x.append(i*2)
          return x
        ```
    *   **AI Output (a clean, Pythonic version):**
        ```python
        def double_evens(numbers: list) -> list:
            """Doubles the even numbers in a list."""
            return [num * 2 for num in numbers if num % 2 == 0]
        ```

#### 4. 🔍 Smart Snippet Search
Find the code you need without leaving the terminal.

*   **How to Use:**
    1.  Run `~ai` and select "Snippet Search".
    2.  Describe the functionality you're looking for.
    3.  The AI will provide a relevant code snippet.

*   **Example:**
    *   **Your Input:** `how to read a json file in python`
    *   **AI Output:**
        ```python
        import json

        def read_json_file(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        ```

---

## ✨ A More Intuitive and Dynamic UI

We've polished the user interface to make your time in PyShell more productive and enjoyable.

*   **Live Suggestions Toolbar:** The subtle toolbar at the bottom of the prompt is your new best friend. It provides real-time syntax hints and auto-completions as you type, guiding you to the right command without being intrusive.
*   **Interactive Menus:** Navigating menus (like the `stats` menu and the main `AI Panel`) is now fluid and intuitive. Use your **arrow keys** for selection and **Enter** to confirm. No more typing numbers and hitting enter repeatedly.
*   **Vibrant Startup Sequence:** The new 16-color wave animation isn't just for show. It's a statement that your terminal can be both powerful and beautiful, setting a modern, cyberpunk-inspired tone for your session.

---

This is just the beginning. With a powerful local AI at its core, PyShell is poised to become an indispensable part of your development toolkit. We're excited for you to try it out! 