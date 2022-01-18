import numpy as np
import pandas as pd


class Env:
    def __init__(self, matrix):
        self.matrix = matrix
        self.visited = [0]
        self.current_city = 0
        self.done = False
        self.reward = 0
        self.distance = 0

    def reset(self):
        self.visited = [0]
        self.current_city = 0
        self.done = False
        self.reward = 0
        self.distance = 0

    def step(self,i):
        self.reward = 0
        if i == self.current_city:
            self.reward -= np.inf
        if i in self.visited:
            self.reward -= 0.1*self.matrix[self.current_city][i]
        else:
            self.reward -= self.matrix[self.current_city][i]*0.01
            self.visited.append(i)

        self.distance += self.matrix[self.current_city][i]
        self.done = len(self.matrix) == len(self.visited)
        self.current_city = i
        self.reward += 10 if self.done else 0
        return self.reward, self.done


class Agent:
    def __init__(self, matrix, gamma=1, epsilon=1, lr=0.2, epsilon_dec=0.999):
        self.matrix = matrix
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] /= 10**len(str(max(matrix[0])))
        self.env = Env(self.matrix)
        self.lr = lr
        self.current_city = 0
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec

        self.q_values = np.zeros((len(self.matrix), len(self.matrix)))


        self.reward = 0
        self.done = False
        self.action = 0

        self.road = []

    def chooseAction(self):
        if np.random.random() < self.epsilon:
            x = np.random.randint(0, len(self.matrix))
            return x

        else:
            return np.argmax(self.q_values[self.current_city])

    def learn(self):
        for episode in range(1000):
            self.env.reset()
            while not self.done:
                self.action = self.chooseAction()
                self.reward, self.done = self.env.step(self.action)
                old_q_value = self.q_values[self.current_city, self.action]
                temporal_difference = self.reward + (self.gamma * np.max(self.q_values[self.action]))
                new_q_value = (1 - self.lr) * old_q_value + (self.lr * temporal_difference)
                self.q_values[self.current_city, self.action] = new_q_value
                self.current_city = self.action
                self.epsilon = self.epsilon * self.epsilon_dec if self.epsilon > 0.01 else 0.01
            self.current_city = 0
            self.done = False

    def act(self):
        self.road = [0]
        self.env.reset()
        while not self.done:
            self.action = self.chooseAction()
            self.reward, self.done = self.env.step(self.action)
            self.current_city = self.action
            self.road.append(self.action)
        self.road.append(0)
        self.done = False

M = [[0,12502,558173, 333732,193824],
 [12502,0,548270,324290,207787],
 [558173, 547334,0, 258323, 754689],
 [333732, 322893, 258431,0, 530247],
 [193686, 207169, 755971, 531991,0]]
# to remove
print(max(M[0]))
#

agent = Agent(M)
agent.learn()
agent.act()
print(agent.road)

