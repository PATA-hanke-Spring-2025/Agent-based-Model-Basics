import pandas as pd
import random
from reading import create_state_matrix, read_value_elements
from value_calculator import ValuePropositionCalculator

class Agent:
#for SellerAgent
    def __init__(self, transition_data, states, value_elements_df, category_weights_df):
        self.states = states
        self.state = states['State'].iloc[0]
        self.transition_matrix = create_state_matrix(transition_data, states)
         # Initialize value calculator
        self.value_calculator = ValuePropositionCalculator(value_elements_df, category_weights_df)

    

    def step(self):
        probabilities = self.transition_matrix.loc[self.state].values
        self.state = random.choices(self.states['State'].tolist(), weights=probabilities)[0]
        return self.state