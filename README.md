# Linux Services Manager

A terminal-based system services dashboard and management tool built with Python and Rich.

## Features

* **List Services**: Display all systemd services with status, colorized and sorted (running first).
* **Manage a Service**:

  * Start, Stop, Restart, Disable
  * View logs via `journalctl` (last 100, follow live, since boot, errors)
  * Fallback to raw syslog (`/var/log/syslog` or `/var/log/messages`)
* **Find a Service**: Search by keyword in unit name or description, view details and unit file location.

## Prerequisites

* Python 3.6+
* [Rich](https://github.com/Textualize/rich) library
* Systemd (Linux distribution with `systemctl` & `journalctl`)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/linux-services-manager.git
   cd linux-services-manager
   ```

2. **Install dependencies**

   ```bash
   pip install rich
   ```

3. **Make script executable**

   ```bash
   chmod +x main.py
   ```

## Usage

Run the dashboard:

```bash
python3 main.py
```

You will be presented with a main menu:

1. **List all services** — Shows a colorized table of all services and their statuses.
2. **Manage a service** — Enter a submenu to control a specific service or view logs.
3. **Find a service** — Search for services by keyword and view details.
4. **Exit** — Quit the application.

### Manage a Service

After selecting a service, choose from:

* Start, Stop, Restart, Disable
* View last 100 `journalctl` entries
* Follow live logs (`journalctl -f`)
* View logs since last boot
* View only error logs
* Tail raw `/var/log/syslog` or `/var/log/messages`

### Find a Service

Search by keyword to list matching units, then view `systemctl status` and the service unit file path.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/XYZ`).
3. Make your changes and commit (`git commit -m 'Add XYZ feature'`).
4. Push to your branch (`git push origin feature/XYZ`).
5. Open a Pull Request.

