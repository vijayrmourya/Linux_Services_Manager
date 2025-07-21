#!/usr/bin/env python3
import curses
import subprocess

def main(stdscr):
    # hide the cursor
    curses.curs_set(0)

    menu = [
        'Monitor services on my system',
        'Get Service logs',
        'Exit'
    ]
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # draw title
        title = 'Linux Services Manager'
        stdscr.addstr(1, w // 2 - len(title) // 2, title, curses.A_BOLD)

        # draw menu options
        for idx, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

        key = stdscr.getch()
        # navigate
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in (curses.KEY_ENTER, ord('\n')):
            # Exit
            if current_row == len(menu) - 1:
                break

            # Monitor services on my system
            if current_row == 0:
                stdscr.clear()
                stdscr.addstr(0, 0, 'Services status:')
                # Fetch all services and statuses
                proc = subprocess.run(
                    ['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--no-legend'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                lines = proc.stdout.splitlines()
                max_y, max_x = stdscr.getmaxyx()
                per_page = max_y - 2  # leave one line for header and one for prompt

                # Paginate through service list
                for start in range(0, len(lines), per_page):
                    stdscr.clear()
                    stdscr.addstr(0, 0, 'Services status:')
                    chunk = lines[start:start + per_page]
                    for idx_line, line in enumerate(chunk):
                        stdscr.addstr(idx_line + 1, 0, line[:max_x - 1])
                    stdscr.addstr(max_y - 1, 0, 'Press any key for next page or q to quit')
                    stdscr.refresh()
                    c = stdscr.getch()
                    if c in (ord('q'), ord('Q')):
                        break

            # Get Service logs
            elif current_row == 1:
                stdscr.clear()
                stdscr.addstr(0, 0, '→ Getting Service logs...')
                stdscr.addstr(2, 0, 'Press any key to return…')
                stdscr.refresh()
                stdscr.getch()

    # clean up
    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
