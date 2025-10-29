import rich.box as box
from rich.console import Console
from rich.table import Table

from spook.modes import MODES

spook_logo = r"""
    ▒▒▒░░░░░░░░░░▄▐░░░░                                 spook
    ▒░░░░░░▄▄▄░░▄██▄░░░                                 -----
    ░░░░░░▐▀█▀▌░░░░▀█▄░       A collection of red-teaming tools, scripts, and workflows.
    ░░░░░░▐█▄█▌░░░░░░▀█▄
    ░░░░░░░▀▄▀░░░▄▄▄▄▄▀▀
    ░░░░░▄▄▄██▀▀▀▀░░░░░
    ░░░░█▀▄▄▄█░▀▀░░░░░░
    ░░░░▌░▄▄▄▐▌▀▀▀░░░░░
    ░▄░▐░░░▄▄░█░▀▀░░░░░             
    ░▀█▌░░░▄░▀█▀░▀░░░░░
    ░░░░░░░░▄▄▐▌▄▄░░░░░
    ░░░░░░░░▀███▀█░▄░░░
    ░░░░░░░▐▌▀▄▀▄▀▐▄░░░
    ░░░░░░░▐▀░░░░░░▐▌░░
    ░░░░░░░█░░░░░░░░█░░                  Author: Ethan Gallucci <phasewalk1>
    ░░░░░░▐▌░░░░░░░░░█░                      Version Info: v0.1.0-alpha
"""


def show_banner(console: Console):
    """Display the Spook banner"""
    console.print(spook_logo, style="bold red")


def show_modes_table(console: Console):
    """Display available modes in a beautiful table"""
    table = Table(
        title="Available Modes",
        box=box.MINIMAL_HEAVY_HEAD,
        show_header=True,
        header_style="bold red",
    )

    table.add_column("Mode", style="white", width=12)
    table.add_column("Description", style="white")

    for mode, description in MODES.items():
        table.add_row(mode, description)

    console.print(table)
