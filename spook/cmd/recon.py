import os
import time
from typing import Optional
import typer
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.status import Status

from spook.ports import PortRange


def handle(
    target: Optional[str] = typer.Option(None, help="Target IP or domain"),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    icallback: Optional[bool] = typer.Option(
        False, "--icallback", "-i", help="<internal> Enable interactive callback"
    ),
    console: Optional[Console] = typer.Option(
        None, help="<internal> Rich Console instance"
    ),
):
    """Information Gathering and Reconnaissance Mode"""

    # Initialize state
    state = {
        "target": target,
        "verbose": verbose,
        "ports": "1-1000",
        "threads": "10",
        "status": "idle",
        "logs": [],  # Store recent log messages
    }

    def create_display(state):
        """Create the full display with panel"""
        status_color = {"idle": "yellow", "scanning": "green", "complete": "cyan"}.get(
            state["status"], "white"
        )

        panel_content = (
            f"[bold green]Target:[/bold green] {state['target'] or 'Not set'}\n"
            f"[bold magenta]Verbose:[/bold magenta] {'✓ Enabled' if state['verbose'] else '✗ Disabled'}\n"
            f"[bold yellow]Port Range:[/bold yellow] {state['ports']}\n"
            f"[bold cyan]Threads:[/bold cyan] {state['threads']}\n"
            f"[bold {status_color}]Status:[/bold {status_color}] {state['status']}\n\n"
            f"[dim]Commands: target, ports, threads, verbose (v), scan (s), quit (q)[/dim]"
        )

        return Panel(
            panel_content, title="🔍 Reconnaissance Mode", border_style="green"
        )

    SCANNING = False

    console = console or Console()

    if target is not None or icallback:
        console.clear()

        with Live(
            create_display(state), refresh_per_second=4, console=console, screen=False
        ) as live:

            while not SCANNING:
                try:
                    live.stop()
                    cmd = (
                        Prompt.ask("[bold white]recon[/bold white]", default="scan")
                        .lower()
                        .strip()
                    )
                    live.start()
                    os.system("clear" if os.name != "nt" else "cls")
                    live.update(create_display(state))

                    if cmd == "quit" or cmd == "q":
                        break

                    elif cmd == "target":
                        live.stop()
                        state["target"] = Prompt.ask("[green]Enter target")
                        console.clear()
                        live.start()
                        live.update(create_display(state))

                    elif cmd == "ports":
                        live.stop()
                        console.log(
                            "E.g., '1-1000' (Default), '22,80,443' (Comma-separated list), '1-' (All ports)"
                        )
                        state["ports"] = Prompt.ask(
                            "[yellow]Enter port range",
                            default="1-1000",
                        )
                        console.clear()
                        live.start()
                        live.update(create_display(state))

                    elif cmd == "threads":
                        live.stop()
                        state["threads"] = Prompt.ask(
                            "[cyan]Enter thread count", default="10"
                        )
                        console.clear()
                        live.start()
                        live.update(create_display(state))

                    elif cmd == "verbose" or cmd == "v":
                        state["verbose"] = not state["verbose"]
                        live.update(create_display(state))

                    elif cmd == "scan" or cmd == "s":
                        if not state["target"]:
                            console.print("[red]✗ No target specified[/red]")
                            continue

                        # get state["ports"] into a PortRange object
                        port_range = PortRange.parse(state["ports"])

                        console.print(
                            f"[bold green]✓[/bold green] Starting scan on [bold]{state['target']}[/bold] for ports [bold]{port_range}[/bold] with [bold]{state['threads']}[/bold] threads."
                        )
                        SCANNING = True
                        scan_status = Status(
                            "[bold white]Scanning in progress...[/bold white]",
                            spinner="bouncingBar",
                        )
                        scan_status.start()

                        # Simulate scan
                        time.sleep(10)

                        scan_status.stop()

                        SCANNING = False

                        state["status"] = "idle"
                        live.update(create_display(state))

                    else:
                        live.stop()
                        console.print(f"[red]Unknown command: {cmd}[/red]")
                        live.start()

                except KeyboardInterrupt:
                    break

    else:
        console.print(
            "[yellow]No target specified. Use -i for interactive mode.[/yellow]"
        )
