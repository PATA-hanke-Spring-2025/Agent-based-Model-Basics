import random
import pandas as pd

class Buyer:
    def __init__(self, state_transitions):
        super().__init__()
        self.state = "NOT_INTERESTED"
        self.state_transitions = state_transitions
        random.seed(42)

    def step(self):
        transitions = self.state_transitions[self.state_transitions['current_state'] == self.state]

        if transitions.empty:
            return

        chance = random.random()
        cumulative_probability = 0.0

        for _, row in transitions.iterrows():
            cumulative_probability += row['probability']
            if chance < cumulative_probability:
                self.state = row['next_state']
                break