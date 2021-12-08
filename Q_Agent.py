import math

import Helpers
from Helpers import *

class QLearningAgent:
    def __init__(self, alpha=0.2, epsilon=0.7, gamma=0.8, numTraining=500):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.numTraining = numTraining

        self.episodes_counter = 0

        self.q_value = Counter()

        self.score = 0

        self.lastState = []

        self.lastAction = []

    def increment_episodes_so_far(self):
        self.episodes_counter += 1

    def get_episodes_so_far(self):
        return self.episodes_counter

    def get_num_training(self):
        return self.numTraining


    def set_epsilon(self, value):
        self.epsilon = value

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, value):
        self.alpha = value

    def get_gamma(self):
        return self.gamma

    def get_q_value(self, state, action):

        return self.q_value[(state, (action[0], action[1]))]

    def get_max_q(self, state):
        q_list = []
        for action in state.get_legal_actions(mob_type=PLAYER):
            q = self.get_q_value(state, action)
            q_list.append(q)
        if len(q_list) == 0:
            return 0

        return max(q_list)

    def update_q(self, state, action, reward, q_max):
        q = self.get_q_value(state, action)
        self.q_value[(state, (action[0], action[1]))] = q + self.alpha * (reward + self.gamma*q_max)

    def do_the_right_thing(self, state):

        allowed_directions = state.get_legal_actions(mob_type=PLAYER)

        if self.get_episodes_so_far() * 1.0 / self.get_num_training() < 0.5:
            if Directions.STOP in allowed_directions:
                allowed_directions.remove(Directions.STOP)

            if len(self.lastAction) > 0:
                last_action = self.lastAction[-1]
                if state.get_ghost_positions():
                    distance0 = state.get_pacman_position()[0] - state.get_ghost_positions()[0][0]
                    distance1 = state.get_pacman_position()[1] - state.get_ghost_positions()[0][1]
                    if math.sqrt(distance0 ** 2 + distance1 ** 2) > 2:
                        if(Directions.REVERSED[(last_action[0], last_action[1])] in allowed_directions) and len(allowed_directions) > 1:
                            allowed_directions.remove(vec(Directions.REVERSED[(last_action[0], last_action[1])]))
        temp = Counter()

        for action in allowed_directions:
            temp[(action[0], action[1])] = self.get_q_value(state, (action[0], action[1]))
        print(self.score, temp.argMax())
        return temp.argMax()

    def get_action(self, state):
        allowed_directions = state.get_legal_actions(mob_type=PLAYER)
        if Directions.STOP in allowed_directions:
            allowed_directions.remove(Directions.STOP)

        reward = state.get_score() - self.score

        if len(self.lastState) > 0:
            last_state = self.lastState[-1]
            last_action = self.lastAction[-1]
            max_q = self.get_max_q(state)
            self.update_q(last_state, last_action, reward, max_q)

        if Helpers.flipCoin(self.epsilon):
            action = random.choice(allowed_directions)
        else:
            action = self.do_the_right_thing(state)

        self.score = state.get_score()
        self.lastState.append(state)
        self.lastAction.append(action)

        return action


    def final(self, state):
        print(self.episodes_counter, self.score)
        reward = state.get_score() - self.score
        last_state = self.lastState[-1]
        last_action = self.lastAction[-1]

        self.update_q(last_state, last_action, reward, 0)

        self.score = 0
        self.lastState = []
        self.lastAction = []

        epsilon = 1 - self.get_episodes_so_far() * 1.0 / self.get_num_training()

        self.set_epsilon(epsilon * 0.1)

        self.increment_episodes_so_far()

        if self.get_episodes_so_far() % 10 == 0:
            print(f"Completed {self.get_episodes_so_far()}")

        if self.get_episodes_so_far() == self.get_num_training():
            pass
