# Ion - AI-powered CLI Assistant

## Overview

Ion is a CLI-based AI-powered assistant that executes OS-level commands based on natural language input. Users can install it and use their own API keys for execution. Ion supports Windows, macOS, and Linux, making it a versatile tool for streamlining command-line operations.

## Features

Give it any task to do, it will generate commands to execute the task. Works well with gemini-1.5-flash model. But works better with gemini 2.5-pro model.
Some prompt(task) examples to give:
- Open/close 'app name'.
- Close all opened apps at once.
- What's the filename of the first image in downloads?
- Search teapot on google.
- Go to chatgpt.com in brave browser.
- And anything you wish it to do. 

In future I will be integrating a better file/folder indexing system. Memory management, so it remembers previous texts in the same conversation.
And hoping to create a GUI popup for it with speech recognition as well.

## Installation

To use Ion you need to download and install python. During installation make sure to check the 'ADD TO PATH' option. After installing python, go to your terminal and type/copy paste the command below.

```sh
pip install ion
```

### Setup

Before running Ion, you need to configure your API key and model:

1. **Obtain a Gemini API Key:**

   - Go to [Google AI Studio](https://aistudio.google.com/apikey) and sign in.
   - Generate an API-key here.
   - Copy and the API key for later use.

2. **Set Up Your Environment File:**

   - Locate the `.env.example` file in the repository(in the folder you installed ion).
   - Rename it to `.env`.
   - Open the `.env` file and update it with your API key and model:
     ```sh
     API_KEY=your_google_api_key
     MODEL=gemini-1.5-flash
     ```
   - Save the file.

You can replace the model to be gemini 2.5 pro with your own api key as well.

3. **Run the Assistant:**
Now go to the terminal again and type:
   ```sh
   ion
   ```

## Usage

Once Ion is running, you can use it to execute commands with natural language input:

```sh
$ ion
 AI Shell Assistant
> Open Chrome
> Run VS Code
> Find 'folder name'
> Create a new note in notepad++
> Anything you can think of...
```

Ion will generate a corresponding system command and prompt you to confirm execution.
Click 'y' for accepteing the command and 'n' for cancelling the command.

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

Will not be able to accept contributions until next month.

## License

This project is licensed under the [GPL-3.0 + Non-Commercial Clause](LICENSE).

It is free to use for personal and non-commercial purposes only.