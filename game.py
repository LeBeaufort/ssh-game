import curses
from bigtext import *
from time import sleep
from curses.textpad import rectangle
from random import randint


class Game:
    def __init__(self):
        self.default_snake = [(9, 3), (9, 4), (9, 5)]
        self.snake = None
        self.direction = 0  # 0 --> UP ; 1 --> LEFT ; 2 --> DOWN ; 3 --> RIGHT
        self.in_menu = True
        self.apples = []

        self.SQUARE_SIZE_X = 5
        self.SQUARE_SIZE_Y = 3
        self.GAME_SIZE_X = 70  # it will be  14 columns (5 * 14 = 70)
        self.GAME_SIZE_Y = 27  # it will be 9 rows (3 * 9 = 27)
        self.SNAKE_UPDATE_FREQUENCY = 3
        self.APPLE_SPAWNING_PROBAPILITY = 30
        self.MAX_APPLE = 6

        self.w = None
        self.snake_update_counter = 0
        self.display_gameover = False
        self.score = 0

    def update_direction(self, new_key):
        if new_key == "UP" and self.direction != 2:
            self.direction = 0
        elif new_key == "LEFT" and self.direction != 3:
            self.direction = 1
        elif new_key == "DOWN" and self.direction != 0:
            self.direction = 2
        elif new_key == "RIGHT" and self.direction != 1:
            self.direction = 3

    def display_game(self):
        # first snake
        for x, y in self.snake:
            for a in range(self.SQUARE_SIZE_Y):
                for b in range(self.SQUARE_SIZE_X):
                    self.w.addstr(y * self.SQUARE_SIZE_Y + a, x * self.SQUARE_SIZE_X + b, "#", curses.color_pair(5))

        #  then apples
        for x, y in self.apples:
            for a in range(self.SQUARE_SIZE_Y):
                for b in range(self.SQUARE_SIZE_X):
                    self.w.addstr(y * self.SQUARE_SIZE_Y + a, x * self.SQUARE_SIZE_X + b, "#", curses.color_pair(6))

    def update_snake(self):
        headx = self.snake[0][0]
        heady = self.snake[0][1]
        if self.direction == 0:
            heady -= 1
        elif self.direction == 1:
            headx -= 1
        elif self.direction == 2:
            heady += 1
        else:
            headx += 1

        self.snake.insert(0, (headx, heady))
        self.snake.pop(len(self.snake) - 1)

    def is_dead(self):
        return (self.snake[0][0] >= self.GAME_SIZE_X / self.SQUARE_SIZE_X or
                self.snake[0][1] >= self.GAME_SIZE_Y / self.SQUARE_SIZE_Y or
                self.snake[0][0] < 0 or
                self.snake[0][1] < 0)

    def spawn_apple(self):
        new = self.snake[0]  # we initialise to this position, so we are sure to place go at least one time in the loop
        # and do not get the same (0,0) each time
        while new in self.apples or new in self.snake:  # preventing to spawn on an apple or on the snake
            new = (
                randint(0, int(self.GAME_SIZE_X / self.SQUARE_SIZE_X) - 1),
                randint(0, int(self.GAME_SIZE_Y / self.SQUARE_SIZE_Y) - 1))
        self.apples.append(new)

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
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_RED)

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
                print(f"Key is {key}, type is {type(key)}")
            except:
                key = None

            # do something with it
            if key == " ":
                if self.in_menu:
                    #  reseting to default
                    self.snake = self.default_snake.copy()
                    self.direction = 0
                    self.score = 0
                    self.in_menu = False
                    self.apples = []
                elif self.display_gameover:
                    self.in_menu = True
                    self.display_gameover = False

            elif key == '\x1b':  # if the user press escape, we leave the game
                curses.endwin()
                exit()
            # stuff to update the direction of the snake
            elif key == "KEY_UP":
                self.update_direction("UP")
            elif key == "KEY_DOWN":
                self.update_direction("DOWN")
            elif key == "KEY_LEFT":
                self.update_direction("LEFT")
            elif key == "KEY_RIGHT":
                self.update_direction("RIGHT")

            #  cleaning old text and displaying new one
            stdscr.clear()

            if self.in_menu:
                # display the intro
                stdscr.addstr(1, 0, intro, curses.color_pair(2))
                stdscr.addstr(10, 0, play, curses.color_pair(3))
                stdscr.addstr(20, 0, exitmsg, curses.color_pair(3))
            else:

                # should we update the snake now ?
                if self.snake_update_counter != self.SNAKE_UPDATE_FREQUENCY:
                    self.snake_update_counter += 1
                    #  check if we should spawn the apple
                    if len(self.apples) < self.MAX_APPLE and randint(0, self.APPLE_SPAWNING_PROBAPILITY) == 0:
                        self.spawn_apple()
                        print('Spawning apple')
                else:
                    self.snake_update_counter = 0
                    self.update_snake()

                game_window.clear()
                stdscr.addstr(2, self.GAME_SIZE_X + 4, f"Score : {self.score}", curses.color_pair(3))
                #  stdscr.addstr(4, self.GAME_SIZE_X + 4, controls, curses.color_pair(2))
                display_controls(stdscr, 4, self.GAME_SIZE_X, 2)

                # check if the snake is alive. If yes displaying, else display game over
                if self.is_dead():
                    display_gameover(game_window, int(self.GAME_SIZE_Y / 2 - 5), 10, color_pair_number=1)
                    game_window.addstr(int(self.GAME_SIZE_Y / 2 + 2), 22, "hit space to continue", curses.color_pair(1))
                    self.display_gameover = True
                else:
                    self.display_game()

                # displaying the rectangle, inside a try/except because :
                # https://stackoverflow.com/questions/52804155/extending-curses-rectangle-box-to-edge-of-terminal-in-python
                try:
                    rectangle(game_window, 0, 0, self.GAME_SIZE_Y - 1, self.GAME_SIZE_X - 1)
                except:
                    pass

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
