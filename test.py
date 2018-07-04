# fernival made
from snakegame import SnakeGame
from maze import maze
import curses

KEY_EXIT = 27  # define macros
KEY_SPACE = 32
KEY_UP = 119  # WASD
KEY_DOWN = 115
KEY_LEFT = 97
KEY_RIGHT = 100
KEY_LOST = KEY_DOWN
NO_ENTRY = float('-inf')
ABSORB = 1.0

MAX_ITER = 100000
HEIGHT = 8
WIDTH = 8

def getkey(snake, food, shape=(16, 16)):
    m = maze(shape[0], shape[1], value=-1)
    m.setAbsorb(food)
    m.refreshDead(snake)
    m.refreshPi()  # exclude -inf
    bConverge = False
    count = 0
    while not bConverge:
        bConverge = m.refreshValue()
        m.refreshPi()
        count += 1
        if count >= MAX_ITER:
            break
    return m.getMove(snake[0]), count


sg = SnakeGame(height=HEIGHT, width=WIDTH, snake=[[2, 3], [2, 2]], food=[3, 3])
food = sg.getfood()

totalc = 0
maxc = 0
steps = 0
while food:
    snake = sg.getsnake()

    key, count = getkey(snake, food, shape=[HEIGHT, WIDTH])
    print(len(snake), count)
    if maxc < count:
        maxc = count
    if count < MAX_ITER:
        totalc += count
        steps += 1

    food = sg.keyinput(key)
    curses.napms(200)

print(maxc, totalc / steps)