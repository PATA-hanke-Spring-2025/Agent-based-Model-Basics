import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from model import B2BValueElementsModel
from reading import read_excel  # Import the read_excel function

def check_csv_files_exist():
    """Check that necessary CSV files exist"""
    required_files = ['value_elements.csv', 'category_weights.csv', 'state_transitions.csv']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        raise FileNotFoundError(f"The following required CSV files are missing: {missing_files}")
    else:
        print("All required CSV files found.")

def run_model(steps=50, num_buyers=30, num_sellers=8):
    """Run the B2B Value Elements model and analyze results"""
    print(f"Starting B2B Value Elements Model simulation with {num_buyers} buyers and {num_sellers} sellers")
    
    # Check that CSV files exist
    check_csv_files_exist()
    
    # Load states and transition data
    states_file = "SellerStates.csv"
    transition_file = "SellerTransition.csv"
    
    if os.path.exists("SellerStates.xlsx"):
        states_file = "SellerStates.xlsx"
    elif os.path.exists("SellerStates.xls"):
        states_file = "SellerStates.xls"
    
    if os.path.exists("SellerTransition.xlsx"):
        transition_file = "SellerTransition.xlsx"
    elif os.path.exists("SellerTransition.xls"):
        transition_file = "SellerTransition.xls"
    
    states = read_excel(states_file)
    transition_data = read_excel(transition_file)
    
    # Create the model - pass states and transition_data
    model = B2BValueElementsModel(
        num_buyers=num_buyers, 
        num_sellers=num_sellers,
        states=states,
        transition_data=transition_data
    )
    
    # Run simulation
    for i in range(steps):
        print(f"\nStep {i+1}/{steps}")
        model.step()
        
        # Print summary statistics
        print(f"  Transactions: {model.count_transactions()}")
        print(f"  Avg Value Score: {model.average_value_score():.2f}")
        
    return model

def create_visualizations(model):
    """Create visualizations of the model results"""
    # Create output directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # 1. Collect data from model
    # Create a DataFrame from the model's datacollector
    df = model.datacollector.get_model_vars_dataframe()
    
    # 2. Plot state distributions over time
    # Extract buyer states data
    buyer_states = []
    for step in range(model.schedule.steps):
        step_states = next((data for i, data in enumerate(df['Buyer_States']) if i == step), {})
        step_data = {'step': step}
        for state, count in step_states.items():
            step_data[state] = count
        buyer_states.append(step_data)
    
    buyer_df = pd.DataFrame(buyer_states)
    buyer_df = buyer_df.fillna(0)  # Replace NaN with 0
    
    # Extract seller states data
    seller_states = []
    for step in range(model.schedule.steps):
        step_states = next((data for i, data in enumerate(df['Seller_States']) if i == step), {})
        step_data = {'step': step}
        for state, count in step_states.items():
            step_data[state] = count
        seller_states.append(step_data)
    
    seller_df = pd.DataFrame(seller_states)
    seller_df = seller_df.fillna(0)  # Replace NaN with 0
    
    # Plot buyer states
    plt.figure(figsize=(12, 6))
    for state in buyer_df.columns:
        if state != 'step':
            plt.plot(buyer_df['step'], buyer_df[state], label=state)
    plt.xlabel('Step')
    plt.ylabel('Number of Buyers')
    plt.title('Buyer States Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results/buyer_states.png')
    plt.close()
    
    # Plot seller states
    plt.figure(figsize=(12, 6))
    for state in seller_df.columns:
        if state != 'step':
            plt.plot(seller_df['step'], seller_df[state], label=state)
    plt.xlabel('Step')
    plt.ylabel('Number of Sellers')
    plt.title('Seller States Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results/seller_states.png')
    plt.close()
    
    # 3. Plot transactions and value scores
    steps = range(model.schedule.steps)
    transactions_per_step = [len([t for t in model.transactions if t["buyer_id"] < step]) for step in steps]
    avg_values = [df['Average_Value_Score'][i] if i < len(df) else 0 for i in steps]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Step')
    ax1.set_ylabel('Transactions', color=color)
    ax1.plot(steps, transactions_per_step, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Average Value Score', color=color)
    ax2.plot(steps, avg_values, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Transactions and Value Scores Over Time')
    fig.tight_layout()
    plt.savefig('results/transactions_value.png')
    plt.close()
    
    # 4. Create summary visualization
    transaction_data = model.transactions
    if transaction_data:
        # Summarize transactions by seller
        seller_performance = {}
        for transaction in transaction_data:
            seller_id = transaction['seller_id']
            if seller_id not in seller_performance:
                seller_performance[seller_id] = {'count': 0, 'total_value': 0}
            seller_performance[seller_id]['count'] += 1
            seller_performance[seller_id]['total_value'] += transaction['value_score']
        
        # Calculate average value score per seller
        for seller_id, data in seller_performance.items():
            data['avg_value'] = data['total_value'] / data['count'] if data['count'] > 0 else 0
        
        # Create DataFrame for plotting
        seller_df = pd.DataFrame([
            {
                'seller_id': seller_id,
                'transactions': data['count'],
                'avg_value': data['avg_value'],
                'strategy': next((s.strategy for s in model.sellers if s.unique_id == seller_id), 'unknown')
            }
            for seller_id, data in seller_performance.items()
        ])
        
        # Plot seller performance by strategy
        plt.figure(figsize=(12, 6))
        strategies = seller_df['strategy'].unique()
        colors = {'balanced': 'blue', 'relationship': 'green', 'value': 'red', 'unknown': 'gray'}
        
        for strategy in strategies:
            strategy_data = seller_df[seller_df['strategy'] == strategy]
            plt.scatter(
                strategy_data['transactions'], 
                strategy_data['avg_value'],
                s=100, 
                color=colors.get(strategy, 'gray'),
                label=strategy, 
                alpha=0.7
            )
        
        for _, row in seller_df.iterrows():
            plt.annotate(
                f"Seller {row['seller_id']}", 
                (row['transactions'], row['avg_value']),
                xytext=(5, 5), 
                textcoords='offset points'
            )
        
        plt.xlabel('Number of Transactions')
        plt.ylabel('Average Value Score')
        plt.title('Seller Performance by Strategy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('results/seller_performance.png')
        plt.close()
    
    print("Visualizations created and saved to 'results' directory.")
    
    return model

if __name__ == "__main__":
    model = run_model(steps=50, num_buyers=30, num_sellers=8)
    print("Simulation completed successfully.")
    create_visualizations(model)
    print("Visualizations created successfully.")