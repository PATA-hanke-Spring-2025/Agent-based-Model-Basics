import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def load_simulation_results(file_path):
    """Load simulation results from a CSV file."""
    return pd.read_csv(file_path)

def get_latest_simulation_results_file():
    """Find the most recent simulation results file based on the timestamp in the filename."""
    files = glob.glob("aggregated_simulation_results_*.csv")
    if not files:
        raise FileNotFoundError("No simulation results file found.")
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def plot_state_transitions(results_df):
    """Plot the state transitions over time, showing individual runs and the average."""
    plt.figure(figsize=(12, 8))

    # Plot individual runs
    for run_id, run_data in results_df.groupby("Run"):
        plt.plot(run_data["Current Step Number"], run_data["Current State"], alpha=0.3, label=f"Run {run_id}")

    # Map non-numeric states to numeric values
    if not pd.api.types.is_numeric_dtype(results_df["Current State"]):
        state_mapping = {state: idx for idx, state in enumerate(results_df["Current State"].unique())}
        results_df["Numeric State"] = results_df["Current State"].map(state_mapping)
    else:
        results_df["Numeric State"] = results_df["Current State"]

    # Calculate and plot the average state transitions
    avg_state_transitions = results_df.groupby("Current Step Number")["Numeric State"].mean()
    plt.plot(avg_state_transitions.index, avg_state_transitions.values, color="red", linewidth=2, label="Average State")

    plt.xlabel("Step Number")
    plt.ylabel("State (Numeric)")
    plt.title("State Transitions Over Time (Individual Runs and Average)")
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

def plot_state_distribution(results_df):
    """Plot the distribution of states across all runs."""
    state_counts = results_df["Current State"].value_counts(normalize=True) * 100
    plt.figure(figsize=(10, 6))
    state_counts.sort_index().plot(kind="bar", color="skyblue")
    plt.xlabel("State")
    plt.ylabel("Percentage of Occurrences")
    plt.title("State Distribution Across All Runs")
    plt.grid(axis="y")
    plt.show()

def plot_average_steps_per_state(results_df):
    """Plot the average number of steps spent in each state."""
    avg_steps = results_df.groupby("Current State")["Current Step Number"].mean()
    plt.figure(figsize=(10, 6))
    avg_steps.sort_index().plot(kind="bar", color="orange")
    plt.xlabel("State")
    plt.ylabel("Average Steps")
    plt.title("Average Steps Per State Across All Runs")
    plt.grid(axis="y")
    plt.show()

def main():
    try:
        simulation_results_file = get_latest_simulation_results_file()
        print(f"Using latest simulation results file: {simulation_results_file}")
        results_df = load_simulation_results(simulation_results_file)

        # List of value elements to visualize (replace with actual column names if available)
        value_elements = ["parameter1", "parameter2", "parameter3"]  # Replace with actual value element names

        # Plot state transitions
        plot_state_transitions(results_df)

        # Plot value effects
        plot_value_effects(results_df, value_elements)

        # Plot state distribution
        plot_state_distribution(results_df)

        # Plot average steps per state
        plot_average_steps_per_state(results_df)
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()