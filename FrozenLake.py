import numpy as np

# global variables
BOARD_ROWS = 5
BOARD_COLS = 5
WIN_STATE = (4, 4)
LOSE_STATE = {(1, 0), (1, 3), (3, 1), (4, 2)}
START = (0, 0)


class State:
    def __init__(self, state=START):
        self.state = state
        self.isEnd = False

    # returning rewards at each instance of the agent
    def getReward(self):
        if self.state == WIN_STATE:
            return 1
        elif self.state in LOSE_STATE:
            return -5
        else:
            return -1

    # checking if agent have reached an end
    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state in LOSE_STATE):
            self.isEnd = True

    # identifying next possible state for an agent upon particular action
    def nxtPosition(self, action):
        if action == "up":
            nxtState = (self.state[0] - 1, self.state[1])
        elif action == "down":
            nxtState = (self.state[0] + 1, self.state[1])
        elif action == "left":
            nxtState = (self.state[0], self.state[1] - 1)
        else:
            nxtState = (self.state[0], self.state[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= 4):
            if (nxtState[1] >= 0) and (nxtState[1] <= 4):
                return nxtState  # if next state legal

        return self.state  # Any move off the grid leaves state unchanged


# Agent

class Agent:

    def __init__(self):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.discount = 0.9

        # initialise state values
        self.state_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.state_values[(i, j)] = 0  # set initial value to 0

        self.new_state_values = {}

    def frozen_lake(self, episodes):
        x = 0
        # Loop through all the states rows * cols
        while x < episodes:
            i = 0
            j = 0
            while i < BOARD_ROWS:
                while j < BOARD_COLS:
                    nxt_value = [0, 0, 0, 0]
                    self.State = State(state=(i, j))
                    self.State.isEndFunc()
                    if not self.State.isEnd:
                        for a in self.actions:
                            nxt_value[self.actions.index(a)] = self.State.getReward() + (
                                        self.discount * self.state_values[self.State.nxtPosition(a)])
                        mn_nxt_value = max(nxt_value)
                    else:
                        mn_nxt_value = self.State.getReward()
                        # Update the state values
                    self.new_state_values[(i, j)] = round(mn_nxt_value, 3)
                    j += 1
                i += 1
                j = 0
            x += 1
            self.state_values = self.new_state_values.copy()

    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')


if __name__ == "__main__":
    ag = Agent()
    ag.frozen_lake(10000)
    print(ag.showValues())
