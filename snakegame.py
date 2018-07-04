# SNAKES GAME IMPLEMENTATION FOR AI
# NOT FOR HUMAN !
# fernival made

import curses
from random import randint

KEY_EXIT = 27  # define macros
KEY_SPACE = 32
KEY_UP = 119  # WASD
KEY_DOWN = 115
KEY_LEFT = 97
KEY_RIGHT = 100


class SnakeGame():
    def __init__(self, height=16, width=32, snake=((1, 1)), food=(2, 2)):
        curses.initscr()
        self.height = height +2
        self.width = width +2
        self.status = True
        self.win = curses.newwin(self.height, self.width, 0, 0)   # mind that border axis is (-1)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.score = 0
        self.snake = snake  # Initial snake co-ordinates, (y, x)!
        self.food = food  # First food co-ordinates
        self.show([self.food])  # Prints the food & the snake
        self.show(self.snake, '#')
        self.win.refresh()

    def show(self, itemlist, symbol='*'):
        for i in itemlist:
            self.win.addch(i[0], i[1], symbol)

    def endgame(self):
        curses.endwin()
        self.status = False
        print("\nScore - " + str(self.score))
        print("Happy hunting!\n")
        return self.score

    def getfood(self):
        return self.food

    def getsnake(self):
        return self.snake

    def keyinput(self, key):
        if not self.status:
            return self.status

        self.win.border(0)
        self.win.addstr(0, 1, 'Score:' + str(self.score) + ' ')  # Printing 'Score'
        #self.win.addstr(0, 25, ' SNAKE ')  # 'SNAKE' strings
        #self.win.addstr(0, self.width // 2, ' x-{0} y-{1} '.format(self.snake[0][1], self.snake[0][0]))
        self.win.refresh()

        self.snake.insert(0, [self.snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                              self.snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        # If snake crosses the boundaries, make it enter from the other side
        if self.snake[0][0] == 0: self.snake[0][0] = self.height -2
        if self.snake[0][1] == 0: self.snake[0][1] = self.width -2
        if self.snake[0][0] == self.height -1: self.snake[0][0] = 1
        if self.snake[0][1] == self.width -1: self.snake[0][1] = 1
        if self.snake[0] in self.snake[1:]:
            self.endgame()
            return False

        # Exit if snake crosses the boundaries
        # if self.snake[0][0] == 0 or self.snake[0][0] == self.height -1 or \
        #         self.snake[0][1] == 0 or self.snake[0][1] == self.width -1:
        #     self.endgame()
        #     return False
        # elif self.snake[0] in self.snake[1:]:
        #     self.endgame()
        #     return False

        if self.snake[0] == self.food:
            self.food = []
            self.score += 1
            while self.food == []:
                self.food = [randint(1, self.height -2), randint(1, self.width -2)]  # Calculating next food's coordinates
                if self.food in self.snake:
                    self.food = []
            self.show([self.food])
        else:
            tail = self.snake.pop()
            self.show([tail], ' ')
        self.show(self.snake, '#')
        return self.food
