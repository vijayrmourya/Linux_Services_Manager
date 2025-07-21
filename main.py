#!/usr/bin/env python3
import curses

def main(stdscr):
    # hide the cursor
    curses.curs_set(0)

    menu = ['Option 1', 'Option 2', 'Exit']
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        # draw menu
        for idx, row in enumerate(menu):
            x = w//2 - len(row)//2
            y = h//2 - len(menu)//2 + idx
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
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key in (curses.KEY_ENTER, ord('\n')):
            # Exit
            if current_row == len(menu)-1:
                break
            # Option 1
            elif current_row == 0:
                stdscr.clear()
                stdscr.addstr(0, 0, "→ You chose Option 1!")
                stdscr.addstr(2, 0, "Press any key to return…")
                stdscr.refresh()
                stdscr.getch()
            # Option 2
            elif current_row == 1:
                stdscr.clear()
                stdscr.addstr(0, 0, "→ You chose Option 2!")
                stdscr.addstr(2, 0, "Press any key to return…")
                stdscr.refresh()
                stdscr.getch()

    # clean up
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
