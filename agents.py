import pandas as pd
import random
import os
import importlib
from reading import create_state_matrix, read_plugins

class Agent:

    def __init__(self, transition_data, states):
        self.states=states
        self.state = states['State'].iloc[0]
        self.transition_matrix = create_state_matrix(transition_data, states)
        self.read_plugins_from_file()

    def read_plugins_from_file(self):
        self.plugins, self.plugin_data, self.loaded_plugins = read_plugins(self)

    def apply_plugins(self, probabilites):
        for plugin_name, plugin_info in self.plugin_data.items():
                module, plugin_function = self.loaded_plugins[plugin_name]
                function_to_call = getattr(module, plugin_function)
                print(f"➡️  Applying plugin: {plugin_info}")
                probabilites = function_to_call(probabilites, plugin_info, self.states['State'].tolist(), self.state)
        return probabilites

    def step(self):
        probabilities = self.transition_matrix.loc[self.state].values
        if self.plugin_data is not None:
            probabilities = self.apply_plugins(probabilities)
        self.state = random.choices(self.states['State'].tolist(), weights=probabilities)[0]
        return self.state