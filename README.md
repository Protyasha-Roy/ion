# Ion - AI-powered CLI Assistant

## Overview

Ion is a CLI-based AI-powered assistant that executes OS-level commands based on natural language input. Users can install it and use their own API keys for execution. Ion supports Windows, macOS, and Linux, making it a versatile tool for streamlining command-line operations.

## Features

- Generates shell commands using Google's Gemini API.
- Compatible with Windows, macOS, and Linux.
- Runs locally with user-provided API keys.
- Automatically detects installed applications and user directories.
- Provides a safe execution environment with command validation.

## Installation

To install Ion, use the following command:
You'll need to install python, and pip before running the pip command.
After installing both, go to your terminal and type/copy paste the command below.

```sh
pip install ion
```


### Setup

Before running Ion, you need to configure your API key and model:

1. **Obtain a Gemini API Key:**

   - Go to [Google AI](https://ai.google.dev) and sign in.
   - Navigate to API Keys and generate a new key.
   - Copy the API key for later use.

2. **Set Up Your Environment File:**

   - Locate the `.env.example` file in the repository.
   - Rename it to `.env`.
   - Open the `.env` file and update it with your API key and model:
     ```sh
     API_KEY=your_google_api_key
     MODEL=gemini-1.5-flash
     ```
   - Save the file.

3. **Run the Assistant:**

   ```sh
   ion
   ```

## Usage

Once Ion is running, you can use it to execute commands with natural language input:

```sh
$ ion
🤖 AI Shell Assistant
> Open Chrome
> Run VS Code
> Find my downloads folder
```

Ion will generate a corresponding system command and prompt you to confirm execution.

### Example Commands

```sh
> Open Notepad
   → Generated Command: `powershell -Command "Start-Process notepad.exe"`

> Show my desktop folder
   → Generated Command: `powershell -Command "Get-ChildItem -Path 'C:\Users\YourName\Desktop'"`
```

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Open a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [GPL-3.0 + Non-Commercial Clause](LICENSE).

It is free to use for personal and non-commercial purposes only.

