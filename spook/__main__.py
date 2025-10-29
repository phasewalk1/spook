import os
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.panel import Panel
from loguru import logger
import typer

import spook.candy as candy
from spook.modes import Mode

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True,
)

console = Console()
app = typer.Typer(add_completion=False)


@app.command()
def scripts(
    script: Optional[str] = typer.Argument(None, help="Script name to run"),
    target: Optional[str] = typer.Option(None, help="Target IP or domain"),
    icallback: Optional[bool] = typer.Option(
        False, "--icallback", "-i", help="<internal> Enable interactive callback"
    ),
):
    import spook.cmd.scripts as cmd

    cmd.handle(script, target, icallback, console)


@app.command()
def recon(
    target: Optional[str] = typer.Option(None, help="Target IP or domain"),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    icallback: Optional[bool] = typer.Option(
        False, "--icallback", "-i", help="<internal> Enable interactive callback"
    ),
):
    import spook.cmd.recon as cmd

    cmd.handle(target, verbose, icallback, console)


@app.command()
def expl(
    target: Optional[str] = typer.Argument(None, help="Target IP or domain"),
    exploit: Optional[str] = typer.Option(
        None, "--exploit", "-e", help="Exploit module to use"
    ),
):
    """Exploitation and Post-Exploitation Tools"""
    logger.info("Starting exploitation mode")

    if target:
        console.print(
            Panel(
                f"[bold red]Target:[/bold red] {target}\n"
                f"[bold yellow]Exploit:[/bold yellow] {exploit or 'Not specified'}",
                title="🔥 Exploitation Mode",
                border_style="red",
            )
        )
        # TODO:
        # i'll impl this later ...
    else:
        console.print(
            "[yellow]No target specified. Run with --help for usage.[/yellow]"
        )


@app.command()
def lateral(
    target: Optional[str] = typer.Argument(None, help="Target IP or domain"),
):
    """Lateral Movement and Privilege Escalation Tools"""
    logger.info("Starting lateral movement mode")

    if target:
        console.print(f"[bold cyan]Lateral Movement:[/bold cyan] {target}")
        # TODO:
        # i'll impl this later ...
    else:
        console.print(
            "[yellow]No target specified. Run with --help for usage.[/yellow]"
        )


@app.command()
def interactive():
    """Start interactive mode"""
    console.print("[bold red]Welcome to Spook Interactive Mode![/bold red]")
    mode = console.input(
        "[bold white]mode> [/bold white] "
    )

    ICALLBACK = True
    SPOOK_VERBOSE = True
    TARGET = os.environ.get("TARGET")
    while mode != "q":
        if Mode.parse(mode):
            mode = Mode.parse(mode)
            console.print(f"\n[bold green]✓[/bold green] Selected: [cyan]{mode}[/cyan]")

            if mode == Mode.RECON:
                recon(TARGET, SPOOK_VERBOSE, ICALLBACK)
            elif mode == Mode.SCRIPTS:
                scripts(None, TARGET, ICALLBACK)
            elif mode == Mode.EXPL:
                expl()
            elif mode == Mode.LATERAL:
                lateral()
        else:
            console.print(f"[bold red]✗[/bold red] Invalid mode: {mode}")
            logger.error(f"Invalid mode selected: {mode}")

        candy.show_banner(console)
        candy.show_modes_table(console)
        mode = console.input(
            "\n[bold white]mode> [/bold white] "
        )



@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """spook - A collection of red-teaming tools, scripts, and workflows."""
    if ctx.invoked_subcommand is None:
        candy.show_banner(console)
        candy.show_modes_table(console)
        interactive()
    elif ctx.invoked_subcommand == "recon":
        logger.info("Recon mode selected from main callback")
    elif ctx.invoked_subcommand == "expl":
        logger.info("Exploitation mode selected from main callback")
    elif ctx.invoked_subcommand == "lateral":
        logger.info("Lateral movement mode selected from main callback")
    else:
        logger.warning(f"Unknown subcommand: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()
