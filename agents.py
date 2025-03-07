import pandas as pd

class SellerAgent:
    def __init__(self, states_file: str, matrix_file: str):
        """Initialize the SellerAgent with two Excel files"""
        self.states_file = states_file
        self.matrix_file = matrix_file
        self.states = {}  # Stores ID to State mappings
        self.transition_matrix = {}  # Stores transition probabilities


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
            matrix_df.columns = matrix_df.columns.str.strip()  # Clean spaces from header
            matrix_df = matrix_df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Clean spaces in body

            # Extract transition matrix
            header = matrix_df.columns[1:].tolist()  # State names from column headers
            for index, row in matrix_df.iterrows():
                from_state = row.iloc[0]  # First column is the 'From' state
                probabilities = row[1:].astype(float).tolist()  # Convert to float
                self.transition_matrix[from_state] = dict(zip(header, probabilities))

        except Exception as e:
            print(f"Error loading data: {e}")

    def display_data(self):
        """Print the loaded data for debugging."""
        print("States:")
        for agent_id, state in self.states.items():
            print(f"  {agent_id}: {state}")

        print("\nTransition Matrix:")
        for from_state, transitions in self.transition_matrix.items():
            print(f"  {from_state}: {transitions}")

# Example usage:
if __name__ == "__main__":
    agent = SellerAgent(r"your PATH TO FILE", r"your PATH TO FILE")
    agent.load_data()
    agent.display_data()
