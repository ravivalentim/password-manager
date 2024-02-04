def menu():
    from rich.console import Console

    style = 'bold black'

    console = Console()
    console.print("[1] Add a new item 🔐", style=style)
    console.print("[2] View item 🔓", style=style)
    console.print("[3] Delete item ❌", style=style)
    console.print("[4] Exit ✌️", style=style)