#!/usr/bin/env python3
import curses
import os
import sys
from curses.textpad import rectangle
from json import loads
from random import randint
from time import sleep
from requests import get


import datetime
import pytz

from bigtext import *

# make sure we are running the script in the good directory
file_place = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_place)


def load_commit_info():
    try:
        with open("./commit_info", "r") as f:
            return loads(f.read())
    except FileNotFoundError:
        return {"commit": ".......", "gitdir": None, "message": None, "refs": None, "tree": None, "parent": None,
                "author": None, "author_date": None}


class Game:
    def __init__(self):
        self.default_snake = [(9, 3), (9, 4), (9, 5)]
        self.snake = None
        self.direction = 0  # 0 --> UP ; 1 --> LEFT ; 2 --> DOWN ; 3 --> RIGHT
        self.last_frame_direction = 2  # this help to prevent dying if direction is changed twice
        self.in_menu = True
        self.apples = []
        self.paused = False

        self.SQUARE_SIZE_X = 5
        self.SQUARE_SIZE_Y = 3
        self.GAME_SIZE_X = 70  # it will be  14 columns (5 * 14 = 70)
        self.GAME_SIZE_Y = 27  # it will be 9 rows (3 * 9 = 27)
        self.SNAKE_UPDATE_FREQUENCY = 3
        self.APPLE_SPAWNING_PROBABILITY = 30
        self.MAX_APPLE = 6
        self.DELAY_BETWEEN_FRAMES = 0.1
        self.MIN_COLS = 117
        self.MIN_LINES = 30
        self.commit_info = load_commit_info()
        self.VERSION_TEXT = f"{self.commit_info['commit'][0:7]} -- https://github.com/LeBeaufort/ssh-game  ({self.commit_info['author_date']})"
        self.TIME_FORMAT = "It is %H:%M:%S"

        try:
            self.CLIENT = sys.argv[1]
            self.CLIENT_PORT = sys.argv[2]
            self.HOST = sys.argv[3]
            self.HOST_PORT = sys.argv[4]
        except IndexError: self.CLIENT = None; self.CLIENT_PORT = 0;self.host=None;self.HOST_PORT=None

        self.time_zone = None
        self.is_client_tz = None

        self.w = None
        self.snake_update_counter = 0
        self.display_gameover = False
        self.score = 0
        self.has_display_statics = False
        self.in_game = False
        self.in_infos = False

    def find_timezone(self):
        response = get(f"http://ip-api.com/json/{self.CLIENT}?fields=status,timezone")
        json_response = response.json()
        if json_response['status'] != 'success':
            self.is_client_tz = False
            self.time_zone = pytz.timezone('utc')
        else:
            try:
                self.time_zone = pytz.timezone(json_response['timezone'])
                self.is_client_tz = True
            except pytz.exceptions.UnknownTimeZoneError:
                self.is_client_tz = False
                self.time_zone = pytz.timezone('utc')

    def get_time(self):
        return datetime.datetime.now(self.time_zone).strftime(self.TIME_FORMAT) + ("" if self.is_client_tz else " (UTC)")

    def update_direction(self, new_key):
        if new_key == "UP" and self.last_frame_direction != 2:
            self.direction = 0
        elif new_key == "LEFT" and self.last_frame_direction != 3:
            self.direction = 1
        elif new_key == "DOWN" and self.last_frame_direction != 0:
            self.direction = 2
        elif new_key == "RIGHT" and self.last_frame_direction != 1:
            self.direction = 3

    def display_game(self):
        # first snake
        for x, y in self.snake:
            for a in range(self.SQUARE_SIZE_Y):
                for b in range(self.SQUARE_SIZE_X):
                    try:
                        self.w.addstr(y * self.SQUARE_SIZE_Y + a, x * self.SQUARE_SIZE_X + b, "#", curses.color_pair(5))
                    except curses.error:
                        pass

        #  then apples
        for x, y in self.apples:
            for a in range(self.SQUARE_SIZE_Y):
                for b in range(self.SQUARE_SIZE_X):
                    try:
                        self.w.addstr(y * self.SQUARE_SIZE_Y + a, x * self.SQUARE_SIZE_X + b, "#", curses.color_pair(6))
                    except curses.error:
                        pass

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
        self.last_frame_direction = self.direction

        if (headx, heady) in self.apples:
            # if there is an apple at these coordinates, we remove it and increment the score
            self.apples.pop(self.apples.index((headx, heady)))
            self.score += 1
        else:
            # if there is not, we remove the last square of the snake, so it isn't getting bigger
            self.snake.pop(len(self.snake) - 1)

    def is_dead(self):
        return (self.snake[0][0] >= self.GAME_SIZE_X / self.SQUARE_SIZE_X or
                self.snake[0][1] >= self.GAME_SIZE_Y / self.SQUARE_SIZE_Y or
                self.snake[0][0] < 0 or
                self.snake[0][1] < 0 or
                self.snake[0] in self.snake[1:])  # check if the snake hit himself

    def spawn_apple(self):
        new = self.snake[0]  # we initialise to this position, so we are sure to place go at least one time in the loop
        # and do not get the same (0,0) each time
        while new in self.apples or new in self.snake:  # preventing to spawn on an apple or on the snake
            new = (
                randint(0, int(self.GAME_SIZE_X / self.SQUARE_SIZE_X) - 1),
                randint(0, int(self.GAME_SIZE_Y / self.SQUARE_SIZE_Y) - 1))
        self.apples.append(new)

    def game_window_drawing(self):
        """this draw the rectangle and refresh the window"""
        # displaying the rectangle, inside a try/except because :
        # https://stackoverflow.com/questions/52804155/extending-curses-rectangle-box-to-edge-of-terminal-in-python
        try:
            rectangle(self.w, 0, 0, self.GAME_SIZE_Y - 1, self.GAME_SIZE_X - 1)
        except curses.error:
            pass

        self.w.refresh()

    def check_terminal_size(self, stdscr):
        if curses.COLS < self.MIN_COLS or curses.LINES < self.MIN_LINES:
            stdscr.addstr(0, 0, 'YOUR TERMINAL SEEMS TOO LITTLE TO PLAY THIS GAME, YOU SHOULD GET A BIGGER ONE !',
                          curses.color_pair(4))
            stdscr.addstr(2, 0,
                          'THE GAME WILL PROBABLY NOT WORK AS EXPECTED', curses.color_pair(1))
            stdscr.addstr(4, 0, f'Your terminal size : {curses.COLS}x{curses.LINES}', curses.color_pair(4))
            stdscr.addstr(5, 0, f'Min requirements   : {self.MIN_COLS}x{self.MIN_LINES}', curses.color_pair(4))

            stdscr.addstr(7, 0, "Press SPACE to play anyway, press any other key to leave", curses.color_pair(1))
            while True:
                #  get key input
                try:
                    if stdscr.getkey() == " ":
                        return
                    else:
                        exit()
                except curses.error:
                    sleep(self.DELAY_BETWEEN_FRAMES)

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

        self.check_terminal_size(stdscr)
        self.find_timezone()

        #  so we are sure to do not display anything outside an area
        game_window = curses.newwin(self.GAME_SIZE_Y, self.GAME_SIZE_X, 2, 3)

        self.w = game_window

        while True:
            #  get key input
            try:
                key = stdscr.getkey()
            except curses.error:
                key = None

            # do something with it
            if key == " ":
                if self.in_menu:
                    #  resetting to default
                    self.snake = self.default_snake.copy()
                    self.direction = 0
                    self.score = 0
                    self.in_menu = False
                    self.apples = []
                    self.has_display_statics = False
                    self.paused = False
                    self.in_game = True
                    #  cleaning old text to be able to display the game
                    stdscr.clear()
                elif self.display_gameover:
                    self.in_menu = True
                    self.display_gameover = False
                    self.has_display_statics = False

            elif key == '\x1b':  # if the user press escape, we leave the game
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
            elif key == "d":
                self.in_menu = True
                self.in_game = False
                self.has_display_statics = False
            elif key == "p":
                self.paused = not self.paused
                if not self.paused:
                    self.has_display_statics = False
            elif key == "i":
                if not self.in_game and not self.in_infos:
                    self.in_infos = True
                    self.in_menu = False
                    self.in_game = False
                    self.has_display_statics = False

            if self.in_menu:
                if not self.has_display_statics:
                    stdscr.clear()  # cleaning old text
                    # display the intro
                    stdscr.addstr(1, 0, intro, curses.color_pair(2))
                    stdscr.addstr(9, 0, play, curses.color_pair(3))
                    stdscr.addstr(15, 0, exitmsg, curses.color_pair(3))
                    stdscr.addstr(21, 0, infos_main_menu, curses.color_pair(3))
                    self.has_display_statics = True

            elif self.display_gameover:
                if not self.has_display_statics:
                    game_window.clear()
                    display_gameover(game_window, int(self.GAME_SIZE_Y / 2 - 5), 10, color_pair_number=1)
                    game_window.addstr(int(self.GAME_SIZE_Y / 2 + 2), 22, "hit space to continue", curses.color_pair(1))
                    self.game_window_drawing()
                    self.has_display_statics = True

            elif self.in_game:
                # should we update the snake now ?
                if not self.paused and self.snake_update_counter != self.SNAKE_UPDATE_FREQUENCY:
                    self.snake_update_counter += 1
                elif self.snake_update_counter == self.SNAKE_UPDATE_FREQUENCY and not self.paused:
                    self.snake_update_counter = 0
                    self.update_snake()
                    #  check if we should spawn the apple
                    if len(self.apples) < self.MAX_APPLE and randint(0, self.APPLE_SPAWNING_PROBABILITY) == 0:
                        self.spawn_apple()

                    game_window.clear()

                    stdscr.addstr(2, self.GAME_SIZE_X + 4, f"Score : {self.score}", curses.color_pair(3))
                    display_controls(stdscr, 4, self.GAME_SIZE_X, 2)

                    # check if the snake is alive. If yes displaying, else display game over
                    if self.is_dead():
                        self.display_gameover = True
                    else:
                        self.display_game()

                    self.game_window_drawing()

                elif self.paused:
                    if not self.has_display_statics:
                        self.has_display_statics = True
                        display_pause(game_window, 5, 15, 3)
                        game_window.refresh()

            elif self.in_infos:
                if not self.has_display_statics:
                    #  cleaning old text
                    stdscr.clear()
                    stdscr.refresh()
                    game_window.clear()

                    #  displaying infos
                    display_info_title(game_window, 5, 15, 4)
                    game_window.addstr(12, 5, f"Commit id {self.commit_info['commit'][:7]}")
                    game_window.addstr(14, 5, f"Full commit id {self.commit_info['commit']}")
                    game_window.addstr(16, 5, f"Pushed on {self.commit_info['author_date']}")
                    game_window.addstr(18, 5, f"Commit message : \'{self.commit_info['message']}\'")

                    self.game_window_drawing()
                    self.has_display_statics = True

            # displaying the where source code is
            stdscr.addstr(0, 0, self.get_time(), curses.color_pair(4))
            stdscr.addstr(curses.LINES - 1, 0, self.VERSION_TEXT, curses.color_pair(2))
            sleep(self.DELAY_BETWEEN_FRAMES)


if __name__ == "__main__":
    g = Game()
    try:
        curses.wrapper(g.main)
    except KeyboardInterrupt:
        exit()
