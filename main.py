#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import subprocess
import sys

console = Console()

def list_all_services():
    proc = subprocess.run([
        "systemctl", "list-units", "--type=service", "--all", "--no-pager", "--no-legend"
    ], capture_output=True, text=True)
    lines = proc.stdout.splitlines()
    return lines


def list_services():
    """Fetch, sort, and display all system services with their status."""
    lines = list_all_services()

    services = []
    for line in lines:
        parts = line.split(None, 4)
        if len(parts) == 5:
            unit, load, active, sub, desc = parts
            services.append((unit, load, active, sub, desc))

    services.sort(key=lambda s: (s[2] != 'running', s[0]))

    table = Table(title="Services Status", row_styles=["", "dim"])
    table.add_column("UNIT", no_wrap=True)
    table.add_column("LOAD")
    table.add_column("ACTIVE")
    table.add_column("SUB")
    table.add_column("DESCRIPTION", overflow="fold")

    for unit, load, active, sub, desc in services:
        table.add_row(unit, load, active, sub, desc)

    console.print(table)


def find_service():
    """Allow user to search for a service by keyword, show matches, and display details."""
    keyword = Prompt.ask("Enter text to search in service names/descriptions").lower()
    lines = list_all_services()

    matches = []
    for line in lines:
        parts = line.split(None, 4)
        if len(parts) == 5:
            unit, load, active, sub, desc = parts
            if keyword in unit.lower() or keyword in desc.lower():
                matches.append((unit, load, active, sub, desc))

    if not matches:
        console.print(f"[red]No services found matching '{keyword}'.[/]")
        return

    console.print(f"\n[bold cyan]Found {len(matches)} matching services:[/]\n")
    for idx, (unit, load, active, sub, desc) in enumerate(matches, start=1):
        console.print(f"[green]{idx}.[/] {unit} ({active}) - {desc}")

    choice = Prompt.ask(
        "Select a service by number to see details or H to return",
        choices=[str(i) for i in range(1, len(matches)+1)] + ["H"]
    )
    if choice == "H":
        return
    selected = matches[int(choice)-1][0]

    console.clear()
    console.print(f"[bold cyan]Details for {selected}[/]\n")
    subprocess.run(["systemctl", "status", selected])
    path_proc = subprocess.run(
        ["systemctl", "show", selected, "--property=FragmentPath", "--no-pager"],
        capture_output=True, text=True
    )
    fragment = path_proc.stdout.strip().split('=', 1)[-1]
    console.print(f"\n[bold]Unit file:[/] {fragment}")

    console.print("\nPress Enter to return to main menu...", style="dim")
    input()

def manage_service(selected: str):
    """Service-specific management menu with enhanced log reading and fallback methods."""
    while True:
        console.clear()
        console.print(f"\n[bold cyan]{selected} Management Menu[/]\n")
        console.print("[green]1.[/] Start service")
        console.print("[green]2.[/] Stop service")
        console.print("[green]3.[/] Restart service")
        console.print("[green]4.[/] Disable service")
        console.print("[green]5.[/] View last 100 journalctl logs")
        console.print("[green]6.[/] Follow journalctl live logs")
        console.print("[green]7.[/] View journalctl logs since boot")
        console.print("[green]8.[/] View journalctl error logs")
        console.print("[green]9.[/] View raw /var/log/syslog logs")
        console.print("[green]10.[/] View raw /var/log/messages logs")
        console.print("[green]H.[/] Home (main menu)")
        console.print("[green]E.[/] Exit")

        choices = [str(i) for i in range(1, 11)] + ["H", "E"]
        choice = Prompt.ask("Enter choice", choices=choices)

        if choice == "H":
            return
        if choice == "E":
            console.print("Thanks for your time!. Goodbye!")
            sys.exit(0)

        console.clear()
        def fallback_syslog():
            console.print(f"[yellow]No journalctl output, falling back to syslog grep for {selected}[/]")
            subprocess.run(["sudo", "grep", selected, "/var/log/syslog"], check=False)

        if choice == "1":
            console.print(f"Starting {selected}…")
            subprocess.run(["sudo", "systemctl", "start", selected])
        elif choice == "2":
            console.print(f"Stopping {selected}…")
            subprocess.run(["sudo", "systemctl", "stop", selected])
        elif choice == "3":
            console.print(f"Restarting {selected}…")
            subprocess.run(["sudo", "systemctl", "restart", selected])
        elif choice == "4":
            console.print(f"Disabling {selected}…")
            subprocess.run(["sudo", "systemctl", "disable", selected])
        elif choice == "5":
            console.print(f"Showing last 100 journalctl logs for {selected}…\n")
            proc = subprocess.run(
                ["journalctl", "-u", selected, "--no-pager", "-n", "100"],
                capture_output=True,
                text=True
            )
            if proc.stdout.strip():
                console.print(proc.stdout)
            else:
                fallback_syslog()
        elif choice == "6":
            console.print(f"Following journalctl live logs for {selected}… (Ctrl+C to quit)\n")
            subprocess.run(["journalctl", "-u", selected, "-f"], check=False)
        elif choice == "7":
            console.print(f"Showing journalctl logs since boot for {selected}…\n")
            proc = subprocess.run(
                ["journalctl", "-u", selected, "--no-pager", "-b"],
                capture_output=True,
                text=True
            )
            if proc.stdout.strip():
                console.print(proc.stdout)
            else:
                fallback_syslog()
        elif choice == "8":
            console.print(f"Showing journalctl error logs for {selected}…\n")
            proc = subprocess.run(
                ["journalctl", "-u", selected, "--no-pager", "-p", "err"],
                capture_output=True,
                text=True
            )
            if proc.stdout.strip():
                console.print(proc.stdout)
            else:
                fallback_syslog()
        elif choice == "9":
            console.print(f"Showing last 100 lines of /var/log/syslog…\n")
            subprocess.run(["sudo", "tail", "-n", "100", "/var/log/syslog"], check=False)
        elif choice == "10":
            console.print(f"Showing last 100 lines of /var/log/messages…\n")
            subprocess.run(["sudo", "tail", "-n", "100", "/var/log/messages"], check=False)

        console.print("\nPress Enter to continue…", style="dim")
        input()

def check_service_details():
    """List service names, allow user to select one, then enter the management menu."""
    lines = list_all_services()

    services = [line.split(None, 1)[0] for line in lines if line.strip()]

    while True:
        console.clear()
        console.print("\n[bold cyan]Select a service to manage:[/]")
        for idx, unit in enumerate(services, start=1):
            console.print(f"[green]{idx}.[/] {unit}")
        console.print("[green]H.[/] Home (main menu)")
        console.print("[green]E.[/] Exit")

        choices = [str(i) for i in range(1, len(services) + 1)] + ["H", "E"]
        choice = Prompt.ask("Enter choice", choices=choices)

        if choice == "H":
            return
        if choice == "E":
            console.print("Thanks for your time!. Goodbye!")
            sys.exit(0)

        selected = services[int(choice) - 1]
        manage_service(selected)


def main():
    menu = {
        "1": ("List all services on system", list_services),
        "2": ("Manage a service", manage_service),
        "3": ("Find service", find_service),
        "4": ("Exit", None),
    }

    while True:
        console.clear()
        console.print("\n[bold cyan]Linux Services Manager[/]\n")
        for key, (desc, _) in menu.items():
            console.print(f"[bold green]{key}.[/] {desc}")
        choice = Prompt.ask("\nSelect an option\n", choices=list(menu.keys()))

        if choice == "4":
            console.print("Thanks for your time!. Goodbye!")
            sys.exit(0)

        action = menu[choice][1]
        console.clear()
        try:
            if choice == "2":
                check_service_details()
            else:
                action()
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
        console.print("\nPress Enter to continue...", style="dim")
        input()


if __name__ == '__main__':
    main()
