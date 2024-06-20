import curses
from bigtext import *
import datetime
from time import sleep
from curses.textpad import rectangle


snake = []


def main(stdscr):
    in_menu = True

    GAME_SIZE_X = 58
    GAME_SIZE_Y = 25

    stdscr.nodelay(True)  # make stdscr.getkey() non-blocking
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    if curses.COLS < 200 or curses.LINES < 61:
        stdscr.addstr(0, 0, 'Your terminal seems too little to play this game, you should get a bigger one !',
                      curses.color_pair(1))

    #  so we are sure to do not display anything outside an area
    game_window = curses.newwin(GAME_SIZE_Y, GAME_SIZE_X, 3, 3)

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
        elif key == '\x1b':  # if the user press escape, we leave the game
            curses.endwin()
            exit()

        #  cleaning old text and displaying new one
        stdscr.clear()
        if in_menu:
            # display the intro
            stdscr.addstr(1, 0, intro, curses.color_pair(2))
            stdscr.addstr(10, 0, play, curses.color_pair(3))
            stdscr.addstr(20, 0, exitmsg, curses.color_pair(3))
        else:
            try:
                rectangle(game_window, 0, 0, GAME_SIZE_Y-1, GAME_SIZE_X-1)
            except:
                pass
            # https://stackoverflow.com/questions/52804155/extending-curses-rectangle-box-to-edge-of-terminal-in-python

        # displaying the where source code is
        stdscr.addstr(0, 0, "Source code available on https://github.com/LeBeaufort/ssh-game", curses.color_pair(4))

        # refreshing stuff
        stdscr.refresh()
        game_window.refresh()  # we need it
        stdscr.getch()
        sleep(0.1)


curses.wrapper(main)
