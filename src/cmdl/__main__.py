from typing import Optional

from rich.console import Console
from rich.markup import escape
from cmdl import CommandLine, Alias

cmdl = CommandLine()
console = Console()


@cmdl.register(name="help", aliases=["?"], description="Get help.")
def help_command(command_or_section: Optional[str] = None):
    if command_or_section is None:
        for name, command in cmdl.commands.items():
            if not isinstance(name, Alias):
                console.print(f"[cyan]{name}[/] - {command.description}")

    elif command := cmdl.commands.get(command_or_section):
        console.print(f"--=[[blue]{escape(command.name)}[/]]=--")
        console.print(f"[cyan]Aliases[/]: {escape(', '.join(command.aliases))}")
        console.print(f"[cyan]Description[/]: {escape(command.description)}")

    else:
        console.print(f"[red]Error[/]: Command or section `{command_or_section}` not found.")


@cmdl.register(name="add", aliases=["sum"], description="Add arguments as integers.")
def add_command(*args: int):
    console.print(f"[blue]Sum[/]: {sum(args)}")


@cmdl.register(name="exit", aliases=["quit"], description="Exits with specified status code.")
def exit_command(status_code: Optional[int] = None):
    exit(status_code or 0)


while True:
    cmdl.execute(console.input("[bright_blue]Input[/] [bright_black]»[/] "))
