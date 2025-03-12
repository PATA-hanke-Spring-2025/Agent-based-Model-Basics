import pandas as pd
import random

class Buyer:
    """
    Attributes:
        "Not Interested", "Evaluating", "Budgeting", "Deciding", "Go Nogo", "Delivered", "Satisfied"
    """
    def __init__(self, transition_data, states):
        self.state = "Not Interested"
        self.transition_data = transition_data
        self.states = states
        self.transition_matrix = self.create_initial_matrix()

    def create_initial_matrix(self):
        matrix = []
        for from_state in self.states['State']:
            row = []
            for to_state in self.states['State']:
                value = self.transition_data.loc[self.transition_data['From/To'] == from_state, to_state].values[0]
                value = float(value.replace(',', '.'))
                row.append(value)
            matrix.append(row)
        return pd.DataFrame(matrix, index=self.states['State'], columns=self.states['State'])

    def step(self):
        probabilities = self.transition_matrix.loc[self.state].values
        self.state = random.choices(self.states['State'].tolist(), weights=probabilities)[0]
        return self.state
    
random.seed(42)