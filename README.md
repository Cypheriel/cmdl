<div style="text-align: center;"><h1>cmdl</h1></div>
<hr>

`cmdl` is a command-line parser written in Python.

<h3>Information</h3>
`cmdl` makes use of type annotations to convert command-line arguments (as strings) into the specified type.
If this cannot be done automatically, the type remains a string.

<h3>Usage</h3>

```python3
from cmdl import CommandLine

cmdl = CommandLine()


@cmdl.register(name="add", aliases=["sum"], description="Add arguments as numbers.", )
def add_command(*args: int) -> None:
    # Note the annotations of `*args: int`.
    # Here, the args are converted to `int` (from `str`) automatically.
    print(f"Sum: {sum(args)}")

    
if __name__ == "__main__":
    while True:
        cmdl.execute(input("Enter a command:\n$ "))
```
