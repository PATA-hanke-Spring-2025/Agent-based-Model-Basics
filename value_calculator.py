import csv
import logging
import random

logging.basicConfig(level=logging.DEBUG)

class ValuePropositionCalculator:
    """Dynamic calculator for B2B value propositions with weight adjustments."""

    def __init__(self, elements_file='value_elements.csv', category_weights_file='category_weights.csv'):
        """Initialize with elements and weights loaded from CSV files."""
        self.elements_file = elements_file
        self.elements = {}
        self.category_weights = {}

        # Load elements from CSV
        try:
            with open(elements_file, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    element_name = row['element_name']
                    weight = float(row['weight'])
                    # Clamp weight between 0 and 1
                    if weight < 0 or weight > 1:
                        logging.warning(f"Weight for {element_name} is out of bounds ({weight}). Clamping to valid range.")
                        weight = max(0, min(1.0, weight))
                    self.elements[element_name] = {
                        'weight': weight,
                        'original_weight': weight,  # Store the original weight
                        'category': row['category'],
                        'touch_count': int(row['touch_count'])
                    }
        except FileNotFoundError:
            raise FileNotFoundError(f"Elements file {elements_file} not found. Please ensure it exists.")

        # Load category weights from CSV
        try:
            with open(category_weights_file, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    self.category_weights[row['category']] = float(row['weight'])
        except FileNotFoundError:
            raise FileNotFoundError(f"Category weights file {category_weights_file} not found. Please ensure it exists.")

        # Normalize weights after loading
        self.normalize_weights()

    def update_element_weight(self, element_name):
        """Update the weight of a value element based on its touch count."""
        if element_name in self.elements:
            element = self.elements[element_name]
            original_weight = element['original_weight']
            element['touch_count'] += 1
            # Adjust the weight slightly (e.g., ±5% of the original weight)
            adjustment = random.uniform(-0.05, 0.05) * original_weight
            new_weight = element['weight'] + adjustment
            # Ensure the weight stays close to the original and within [0, 1]
            element['weight'] = max(0, min(1.0, new_weight))
            # Apply a "pull" toward the original weight to stabilize
            element['weight'] += 0.1 * (original_weight - element['weight'])
            logging.debug(f"Updated weight for {element_name}: {element['weight']}")

    def randomize_weights(self):
        """Randomize weights for all value elements."""
        for element_name, details in self.elements.items():
            original_weight = details['original_weight']
            # Randomly adjust the weight slightly (for example ±5% of the original weight)
            adjustment = random.uniform(-0.05, 0.05) * original_weight
            new_weight = original_weight + adjustment
            # Weight must stay within 0 and 1
            details['weight'] = max(0, min(1.0, new_weight))
        self.normalize_weights()

    def normalize_weights(self):
        """Normalize weights so that they sum to 1 within each category."""
        category_totals = {}
        for element_name, details in self.elements.items():
            category = details['category']
            category_totals[category] = category_totals.get(category, 0) + details['weight']

        for element_name, details in self.elements.items():
            category = details['category']
            if category_totals[category] > 0:
                details['weight'] /= category_totals[category]
            else:
                logging.warning(f"Category {category} has a total weight of 0. Skipping normalization.")

    def save_elements_to_file(self):
        """Save the elements back to the CSV file without updating weights."""
        with open(self.elements_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['element_name', 'weight', 'category', 'touch_count'])
            for element_name, details in self.elements.items():
                writer.writerow([
                    element_name,
                    details['weight'],  # Save the updated weight
                    details['category'],
                    details['touch_count']
                ])
        #logging.debug(f"Saved elements to {self.elements_file}.")

    def evaluate_offering(self, offering_scores, buyer_preferences=None):
        """Evaluate a B2B offering based on its element scores and buyer preferences."""
        # Check table stakes
        for element, details in self.elements.items():
            if details['category'] == 'table_stakes':
                if element in offering_scores and offering_scores[element] < 6:
                    return 0.0, {"table_stakes_failed": element}
        
        # Calculate scores by category
        category_scores = {cat: 0 for cat in self.category_weights.keys()}
        category_counts = {cat: 0 for cat in self.category_weights.keys()}
        
        for element, score in offering_scores.items():
            if element in self.elements:
                category = self.elements[element]['category']
                
                # Apply the base weight
                weight = self.elements[element]['weight']
                
                # Apply buyer preferences if available
                if buyer_preferences and element in buyer_preferences:
                    weight *= buyer_preferences[element]
                
                # Calculate weighted score based on excellence
                if score >= 8:  # Excellent
                    weighted_score = weight * score / 10
                elif score >= 6:  # Good
                    weighted_score = 0.5 * weight * score / 10
                else:  # Poor
                    weighted_score = 0.1 * weight * score / 10
                
                category_scores[category] += weighted_score
                category_counts[category] += 1
        
        # Normalize category scores
        for cat in category_scores:
            if category_counts[cat] > 0:
                category_scores[cat] /= category_counts[cat]
        
        # Calculate overall score
        overall_score = 0
        for cat, score in category_scores.items():
            overall_score += score * self.category_weights[cat]
        
        return overall_score, category_scores