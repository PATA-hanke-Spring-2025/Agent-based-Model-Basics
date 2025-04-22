import pandas as pd
import matplotlib.pyplot as plt

def load_simulation_results(file_path):
    """Load simulation results from a CSV file."""
    return pd.read_csv(file_path)

def plot_state_transitions(results_df):
    """Plot the state transitions over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Current Step Number"], results_df["Current State"], marker='o', label="State Transitions")
    plt.xlabel("Step Number")
    plt.ylabel("State")
    plt.title("State Transitions Over Time")
    plt.grid()
    plt.legend()
    plt.show()

def plot_value_effects(results_df, value_elements):
    """Plot how value elements affect state transitions."""
    for element in value_elements:
        if element in results_df.columns:
            plt.figure(figsize=(10, 6))
            plt.plot(results_df["Current Step Number"], results_df[element], marker='o', label=f"{element} Effect")
            plt.xlabel("Step Number")
            plt.ylabel(f"{element} Value")
            plt.title(f"Effect of {element} on State Transitions")
            plt.grid()
            plt.legend()
            plt.show()

def main():
    # Path to the simulation results file
    simulation_results_file = "simulation_results.csv"  # Replace with the actual file path
    results_df = load_simulation_results(simulation_results_file)

    # List of value elements to visualize (replace with actual column names if available)
    value_elements = ["parameter1", "parameter2", "parameter3"]  # Replace with actual value element names

    # Plot state transitions
    plot_state_transitions(results_df)

    # Plot value effects
    plot_value_effects(results_df, value_elements)

if __name__ == "__main__":
    main()