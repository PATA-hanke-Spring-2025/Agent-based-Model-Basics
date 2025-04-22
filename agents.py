import pandas as pd
import random
from reading import create_state_matrix, read_value_elements

class Agent:

    def __init__(self, transition_data, states, value_elements, category_weights):
        self.states = states
        self.state = states['State'].iloc[0]
        self.transition_matrix = create_state_matrix(transition_data, states)
        self.value_elements = value_elements
        self.category_weights = category_weights
        self.current_values = self.initialize_values()

    def initialize_values(self):
        """Initialize values based on the current weights."""
        values = {}
        for element, details in self.value_elements.items():
            # Use the weight as the initial value
            values[element] = details['weight']
        return values

    def update_values(self):
        """Update values by slightly modifying the weights."""
        for element, details in self.value_elements.items():
            original_weight = details['weight']
            # Randomly adjust the weight slightly (e.g., ±10%)
            adjustment = random.uniform(-0.1, 0.1) * original_weight
            new_weight = details['weight'] + adjustment
            # Ensure the weight stays close to the original and within [0, 1]
            details['weight'] = max(0, min(1.0, new_weight))
            # Apply a "pull" toward the original weight to stabilize
            details['weight'] += 0.1 * (original_weight - details['weight'])

    def step(self):
        probabilities = self.transition_matrix.loc[self.state].values
        self.update_values()  # Update values at each step
        self.state = random.choices(self.states['State'].tolist(), weights=probabilities)[0]
        return self.state