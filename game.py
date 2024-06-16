import curses
from bigtext import *
import datetime
from time import sleep


def main(stdscr):
    in_menu = True

    stdscr.nodelay(True)  # make stdscr.getkey() non-blocking
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    center_y = round(curses.COLS / 2)
    center_x = round(curses.LINES / 2)

    if curses.COLS < 200 or curses.LINES < 61:
        stdscr.addstr(0, 0, 'Your terminal seems too little to play this game, you should get a bigger one !',
                      curses.color_pair(1))

    while True:

        #  get key input
        try:
            key = stdscr.getkey()
        except:
            key = None

        # do something with it
        if key == " ":
            in_menu = False
            # stuff to run the game
        elif key == '\x1b': # if the user press escape, we leave the game
            curses.endwin()
            exit()

        print(f"[{datetime.datetime.now()}] We reached the end !")

        #  cleaning old text and displaying new one
        stdscr.clear()
        if in_menu:
            # display the intro
            stdscr.addstr(1, center_y - 39, intro, curses.color_pair(2))

            stdscr.addstr(10, 39, play, curses.color_pair(3))
            stdscr.addstr(20, 39, exitmsg, curses.color_pair(3))
        else:
            pass
            # todo : game here

        # refreshing stuff
        stdscr.refresh()
        stdscr.getch()
        sleep(0.1)


curses.wrapper(main)
