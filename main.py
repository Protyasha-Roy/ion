import os
import subprocess
import platform
import re
import json

from google import genai
from google.genai import types, errors
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn

# ── CONFIG ─────────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
CTX_FILE   = "system_context.json"

console = Console()
if not API_KEY:
    console.print("[bold red] ERROR: No API key found![/bold red] "
                  "Set GEMINI_API_KEY in your environment or in a .env file.")
    exit(1)
# ────────────────────────────────────────────────────────────────────────────────

install()  # Rich pretty tracebacks

def build_context_file(filename=CTX_FILE):
    from pathlib import Path

    def find_executables(start_paths):
        executables = {}
        for base in start_paths:
            if not os.path.isdir(base):
                continue
            for root, _, files in os.walk(base):
                for f in files:
                    if f.lower().endswith(".exe"):
                        executables[f.lower()] = os.path.join(root, f)
        return executables

    def get_user_folders():
        home = Path.home()
        folders = {
            "desktop": home / "Desktop",
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "pictures": home / "Pictures",
            "videos": home / "Videos",
            "music": home / "Music",
        }
        return {k: str(v) for k, v in folders.items() if v.exists()}

    paths_to_scan = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
        os.path.expandvars(r"%APPDATA%"),
    ]
    context = {
        "apps": find_executables(paths_to_scan),
        "folders": get_user_folders()
    }
    with open(filename, "w") as f:
        json.dump(context, f, indent=4)
    return filename

def load_context_text():
    if not os.path.exists(CTX_FILE):
        return ""
    with open(CTX_FILE, "r") as f:
        ctx = json.load(f)
    lines = []
    for app, path in ctx.get("apps", {}).items():
        lines.append(f"{app} = {path}")
    for name, path in ctx.get("folders", {}).items():
        lines.append(f"{name} folder = {path}")
    return "\n".join(lines)

client = genai.Client(api_key=API_KEY)
with Progress(
    SpinnerColumn(style="bold magenta"),
    TextColumn("[bold cyan]Building context map..."),
    transient=True,
) as progress:
    progress.add_task("ctx", total=None)
    build_context_file()
    console.print("[bold green]✅ Context map ready![/bold green]")

def get_command_from_gemini(user_input: str) -> str:
    system_os    = platform.system()
    shell_prefix = "powershell -Command" if system_os == "Windows" else "bash -c"
    context_text = load_context_text()

    prompt = (
        "You are an AI assistant that generates precise and real shell commands for the user's current operating system.\n"
        "You MUST only use verified paths and application names from the context below. DO NOT hallucinate or guess any file paths or program names.\n"
        "All returned commands must follow correct syntax for the current OS and be directly executable.\n\n"
        "🧠 RULES:\n"
        "- Only output a single raw command, no explanation, markdown, backticks, or comments.\n"
        "- If on Windows:\n"
        "  • Use powershell -Command \"<command>\"\n"
        "  • Always wrap file paths in single quotes inside the command string (e.g. 'C:\\Path With Spaces')\n"
        "  • Use Start-Process -FilePath '...' to open apps\n"
        "  • Use Stop-Process -Name appname -Force to close apps\n"
        "  • Use Get-ChildItem with -Path '...' when scanning folders\n"
        "- If on Linux/macOS:\n"
        "  • Use bash -c \"<command>\"\n"
        "  • Use open (macOS) or xdg-open (Linux) to launch apps or files\n\n"
        f"Current OS: {system_os}\n"
        f"Environment Context:\n{context_text}\n\n"
        f"User Request: {user_input}"
    )

    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    config   = types.GenerateContentConfig(response_mime_type="text/plain")

    try:
        cmd = ""
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=contents, config=config
        ):
            cmd += chunk.text
        return cmd.strip() or "No response from AI."
    except errors.ClientError as e:
        if e.status_code == 429:
            return "__QUOTA_EXCEEDED__"
        if e.status_code == 400 and "API key not valid" in str(e):
            return "__INVALID_KEY__"
        return f"Error: {e}"

def is_safe_command(cmd: str) -> bool:
    patterns = [
        r"\brm\s+-rf\b", r"\bsudo\b", r"\bshutdown\b", r"\breboot\b", r"&&\s*rm\b",
    ]
    return not any(re.search(p, cmd) for p in patterns)

def main():
    console.print(Panel("[bold blue] ION[/bold blue]", expand=False, subtitle="Type commands like a boss"))
    while True:
        user_input = Prompt.ask("[bold green]Ask me to do something[/bold green] (or 'exit')").strip()
        if user_input.lower() in ("exit", "quit"):
            console.print("[bold red] Goodbye![/bold red]")
            break

        with Progress(
            SpinnerColumn(style="bold magenta"),
            TextColumn("[bold cyan]Generating command..."),
            transient=True,
        ) as progress:
            progress.add_task("gen", total=None)
            command = get_command_from_gemini(user_input)

        if command == "__QUOTA_EXCEEDED__":
            console.print("[bold red] Quota exceeded! Try again later.[/bold red]")
            continue
        if command == "__INVALID_KEY__":
            console.print("[bold red] Invalid API key! Update your key.[/bold red]")
            break
        if command.startswith("Error:"):
            console.print(f"[bold red]{command}[/bold red]")
            continue

        console.print(Panel.fit(f"[cyan]{command}[/cyan]", title="Command to execute"))

        if not Confirm.ask("⚡ Execute?", default=False):
            console.print("[bold yellow]  Canceled.[/bold yellow]")
            continue

        if is_safe_command(command):
            with console.status("[bold green]⚙️  Executing...[/bold green]", spinner="dots"):
                try:
                    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                    console.print("[bold green] Successfully executed.[/bold green]")
                    if result.stdout:
                        console.print(Panel(result.stdout.strip(), title="Output"))
                    if result.stderr:
                        console.print(Panel(result.stderr.strip(), title="Error Output", style="bold red"))
                except subprocess.CalledProcessError as e:
                    console.print(f"[bold red]Execution error:[/bold red] {e}")
        else:
            console.print("[bold red] Unsafe command blocked![/bold red]")

if __name__ == "__main__":
    main()
