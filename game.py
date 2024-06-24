import curses
from bigtext import *
from time import sleep
from curses.textpad import rectangle

default_snake = [(9, 3), (9, 4), (9, 5)]
snake = [(9, 3), (9, 4), (9, 5)]
direction = 0  # 0 --> UP ; 1 --> LEFT ; 2 --> DOWN ; 3 --> RIGHT


def update_direction(new_key):
    global direction
    print(f"Direction is {direction}")
    if new_key == "UP" and direction != 2:
        direction = 0
    elif new_key == "LEFT" and direction != 3:
        direction = 1
    elif new_key == "DOWN" and direction != 0:
        direction = 2
    elif new_key == "RIGHT" and direction != 1:
        direction = 3
    print(f"Now it is [{direction}")


def display_snake(window):
    global snake
    for x, y in snake:
        for a in range(4):
            for b in range(4):
                window.addstr(y * 4 + a, x * 4 + b, "#", curses.color_pair(5))


def update_snake():
    global direction
    global snake
    headx = snake[0][0]
    heady = snake[0][1]
    if direction == 0:
        heady -= 1
    elif direction == 1:
        headx += 1
    elif direction == 2:
        heady += 1
    else:
        headx -= 1

    snake.insert(0, (headx, heady))
    snake.pop(len(snake)-1)


def main(stdscr):
    global snake, default_snake
    in_menu = True

    GAME_SIZE_X = 68
    GAME_SIZE_Y = 28

    stdscr.nodelay(True)  # make stdscr.getkey() non-blocking
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)

    if curses.COLS < 200 or curses.LINES < 61:
        stdscr.addstr(0, 0, 'Your terminal seems too little to play this game, you should get a bigger one !',
                      curses.color_pair(1))

    #  so we are sure to do not display anything outside an area
    game_window = curses.newwin(GAME_SIZE_Y, GAME_SIZE_X, 2, 3)

    while True:

        #  get key input
        try:
            key = stdscr.getkey()
        except:
            key = None

        # do something with it
        if key == " ":
            in_menu = False
            snake = default_snake.copy()
        elif key == '\x1b':  # if the user press escape, we leave the game
            curses.endwin()
            exit()
        # stuff to update the direction of the snake
        elif key == curses.KEY_UP:
            print("HELLOOOOOOOOO")
            update_direction("UP")
        elif key == curses.KEY_DOWN:
            update_direction("DOWN")
        elif key == curses.KEY_LEFT:
            update_direction("LEFT")
        elif key == curses.KEY_RIGHT:
            update_direction("RIGHT")

        #  cleaning old text and displaying new one
        stdscr.clear()

        if in_menu:
            # display the intro
            stdscr.addstr(1, 0, intro, curses.color_pair(2))
            stdscr.addstr(10, 0, play, curses.color_pair(3))
            stdscr.addstr(20, 0, exitmsg, curses.color_pair(3))
        else:
            update_snake()
            game_window.clear()
            if snake[0][0] > GAME_SIZE_X/4 or snake[0][1] > GAME_SIZE_Y/4 or snake[0][0] <= 0 or snake[0][1] <= 0:
                game_window.addstr(int(GAME_SIZE_Y/2-5), 5, gameover, curses.color_pair(1))
                in_menu = True
            else:
                display_snake(game_window)

            try:
                rectangle(game_window, 0, 0, GAME_SIZE_Y - 1, GAME_SIZE_X - 1)
            except:
                pass
            # https://stackoverflow.com/questions/52804155/extending-curses-rectangle-box-to-edge-of-terminal-in-python

        # displaying the where source code is
        stdscr.addstr(0, 0, "Source code available on https://github.com/LeBeaufort/ssh-game", curses.color_pair(4))

        # refreshing stuff
        stdscr.refresh()
        game_window.refresh()  # we need it
        stdscr.getch()
        sleep(0.5)


curses.wrapper(main)
