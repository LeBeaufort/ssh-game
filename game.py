import curses
from bigtext import *



in_menu = True
current_button = 0


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    center_y = round(curses.COLS / 2)
    center_x = round(curses.LINES / 2)

    print(center_y, center_x)
    print(curses.COLS, curses.LINES)

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    if curses.COLS < 200 or curses.LINES < 61:
        stdscr.addstr(0, 0, 'Your terminal seems too little to play this game, you should get a bigger one !',
                      curses.color_pair(1))

    # display the intro
    stdscr.addstr(1, center_y - 39, intro, curses.color_pair(2))

    stdscr.addstr(10, 39, play, curses.color_pair(3))
    stdscr.addstr(20, 39, exitmsg, curses.color_pair(3))

    while True:
        key = stdscr.getkey()
        if key == " ":
            pass
            # stuff to run the game
        elif key == '\x1b':
            exit()

        # refreshing stuff
        stdscr.refresh()
        stdscr.getch()


curses.wrapper(main)
