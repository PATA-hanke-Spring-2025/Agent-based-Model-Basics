from agents import Agent

class Model:
    def __init__(self, agent):
        self.agent = agent  # Store the agent instance
        self.results = []  # Store simulation results

    def step(self):
        # Perform a single step of the simulation
        current_state = self.agent.state
        next_state = self.agent.step()
        self.results.append({
            "Current State": current_state,
            "Next State": next_state,
        })

    def save_results(self, filename):
        # Save the results to a CSV file
        import pandas as pd
        pd.DataFrame(self.results).to_csv(filename, index=False)
