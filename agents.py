import pandas as pd
import random
import os
import importlib
from reading import create_state_matrix, read_plugins
from Plugins.elements_of_value import load

class Agent:

    def __init__(self, transition_data, states):
        self.states = states
        self.state = states['State'].iloc[0]
        self.transition_matrix = create_state_matrix(transition_data, states)
        self.plugins = None
        self.plugin_data = None
        self.loaded_plugins = None
        self.elements = None  # Initialize elements
        self.category_weights = None  # Initialize category_weights
        self.read_plugins_from_file()

    def read_plugins_from_file(self):
        self.plugins, self.plugin_data, self.loaded_plugins = read_plugins(self)
        # Load elements and category_weights from the plugin
        elements_data = load()
        self.elements = elements_data["elements"]  # Ensure elements is a dictionary
        self.category_weights = elements_data["category_weights"]  # Ensure category_weights is a dictionary
        print(f"Debug: Loaded elements in Agent: {self.elements}")

    def apply_plugins(self, probabilities):
        for plugin_name, plugin_info in self.plugin_data.items():
            module, plugin_function = self.loaded_plugins[plugin_name]
            function_to_call = getattr(module, plugin_function)
            print(f"➡️  Applying plugin: {plugin_info}")
            print(f"Debug: Elements passed to plugin: {self.elements}")
            
            # Call the plugin function with the correct arguments
            if plugin_function == "evaluate_offering":
                overall_score, _ = function_to_call(
                    {},  # Empty offering_scores since probabilities are unrelated to elements
                    self.elements,    # elements
                    self.category_weights  # category_weights
                )
                # Ensure probabilities remain a list
                probabilities = [overall_score] * len(probabilities)
            else:
                probabilities = function_to_call(
                    probabilities,
                    self.elements,
                    self.category_weights,
                    self.states['State'].tolist(),
                    self.state
                )
        return probabilities

    def step(self):
        # Get the list of states from the DataFrame
        state_list = self.states['State'].tolist()
        
        # Get the index of the current state
        current_state_index = state_list.index(self.state)
        
        # Get the transition probabilities for the current state
        probabilities = self.transition_matrix.iloc[current_state_index].tolist()
        
        # Select the next state based on the probabilities
        self.state = random.choices(state_list, weights=probabilities)[0]
        return self.state