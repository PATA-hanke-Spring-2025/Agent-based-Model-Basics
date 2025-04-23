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
                    self.elements[element_name] = {
                        'weight': float(row['weight']),
                        'original_weight': float(row['weight']),  # Store the original weight
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

    def save_elements_to_file(self):
        """Save the elements back to the CSV file without updating weights."""
        with open(self.elements_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['element_name', 'weight', 'category', 'touch_count'])
            for element_name, details in self.elements.items():
                writer.writerow([
                    element_name,
                    details['original_weight'],  # Use the original weight instead of the updated weight
                    details['category'],
                    details['touch_count']
                ])
        logging.debug(f"Saved elements to {self.elements_file} without updating weights.")