```python
#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import subprocess
import sys

console = Console()

def list_services():
    """Fetch and display all system services with their status."""
    proc = subprocess.run(
        ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--no-legend"],
        capture_output=True,
        text=True
    )
    lines = proc.stdout.splitlines()
    table = Table(title="Services Status")
    table.add_column("UNIT", no_wrap=True)
    table.add_column("LOAD")
    table.add_column("ACTIVE")
    table.add_column("SUB")
    table.add_column("DESCRIPTION", overflow="fold")

    for line in lines:
        parts = line.split(None, 4)
        if len(parts) == 5:
            unit, load, active, sub, desc = parts
            table.add_row(unit, load, active, sub, desc)

    console.print(table)


def get_service_logs():
    """Prompt the user for a service name and display its recent logs."""
    service = Prompt.ask("Enter the service unit name (e.g., ssh.service)")
    proc = subprocess.run(
        ["journalctl", "-u", service, "--no-pager", "-n", "20"],
        capture_output=True,
        text=True
    )
    console.print(f"\n[bold green]Last 20 log lines for [yellow]{service}[/]:[/]\n")
    console.print(proc.stdout)


def main():
    menu = {
        "1": ("Monitor services on my system", list_services),
        "2": ("Get service logs", get_service_logs),
        "3": ("Exit", None),
    }

    while True:
        console.print("\n[bold cyan]Golem_541 - Linux Services Manager[/]\n")
        for key, (desc, _) in menu.items():
            console.print(f"[green]{key}.[/] {desc}")
        choice = Prompt.ask("\nSelect an option", choices=list(menu.keys()))

        if choice == "3":
            console.print("Exiting. Goodbye!")
            sys.exit(0)

        _, action = menu[choice]
        console.clear()
        try:
            action()
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
        console.print("\nPress Enter to continue...", style="dim")
        input()
        console.clear()


if __name__ == '__main__':
    main()
```
