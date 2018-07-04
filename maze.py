# fernival made
# set certain macros
KEY_EXIT = 27  # define macros
KEY_SPACE = 32
KEY_UP = 119  # WASD
KEY_DOWN = 115
KEY_LEFT = 97
KEY_RIGHT = 100
KEY_LOST = KEY_DOWN
NO_ENTRY = float('-inf')
ABSORB = 1.0
MIN_TOLERANCE = 0.0000000001 # 10^-11

class node():
    def __init__(self, y, x, value=0.0):
        self.pi = {KEY_UP: 0.25, KEY_DOWN: 0.25, KEY_LEFT: 0.25, KEY_RIGHT: 0.25}
        self.value = value
        self.neighborV = {KEY_UP: 0.0, KEY_DOWN: 0.0, KEY_LEFT: 0.0, KEY_RIGHT: 0.0}
        self.y = y
        self.x = x


class maze():
    def __init__(self, height, width, value=0.0):
        self.axis = (height, width)
        self.map = [[node(y, x, value=value) for y in range(width)] for x in range(height)]
        # (height, width) so map[height][width]

    def setAbsorb(self, cord):
        self.map[cord[0]-1][cord[1]-1].value = ABSORB

    def __refreshNeighborValue(self):
        for j in range(self.axis[1]):
            for i in range(self.axis[0]):

                if j == 0:
                    self.map[i][j].neighborV[KEY_LEFT] = self.map[i][self.axis[1] - 1].value
                else:
                    self.map[i][j].neighborV[KEY_LEFT] = self.map[i][j - 1].value
                if j == self.axis[1] - 1:
                    self.map[i][j].neighborV[KEY_RIGHT] = self.map[i][0].value
                else:
                    self.map[i][j].neighborV[KEY_RIGHT] = self.map[i][j + 1].value

                if i == 0:
                    self.map[i][j].neighborV[KEY_UP] = self.map[self.axis[0] - 1][j].value
                else:
                    self.map[i][j].neighborV[KEY_UP] = self.map[i - 1][j].value
                if i == self.axis[0] - 1:
                    self.map[i][j].neighborV[KEY_DOWN] = self.map[0][j].value
                else:
                    self.map[i][j].neighborV[KEY_DOWN] = self.map[i + 1][j].value

    def refreshValue(self, gamma=1, instantValue=-1):
        self.__refreshNeighborValue()
        bConverge = True
        # for j in range(self.axis[1]):
        #     for i in range(self.axis[0]):
        #         nd = self.map[i][j]
        #         nd.value = nd.pi[KEY_UP] * (nd.value + nd.neighborV[KEY_UP]) + \
        #                    nd.pi[KEY_DOWN] * (nd.value + nd.neighborV[KEY_DOWN]) + \
        #                    nd.pi[KEY_LEFT] * (nd.value + nd.neighborV[KEY_LEFT]) + \
        #                    nd.pi[KEY_RIGHT] * (nd.value + nd.neighborV[KEY_RIGHT])
        for col in self.map:
            for nd in col:
                if nd.value == ABSORB or nd.value == NO_ENTRY:
                    continue
                oldValue = nd.value
                nd.value = 0
                for k in nd.pi.keys():
                    if nd.pi[k] == 0:   # exclude cal with -inf
                        continue
                    nd.value += nd.pi[k] * (instantValue + gamma * nd.neighborV[k])
                if bConverge == True:  # check if  converged
                    if abs(oldValue - nd.value) >= MIN_TOLERANCE:
                        bConverge = False
        return bConverge

    def refreshPi(self):
        self.__refreshNeighborValue()
        for col in self.map:
            for nd in col:
                moves = 0
                for k in nd.pi.keys():
                    if nd.pi[k] != 0 and nd.neighborV[k] != NO_ENTRY and nd.neighborV[k] >= nd.value:
                        moves += 1
                    else:
                        nd.pi[k] = 0

                if moves != 0:
                    p = 1 / moves
                else:
                    p = 0

                for k in nd.pi.keys():
                    if nd.pi[k] != 0:
                        nd.pi[k] = p

                    # # no choice set the biggest, if surrounded, go up and die
                    # max = float('-inf')
                    # key = KEY_UP
                    # for k in nd.pi.keys():
                    #     if nd.neighborV[k] > max:
                    #         max = nd.neighborV[k]
                    #         key = k
                    # for k in nd.pi.keys():
                    #     nd.pi[k] = 0
                    # nd.pi[key] = 1

    def refreshDead(self, cords):
        for c in cords:
            self.map[c[0]-1][c[1]-1].value = NO_ENTRY

    def getMove(self, cord):
        nd = self.map[cord[0]-1][cord[1]-1]
        max = nd.neighborV[KEY_DOWN]
        key = KEY_DOWN
        for k in nd.neighborV.keys():
            if nd.pi[k] != 0 and max < nd.neighborV[k]:
                max = nd.neighborV[k]
                key = k
        return key

    def show(self):
        for i in range(self.axis[0]):
            l = []
            for j in range(self.axis[1]):
                l.append(self.map[i][j].value)
            print(l)