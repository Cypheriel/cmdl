"""Simple test for an `add` command."""
import pytest
from cmdl import CommandLine

cmdl = CommandLine()


@cmdl.register(name="add", aliases=["sum"], description="Add arguments as integers.")
def add_command(*args: int) -> None:
    """Add arguments as integers."""
    print(sum(args), end="")


def test_add_command(capfd: pytest.CaptureFixture) -> None:
    """Test `add` command. Should return the sum of arguments."""
    cmdl.execute("add 1 2 3")
    out, err = capfd.readouterr()
    print(type(capfd))
    assert out == "6"
