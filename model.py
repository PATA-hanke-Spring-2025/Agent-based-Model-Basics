import mesa
import random
import logging
from agents import BuyerAgent, SellerAgent
from state_manager import StateTransitionManager

class B2BValueElementsModel(mesa.Model):
    """Model for simulating B2B market with value-based decisions and state transitions"""

    def __init__(
        self, 
        num_buyers=50, 
        num_sellers=10, 
        buyer_industries=["technology", "manufacturing", "healthcare", "finance"],
        buyer_sizes=["small", "medium", "large"],
        elements_file='value_elements.csv',
        category_weights_file='category_weights.csv',
        transitions_file='state_transitions.csv',
        states=None,  # Add states parameter
        transition_data=None  # Add transition_data parameter
    ):
        super().__init__()
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        
        # Load configuration files for transitions
        self.state_manager = StateTransitionManager(transitions_file)
        
        # Store the states DataFrame
        self.states = states
        
        # Store the transition data
        self.transition_data = transition_data
        
        # Initialize data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total_Transactions": lambda m: self.count_transactions(),
                "Average_Value_Score": lambda m: self.average_value_score(),
                "Market_Concentration": lambda m: self.market_concentration(),
                "Buyer_States": lambda m: self.count_buyer_states(),
                "Seller_States": lambda m: self.count_seller_states()
            },
            agent_reporters={
                "Type": lambda a: a.agent_type if hasattr(a, "agent_type") else "unknown",
                "State": lambda a: a.state if hasattr(a, "state") else "unknown",
                "Transactions": lambda a: getattr(a, "transaction_count", 0),
                "Value_Score": lambda a: getattr(a, "average_value_score", 0),
            }
        )
        
        # Create buyer agents - using CSV-based value calculator
        for i in range(num_buyers):
            industry = random.choice(buyer_industries)
            size = random.choice(buyer_sizes)
            buyer = BuyerAgent(i, self, industry, size, states=self.states, transition_data=self.transition_data)  # Pass states and transition_data
            self.schedule.add(buyer)
            
        # Create seller agents - using CSV-based value calculator
        for i in range(num_sellers):
            strategy = random.choice(["balanced", "relationship", "value"])
            seller = SellerAgent(i + num_buyers, self, strategy, states=self.states, transition_data=self.transition_data)  # Pass states and transition_data
            self.schedule.add(seller)
            
        # Keep separate lists for buyer and seller agents
        self.buyers = [agent for agent in self.schedule.agents if isinstance(agent, BuyerAgent)]
        self.sellers = [agent for agent in self.schedule.agents if isinstance(agent, SellerAgent)]
        
        # Store transactions
        self.transactions = []

    def step(self):
        """Advance the model by one step."""
        # Let all agents take a step
        self.schedule.step()

        # Record transactions between buyers and sellers
        for buyer in self.buyers:
            if buyer.current_seller and buyer.best_offer:
                transaction = {
                    "buyer_id": buyer.unique_id,
                    "seller_id": buyer.current_seller.unique_id,
                    "value_score": buyer.best_value_score,  # Ensure value_score is recorded
                }
                self.transactions.append(transaction)
                buyer.transaction_count += 1
                buyer.average_value_score = (
                    (buyer.average_value_score * (buyer.transaction_count - 1) + buyer.best_value_score)
                    / buyer.transaction_count
                )
                buyer.current_seller.transaction_count += 1
                buyer.current_seller.average_value_score = (
                    (buyer.current_seller.average_value_score * (buyer.current_seller.transaction_count - 1)
                     + buyer.best_value_score)
                    / buyer.current_seller.transaction_count
                )
                logging.debug(f"Transaction recorded: {transaction}")

        # Collect data for visualization
        self.datacollector.collect(self)

    def count_transactions(self):
        """Count the total number of transactions."""
        return len(self.transactions)

    def average_value_score(self):
        """Calculate the average value score of all transactions."""
        if not self.transactions:
            return 0
        return sum(t["value_score"] for t in self.transactions if t["value_score"] > 0) / len(self.transactions)

    def market_concentration(self):
        """Calculate market concentration based on seller transactions."""
        if not self.sellers:
            return 0
        transaction_counts = [seller.transaction_count for seller in self.sellers]
        total_transactions = sum(transaction_counts)
        if total_transactions == 0:
            return 0
        return max(transaction_counts) / total_transactions

    def count_buyer_states(self):
        """Count the number of buyers in each state."""
        state_counts = {}
        for buyer in self.buyers:
            state_counts[buyer.state] = state_counts.get(buyer.state, 0) + 1
        return state_counts

    def count_seller_states(self):
        """Count the number of sellers in each state."""
        state_counts = {}
        for seller in self.sellers:
            state_counts[seller.state] = state_counts.get(seller.state, 0) + 1
        return state_counts
