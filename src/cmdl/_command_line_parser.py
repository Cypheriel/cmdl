from abc import ABCMeta
from inspect import signature, Parameter
from shlex import split
from types import NoneType
from typing import Optional, Callable, Any, Mapping, get_origin, Union, get_args, Iterable

from rich.console import Console

from ._exceptions import ArgumentError

console = Console()


def convert_args(parameters: Mapping[str, Parameter], *args: str) -> Iterable[Any]:
    """
    Convert `args` to type annotations of `parameters`.

    :param parameters: Mapping of `Parameter`s from `inspect.Signature.parameters`.
    :param args: Command arguments as strings.
    :return: Iterable containing converted arguments.
    """

    def converter():
        param_type = None
        for param in parameters.values():
            param_type = param.annotation
            type_origin = get_origin(param_type)
            type_args = get_args(param_type)

            if type_origin == Union and len(type_args) == 2 and type_args[1] == NoneType:
                param_type = type_args[0]

            yield param_type

        while param_type is not None:
            yield param_type

    try:
        return iter(new_type(s) for s, new_type in zip(args, converter()))

    except ValueError:
        raise ArgumentError("Invalid arguments.")


class Alias(str):
    pass


class Command(Callable, metaclass=ABCMeta):
    name: str
    description: str
    aliases: list[str]

    def __call__(self, *args, **kwargs):
        pass


class CommandLine:
    def __init__(self):
        self.commands: dict[str, Command] = {}

    def register(self, name: str, description: str, aliases: Optional[list[str]] = None):
        if aliases is None:
            aliases = []

        def decorator(command: Command):
            command.name = name
            command.description = description
            command.aliases = aliases

            self.commands[name] = command
            for alias in command.aliases:
                self.commands[Alias(alias)] = command

            return command

        return decorator

    def execute(self, command: str):
        args: list[str] = split(command, comments=True)
        command = self.commands.get(args[0].lower())

        if command:
            try:
                converted_args = convert_args(signature(command).parameters, *args[1:])
                command(*converted_args)

            except ArgumentError:
                console.print("[red]Error[/]: Invalid arguments.")

        else:
            console.print(f"[red]Error[/]: Invalid command '{command}'.")

        print()
