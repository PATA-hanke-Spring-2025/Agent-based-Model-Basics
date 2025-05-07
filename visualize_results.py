import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_simulation_results(file_path):
    """Load simulation results from a CSV file."""
    return pd.read_csv(file_path)

def plot_closing_state_histogram(results_df):
    """Plot a histogram with a distribution curve for the 'Closing' state."""
    # Filter data for the 'Closing' state
    closing_state_data = results_df[results_df["Current State"] == "Closing"]["Current Step Number"]

    # Create the histogram with 10 deciles and overlay a curve
    plt.figure(figsize=(10, 6))
    sns.histplot(closing_state_data, bins=10, kde=True, color="blue", stat="percent", edgecolor="black")
    
    plt.xlabel("Number of Steps to Reach 'Closing'")
    plt.ylabel("Frequency")
    plt.title("Histogram with Distribution Curve for 'Closing' State")
    plt.grid(axis="y")
    plt.show()

def plot_state_transitions(results_df):
    """Plot the state transitions over time, showing individual runs and the average."""
    plt.figure(figsize=(12, 8))

    # Dynamically determine the state order, excluding "Maintaining"
    state_order = [state for state in results_df["Current State"].unique() if state != "Maintaining"]

    # Ensure "Current State" follows the defined order
    results_df["Current State"] = pd.Categorical(results_df["Current State"], categories=state_order, ordered=True)

    # Plot individual runs
    for run_id, run_data in results_df.groupby("Run"):
        plt.plot(run_data["Current Step Number"], run_data["Current State"].cat.codes, alpha=0.3, label=f"Run {run_id}")

    # Map non-numeric states to numeric values
    state_mapping = {state: idx for idx, state in enumerate(state_order)}
    results_df["Numeric State"] = results_df["Current State"].map(state_mapping).astype(float)

    # Calculate the average state transitions, excluding steps with insufficient data
    step_counts = results_df["Current Step Number"].value_counts()
    valid_steps = step_counts[step_counts > 5].index  # Exclude steps with <= 5 transitions
    filtered_results = results_df[results_df["Current Step Number"].isin(valid_steps)]
    avg_state_transitions = filtered_results.groupby("Current Step Number")["Numeric State"].mean()

    # Plot the average state transitions
    plt.plot(avg_state_transitions.index, avg_state_transitions.values, color="red", linewidth=2, label="Average State")

    # Update y-axis ticks to show state names
    plt.yticks(range(len(state_order)), state_order)

    plt.xlabel("Step Number")
    plt.ylabel("State")
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

def main(filename):
    simulation_results_file = filename
    results_df = load_simulation_results(simulation_results_file)

    # List of value elements to visualize (replace with actual column names if available)
    value_elements = ["parameter1", "parameter2", "parameter3"]  # Replace with actual value element names

    # Plot histogram for 'Closing' state
    plot_closing_state_histogram(results_df)

    # Plot state transitions
    plot_state_transitions(results_df)

    # Plot value effects
    plot_value_effects(results_df, value_elements)

    # Plot state distribution
    plot_state_distribution(results_df)

    # Plot average steps per state
    plot_average_steps_per_state(results_df)

if __name__ == "__main__":
    main()