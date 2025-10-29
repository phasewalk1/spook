import os
from typing import Optional
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt


def handle(
    script: Optional[str],
    target: Optional[str],
    icallback: Optional[bool],
    console: Optional[Console],
):
    console = console or Console()
    scripts = [
        ("listener.py", "Reverse shell listener"),
        ("scanner.py", "Port scanner"),
        ("bruteforce.py", "Brute force attack tool"),
    ]
    script_list = "\n".join([f"- {name} ({desc})" for name, desc in scripts])
    panel = Panel(
        f"[bold yellow]Available Scripts:[/bold yellow]\n\n{script_list}",
        title="🛠️ Script Manager",
        border_style="yellow",
    )
    console.print(panel)
    script = Prompt.ask("run> ", default="listener.py", choices=[name for name, _ in scripts])
    if script == "listener.py":
        port = Prompt.ask("listen on port> ", default="9001")
        # execute the script with output
        os.system(f"uv run scripts/{script} {port}")



    console.print(f"[bold green]Running {script}...[/bold green]")
