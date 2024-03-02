# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:46:48 2024

@author: Amitr
"""

import numpy as np
import json
import ast
from collections import defaultdict
import random
import os

class DinoStateSpace:
    """
    Class representing the state space for the Dino in the Q-learning algorithm.

    Attributes:
    - dino: Dino object representing the main character.
    - obstacles: List of Cactus objects representing obstacles.
    """

    def __init__(self, dino, obstacles):
        """Initialize DinoStateSpace object."""
        self.dino = dino
        self.obstacles = obstacles

    @property
    def state(self):
        """Get the current state of the Dino."""
        # Define the state based on the relevant features of the Dino and obstacles
        dino_state = (self.dino.x, self.dino.y, int(self.dino.jumping), int(self.dino.falling))
        obstacles_state = [(obs.x, obs.y) for obs in self.obstacles]
        return dino_state, tuple(obstacles_state)

    def update_state(self):
        """Update the state based on the new position of the Dino and obstacles."""
        self.state

    def get_state(self):
        """Get the current state of the Dino."""
        # Extract relevant features for the state representation
        dino_y = self.dino.y
        obstacle_distances = [obstacle.x - self.dino.x for obstacle in self.obstacles]
        nearest_obstacle_distance = min(obstacle_distances, default=1000)  # Default value for no obstacles

        # Boolean flags for jumping and falling
        is_jumping = self.dino.jumping
        is_falling = self.dino.falling

        # Return a tuple containing the relevant features
        return dino_y, nearest_obstacle_distance, is_jumping, is_falling

class QLearningAgent:
    def __init__(self, state_space, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.state_space = state_space
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        if state in self.q_table:
            return max(self.q_table[state], key=self.q_table[state].get)
        else:
            return random.choice(self.actions)

    def update_q_value(self, state, action, reward, next_state):
        self.initialize_state_action_pair(state, action)
        current_q_value = self.q_table[state][action]

        if next_state not in self.q_table:
            self.initialize_state_actions(next_state)

        max_next_q_value = max(self.q_table[next_state].values(), default=0)
        new_q_value = (1 - self.learning_rate) * current_q_value + \
                      self.learning_rate * (reward + self.discount_factor * max_next_q_value)

        self.q_table[state][action] = new_q_value

    def initialize_state_action_pair(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

    def initialize_state_actions(self, state):
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}

    def decay_exploration_rate(self):
        self.exploration_rate *= 0.995
        self.exploration_rate = max(0.1, self.exploration_rate)

    def load_q_values(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                # Load Q-values and convert string keys back to tuples
                q_table_str_keys = json.load(file)
                self.q_table = {tuple(eval(k)): v for k, v in q_table_str_keys.items()}

    def save_q_values(self, file_path):
        with open(file_path, 'w') as file:
            # Convert tuple keys to string keys
            q_table_str_keys = {str(k): v for k, v in self.q_table.items()}
            json.dump(q_table_str_keys, file)

    def print_q_values(self):
        for state, actions in self.q_table.items():
            print(f"State: {state}, Q-Values: {actions}")