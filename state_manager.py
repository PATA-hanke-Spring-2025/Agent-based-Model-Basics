import csv

class StateTransitionManager:
    """Manages state transition probabilities for agents"""
    
    def __init__(self, transitions_file='state_transitions.csv'):
        """Load state transition probabilities from CSV"""
        self.buyer_transitions = {}
        self.seller_transitions = {}
        
        try:
            with open(transitions_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    agent_type = row['agent_type']
                    from_state = row['from_state']
                    to_state = row['to_state']
                    probability = float(row['probability'])
                    
                    if agent_type == 'buyer':
                        if from_state not in self.buyer_transitions:
                            self.buyer_transitions[from_state] = {}
                        self.buyer_transitions[from_state][to_state] = probability
                    elif agent_type == 'seller':
                        if from_state not in self.seller_transitions:
                            self.seller_transitions[from_state] = {}
                        self.seller_transitions[from_state][to_state] = probability
        except FileNotFoundError:
            raise FileNotFoundError(f"Transitions file {transitions_file} not found. Please ensure it exists.")
    
    def get_buyer_transitions(self, state):
        """Get transition probabilities for a buyer state"""
        return self.buyer_transitions.get(state, {})
    
    def get_seller_transitions(self, state):
        """Get transition probabilities for a seller state"""
        return self.seller_transitions.get(state, {})