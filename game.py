import curses
from bigtext import *
from time import sleep
from curses.textpad import rectangle


class Game:
    def __init__(self):
        self.default_snake = [(9, 3), (9, 4), (9, 5)]
        self.snake = None
        self.direction = 0
        self.in_menu = True

        self.GAME_SIZE_X = 68
        self.GAME_SIZE_Y = 28
        self.SNAKE_UPDATE_FREQUENCY = 3

        self.w = None
        self.snake_update_counter = 0
        self.display_gameover = False

    def update_direction(self, new_key):
        print(f"Direction is {self.direction}")
        if new_key == "UP" and self.direction != 2:
            self.direction = 0
        elif new_key == "LEFT" and self.direction != 3:
            self.direction = 1
        elif new_key == "DOWN" and self.direction != 0:
            self.direction = 2
        elif new_key == "RIGHT" and self.direction != 1:
            self.direction = 3
        print(f"Now it is [{self.direction}")

    def display_snake(self):
        for x, y in self.snake:
            for a in range(4):
                for b in range(4):
                    self.w.addstr(y * 4 + a, x * 4 + b, "#", curses.color_pair(5))

    def update_snake(self):
        headx = self.snake[0][0]
        heady = self.snake[0][1]
        if self.direction == 0:
            heady -= 1
        elif self.direction == 1:
            headx += 1
        elif self.direction == 2:
            heady += 1
        else:
            headx -= 1

        self.snake.insert(0, (headx, heady))
        self.snake.pop(len(self.snake) - 1)

    def main(self, stdscr):
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
        game_window = curses.newwin(self.GAME_SIZE_Y, self.GAME_SIZE_X, 2, 3)

        self.w = game_window

        while True:
            #  get key input
            try:
                key = stdscr.getkey()
            except:
                key = None

            # do something with it
            if key == " ":
                if self.in_menu:
                    self.snake = self.default_snake.copy()
                    self.in_menu = False
                elif self.display_gameover:
                    self.in_menu = True
                    self.display_gameover = False

            elif key == '\x1b':  # if the user press escape, we leave the game
                curses.endwin()
                exit()
            # stuff to update the direction of the snake
            elif key == curses.KEY_UP:
                print("HELLOOOOOOOOO")
                self.update_direction("UP")
            elif key == curses.KEY_DOWN:
                self.update_direction("DOWN")
            elif key == curses.KEY_LEFT:
                self.update_direction("LEFT")
            elif key == curses.KEY_RIGHT:
                self.update_direction("RIGHT")

            #  cleaning old text and displaying new one
            stdscr.clear()

            if self.in_menu:
                # display the intro
                stdscr.addstr(1, 0, intro, curses.color_pair(2))
                stdscr.addstr(10, 0, play, curses.color_pair(3))
                stdscr.addstr(20, 0, exitmsg, curses.color_pair(3))
            else:
                if self.snake_update_counter != self.SNAKE_UPDATE_FREQUENCY:
                    self.snake_update_counter += 1
                else:
                    self.snake_update_counter = 0
                    self.update_snake()
                game_window.clear()
                if (self.snake[0][0] > self.GAME_SIZE_X / 4 or
                        self.snake[0][1] > self.GAME_SIZE_Y / 4 or
                        self.snake[0][0] < 0 or
                        self.snake[0][1] < 0):

                    game_window.addstr(int(self.GAME_SIZE_Y / 2 - 5), 5, gameover, curses.color_pair(1))
                    game_window.addstr(int(self.GAME_SIZE_Y / 2 + 2), 4, "hit space to continue", curses.color_pair(1))
                    self.display_gameover = True
                else:
                    self.display_snake()

                try:
                    rectangle(game_window, 0, 0, self.GAME_SIZE_Y - 1, self.GAME_SIZE_X - 1)
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


if __name__ == "__main__":
    g = Game()
    curses.wrapper(g.main)
