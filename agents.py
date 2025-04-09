import pandas as pd
import random
from value_calculator import ValuePropositionCalculator  # Import the value calculator
from reading import read_plugins  # Import plugin reading logic

class Agent:

    def __init__(self, transition_data, states, agent_type="seller", industry=None, size=None):
        self.transition_data = transition_data  # Ensure transition_data is initialized
        self.states = states
        self.state = states['State'].iloc[0]
        self.transition_matrix = self.create_initial_matrix()
        self.agent_type = agent_type
        self.industry = industry
        self.size = size
        self.value_calculator = ValuePropositionCalculator()  # Initialize value calculator
        self.preferences = self.initialize_preferences() if agent_type == "buyer" else None
        self.capabilities = self.initialize_capabilities() if agent_type == "seller" else None
        self.plugins, self.plugin_data, self.loaded_plugins = read_plugins(self)  # Load plugins

    def create_initial_matrix(self):
        matrix = []
        for from_state in self.states['State']:
            row = []
            for to_state in self.states['State']:
                value = self.transition_data.loc[self.transition_data['From/To'] == from_state, to_state].values[0]
                row.append(value)
            matrix.append(row)
        return pd.DataFrame(matrix, index=self.states['State'], columns=self.states['State'])

    def initialize_preferences(self):
        """Initialize buyer preferences based on industry."""
        preferences = {}
        for element in self.value_calculator.elements:
            preferences[element] = 0.8 + 0.4 * random.random()
        if self.industry == "technology":
            preferences = self.adjust_preferences(preferences, {"innovation": 1.5, "product_quality": 1.2, "scalability": 1.3})
        elif self.industry == "manufacturing":
            preferences = self.adjust_preferences(preferences, {"cost_reduction": 1.5, "time_savings": 1.3, "risk_reduction": 1.2})
        return preferences

    def adjust_preferences(self, preferences, adjustments):
        """Apply industry-specific adjustments to preferences."""
        for key, multiplier in adjustments.items():
            if key in preferences:
                preferences[key] = min(1.0, preferences[key] * multiplier)
        return preferences

    def initialize_capabilities(self):
        """Initialize seller capabilities."""
        capabilities = {}
        for element in self.value_calculator.elements:
            capabilities[element] = 4 + 4 * random.random()
        return capabilities

    def calculate_value_modifier(self, current_state):
        # Placeholder for value modifier calculation logic
        # Replace this with actual logic based on your requirements
        return 0.1 if current_state == "Proposing" else 0.0

    def apply_plugins(self, probabilities, current_state):
        """Apply plugins to modify probabilities."""
        for plugin_name, (module, function_name) in self.loaded_plugins.items():
            plugin_function = getattr(module, function_name, None)
            if callable(plugin_function):
                probabilities = plugin_function(probabilities, self.plugin_data[plugin_name], self.states['State'].tolist(), current_state)
        return probabilities

    def modify_probabilities(self, probabilities, value_modifier):
        # Modify probabilities based on the value modifier
        modified_probabilities = [min(1.0, p + value_modifier) for p in probabilities]
        # Apply plugins to further modify probabilities
        modified_probabilities = self.apply_plugins(modified_probabilities, self.state)
        return modified_probabilities

    def normalize_probabilities(self, probabilities):
        # Normalize probabilities to sum to 1.0
        total = sum(probabilities)
        if total > 0:
            return [p / total for p in probabilities]
        return probabilities

    def update_matrix(self, current_state, modified_probabilities):
        # Update the transition matrix with modified probabilities
        self.transition_matrix.loc[current_state] = modified_probabilities

    def step(self):
        probabilities = self.transition_matrix.loc[self.state].values
        value_modifier = self.calculate_value_modifier(self.state)
        modified_probabilities = self.modify_probabilities(probabilities, value_modifier)
        normalized_probabilities = self.normalize_probabilities(modified_probabilities)
        self.update_matrix(self.state, normalized_probabilities)
        self.state = random.choices(self.states['State'].tolist(), weights=normalized_probabilities)[0]
        return self.state

    def generate_offer(self, buyer):
        """Generate a value proposition offer for a buyer."""
        offer = {}
        for element, capability in self.capabilities.items():
            offer[element] = capability
        if buyer.industry in self.value_calculator.industry_knowledge:
            industry_elements = self.value_calculator.industry_knowledge[buyer.industry]
            for element, importance in industry_elements.items():
                if element in offer and importance > 0:
                    boost_factor = 1 + min(0.2, importance * 0.1)
                    offer[element] = min(10, offer[element] * boost_factor)
        return offer

    def evaluate_offers(self, offers):
        """Evaluate offers and select the best one."""
        best_offer = None
        best_value_score = 0
        for offer in offers:
            value_score, _ = self.value_calculator.evaluate_offering(offer, self.preferences)
            if value_score > best_value_score:
                best_value_score = value_score
                best_offer = offer
        return best_offer, best_value_score

class BuyerAgent(Agent):
    """Agent representing a B2B telecom buyer with state transitions."""
    def __init__(self, unique_id, model, industry, size, states, transition_data, initial_state="NOT_INTERESTED"):
        super().__init__(transition_data=transition_data, states=states, agent_type="buyer", industry=industry, size=size)
        self.unique_id = unique_id
        self.model = model
        self.state = initial_state
        self.previous_state = initial_state
        self.time_in_state = 0
        self.current_seller = None
        self.best_offer = None
        self.best_value_score = 0
        self.purchase_history = []
        self.transaction_count = 0
        self.average_value_score = 0

    def evaluate_offers(self):
        """Evaluate offers from sellers."""
        offers = []
        for seller in self.model.sellers:
            if seller.state in ["PROPOSING", "NEGOTIATING", "CLOSING"]:
                offer = seller.generate_offer(self)
                value_score, _ = self.value_calculator.evaluate_offering(offer, self.preferences)
                offers.append({"seller_id": seller.unique_id, "offer": offer, "value_score": value_score})
        if offers:
            best_offer = max(offers, key=lambda x: x["value_score"])
            self.current_seller = next(
                (seller for seller in self.model.sellers if seller.unique_id == best_offer["seller_id"]), 
                None
            )
            self.best_offer = best_offer["offer"]
            self.best_value_score = best_offer["value_score"]
        else:
            self.best_offer = None
            self.best_value_score = 0.0

    def step(self):
        """Execute one step of the buyer agent."""
        self.time_in_state += 1
        self.previous_state = self.state

        # Evaluate offers from sellers
        self.evaluate_offers()

        # If a valid offer is selected, record the seller
        if self.best_offer and self.current_seller:
            self.purchase_history.append({
                "seller_id": self.current_seller.unique_id,
                "offer": self.best_offer,
                "value_score": self.best_value_score,
            })

        # Determine the next state
        self.determine_next_state()

    def determine_next_state(self):
        """Determine the next state based on probabilities."""
        base_probs = self.model.state_manager.get_buyer_transitions(self.state)
        if not base_probs:
            return
        states = list(base_probs.keys())
        probs = list(base_probs.values())
        self.state = random.choices(states, weights=probs, k=1)[0]

class SellerAgent(Agent):
    """Agent representing a B2B telecom seller with state transitions."""
    def __init__(self, unique_id, model, strategy, states, transition_data, initial_state="PROSPECTING"):
        super().__init__(transition_data=transition_data, states=states, agent_type="seller")
        self.unique_id = unique_id
        self.model = model
        self.state = initial_state
        self.previous_state = initial_state
        self.time_in_state = 0
        self.strategy = strategy
        self.sales_history = []
        self.transaction_count = 0
        self.average_value_score = 0

    def step(self):
        """Execute one step of the seller agent."""
        self.time_in_state += 1
        self.previous_state = self.state
        # Determine the next state
        self.determine_next_state()

    def determine_next_state(self):
        """Determine the next state based on probabilities."""
        base_probs = self.model.state_manager.get_seller_transitions(self.state)
        if not base_probs:
            return
        states = list(base_probs.keys())
        probs = list(base_probs.values())
        self.state = random.choices(states, weights=probs, k=1)[0]

    def generate_offer(self, buyer):
        """Generate a value proposition offer for a buyer."""
        offer = {}
        for element, capability in self.capabilities.items():
            # Adjust the offer based on the buyer's industry preferences
            if buyer.industry in ["technology", "manufacturing", "healthcare", "finance"]:
                offer[element] = capability * random.uniform(0.8, 1.2)
            else:
                offer[element] = capability
        return offer

random.seed(42)