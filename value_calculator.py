import logging
from reading import read_value_elements, read_value_weights
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

class ValuePropositionCalculator:
    """Dynamic calculator for B2B value propositions with weight adjustments."""

    def __init__(self, elements_df, category_weights_df):
     
        self.elements = read_value_elements(elements_df)
        self.category_weights = read_value_weights(category_weights_df)
        self.normalize_weights() 

    def normalize_weights(self):
        category_to_elements = defaultdict(list)
        negative_weight_found = False

        # Sanitize input: replace negative weights with 0 and log once
        for element_name, data in self.elements.items():
            if data['weight'] < 0:
                self.elements[element_name]['weight'] = 0
                negative_weight_found = True

        if negative_weight_found:
            logging.info("Some weights were less than 0 and have been set to 0.")

        # Group elements by category
        for element_name, data in self.elements.items():
            category_to_elements[data['category']].append((element_name, data['weight']))

        # Normalize weights per category
        for category, items in category_to_elements.items():
            total_weight = sum(weight for _, weight in items)

            if total_weight == 0:
                logging.info(f"Skipping normalization for category '{category}' because total weight is 0.")
                continue

            scaling_factor = 1 / total_weight if total_weight > 1 else 1

            for element_name, weight in items:
                self.elements[element_name]['weight'] = weight * scaling_factor

    def evaluate_offering(self, offering_scores, buyer_preferences=None):
        """Evaluate a B2B offering based on its element scores and buyer preferences"""
        
        if offering_scores is None:
            # Return a default score if no offering scores are provided
            return 0.0, {"error": "No offering scores provided"}

        # Check table stakes
        for element, details in self.elements.items():
            if details['category'] == 'table_stakes':
                if element in offering_scores and offering_scores[element] < 6:
                    return 0.0, {"table_stakes_failed": element}

        # Ensure all offering scores exist in elements
        for element in offering_scores:
            if element not in self.elements:
                raise ValueError(
                    f"Offering contains unknown element: {element}")

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