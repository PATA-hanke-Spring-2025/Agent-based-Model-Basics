import pandas as pd
import numpy as np
import csv

class SellerAgent:
    def __init__(self, states_file: str, matrix_file: str):
        """Initialize the SellerAgent with two Excel files"""
        self.states_file = states_file
        self.matrix_file = matrix_file
        self.states = {}  # Stores ID to State mappings as a dictionary
        self.transition_matrix = []  # Stores transition probabilities as narray


    def load_data(self):        #Load the Excel files and process them as CSV-like structures
    
        try:
            # Load States mapping (States file),Clean spaces from header and body
            states_df = pd.read_excel(self.states_file)
            states_df.columns = states_df.columns.str.strip()  # Clean spaces from header
            states_df = states_df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Clean spaces in body

            # Skip the first row (headers) and use them correctly to map ID to State
            self.states = dict(zip(states_df.iloc[:, 0], states_df.iloc[:, 1]))  # First column is ID, second is State

            # Load Transition matrix (Matrix file)
            matrix_df = pd.read_excel(self.matrix_file)
            #matrix_df.columns = matrix_df.columns.str.strip()  # Clean spaces from header
            matrix_df = matrix_df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Clean spaces in body

            # Extract transition matrix
            #header = matrix_df.columns[1:].tolist()  # State names from column headers
            #self.state_names = matrix_df.iloc[:, 0].tolist() # Extract state names (optional, for reference)
            self.transition_matrix = matrix_df.iloc[:, 1:].astype(float).to_numpy() # Convert transition matrix to NumPy array (excluding the first column)

        except Exception as e:
            print(f"Error loading data: {e}")

    def display_data(self):
        """Print the loaded data for debugging."""
        print("States:")
        for agent_id, state in self.states.items():
            print(f"  {agent_id}: {state}")

        print(f"\nTransition Matrix:\n{self.transition_matrix}")
      
    def steps(self, initial_state_id: int = None, output_file: str = "seller_transitions.csv"):
        if initial_state_id is None:
            initial_state_id = list(self.states.keys())[0] # Start from the first state (INITIAL)
        
        state_id = initial_state_id
        last_state_id = list(agent.states.keys())[-1]  # Get the last state ID
        print(f"Initial State: {state_id}\nLast State: {last_state_id}")

        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Current State ID", "Current State", "Next State ID", "Next State"])
            step=1
            while state_id != last_state_id: 
                transition_probabilities = agent.transition_matrix[state_id - 1]  # Get transition row
                valid_transitions = np.where(transition_probabilities > 0)[0]   # Find valid transitions (non-zero probabilities)
                cumulative_prob = np.cumsum(transition_probabilities[valid_transitions])  # Only consider valid transitions  # Convert to cumulative probabilities
            
                random_number = np.random.random()  # Generate a random number
                next_state_row_ind = np.searchsorted(cumulative_prob, random_number)  # Find next state index
                next_state_id = valid_transitions[next_state_row_ind] + 1  # Convert index to state ID
                #print(f"Current state: {agent.states[state_id]} -> Next state: {agent.states[next_state_id]}")
                #print(f"Current state: {state_id} -> Next state: {next_state_id}")
                writer.writerow([step,state_id, self.states[state_id], next_state_id, self.states[next_state_id]])
                state_id = next_state_id  # Move to the next state       
                step+=1

# Example usage:
if __name__ == "__main__":
    agent = SellerAgent(r"C:\Users\tasha\HH\PATA\Agent-based-Model-Basics\Seller_States.xlsx", r"C:\Users\tasha\HH\PATA\Agent-based-Model-Basics\Seller_Matrix.xlsx")
    agent.load_data()
    np.random.seed(42)
    agent.display_data() 
    agent.steps() 

  
    #for i in range(10):
    #   
    #    agent.steps(None, f"seller_transitions_{i}.csv")
    #    print(f"Transition {i} completed.")

    