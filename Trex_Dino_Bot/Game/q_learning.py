# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:46:48 2024

@author: Amitr
"""

import numpy as np
import json

class DinoStateSpace:
    def __init__(self, dino, obstacles):
        self.dino = dino
        self.obstacles = obstacles

    def get_state(self):
        # Define the state based on the relevant features of the Dino and obstacles
        dino_state = (self.dino.x, self.dino.y, int(self.dino.jumping), int(self.dino.falling))
        obstacles_state = [(obs.x, obs.y) for obs in self.obstacles]
        return dino_state, tuple(obstacles_state)

class QLearningAgent:
    def __init__(self, state_space, actions, learning_rate=0.5, discount_factor=0.9, exploration_rate=0.1):
        self.state_space = state_space
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_action(self, state):
        if np.random.rand() < self.exploration_rate:
            # Explore - choose a random action
            return np.random.choice(self.actions)
        else:
            # Exploit - choose the action with the highest Q-value
            return max(self.actions, key=lambda a: self.q_table.get((state, a), 0))

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        max_future_q = max([self.q_table.get((next_state, a), 0) for a in self.actions])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[(state, action)] = new_q
        
    def save_q_values(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.q_values, file)

    @staticmethod
    def load_q_values(filename):
        q_learning_agent = QLearningAgent(state_space=None, actions=None)  # Replace None with appropriate values
        with open(filename, 'r') as file:
            q_learning_agent.q_values = json.load(file)
        return q_learning_agent
