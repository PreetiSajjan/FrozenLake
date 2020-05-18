import random

import numpy as np
import matplotlib.pyplot as plt

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
        if action == 0:
            nxtState = (self.state[0] - 1, self.state[1])
        elif action == 1:
            nxtState = (self.state[0] + 1, self.state[1])
        elif action == 2:
            nxtState = (self.state[0], self.state[1] - 1)
        else:
            nxtState = (self.state[0], self.state[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= 4):
            if (nxtState[1] >= 0) and (nxtState[1] <= 4):
                return nxtState  # if next state legal

        return self.state  # Any move off the grid leaves state unchanged

    # returnng the state instance
    def getIndex(self):
        return self.state


# Agent

class Agent:

    def __init__(self):
        self.states = []
        self.actions = [0, 1, 2, 3]  # ["up", "down", "left", "right"]
        self.State = State()
        self.discount = 0.9
        self.rewards = []

        # initialise Q table
        self.Q = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q[(i, j)] = [0, 0, 0, 0]

        self.new_state_values = {}

    def frozen_lake(self, episodes=10000):
        # Loop through all the states rows * cols
        alpha = 0.5
        gamma = 0.9
        eps = 0.10
        steps = 99
        for x in range(episodes):
            total_reward = 0
            for i in range(BOARD_ROWS):
                for j in range(BOARD_COLS):
                    self.State = State(state=(i, j))
                    self.State.isEndFunc()
                    if not self.State.isEnd:
                        for step in range(steps):

                            # implementing e-greedy method
                            tradeoff = random.uniform(0, 1)
                            if tradeoff < eps:
                                a = random.randint(0, 3)
                            else:
                                a = self.Q[self.State.getIndex()].index(max(self.Q[self.State.getIndex()]))

                            self.Q[self.State.getIndex()][a] = (1 - alpha) * self.Q[self.State.getIndex()][a] + (
                                        alpha * (
                                        self.State.getReward() + (
                                        gamma * (max(self.Q[self.State.nxtPosition(a)])))
                                ))
                            # assigning the next state to agent
                            self.State = State(state=self.State.nxtPosition(a))
                            # checking if next state is terminal state
                            self.State.isEndFunc()
                            if self.State.isEnd:
                                self.Q[self.State.getIndex()][a] = self.State.getReward()
                                break
                    else:
                        self.Q[self.State.getIndex()][a] = self.State.getReward()

                    total_reward += self.State.getReward()
            # append the reward
            self.rewards.append(total_reward)

        for j, v in self.Q.items():
            self.Q[j] = np.round(v, 3)

    def showValues(self):
        print("Score over time: " + str(sum(self.rewards) / 10000))

        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(max(self.Q[(i, j)])).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

        # plotting the curve of the reward per episode
        episode = range(10000)
        plt.plot(episode, self.rewards)
        plt.xlabel('Episodes')
        plt.ylabel('Reward per Episode')
        plt.title('Cumulative Reward over Episodes')
        plt.show()


if __name__ == "__main__":
    ag = Agent()
    ag.frozen_lake()
    print(ag.showValues())
