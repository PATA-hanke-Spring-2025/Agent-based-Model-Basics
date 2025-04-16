import csv
import os
import logging

logging.basicConfig(level=logging.DEBUG)

class ValuePropositionCalculator:
    """Calculator for B2B value propositions based on the Elements of Value framework"""
    
    def __init__(self, elements_file='value_elements.csv', category_weights_file='category_weights.csv'):
        """Initialize with elements and weights loaded from CSV files"""
        # Load elements from CSV
        self.elements = {}
        try:
            with open(elements_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    element_name = row['element_name']
                    self.elements[element_name] = {
                        'weight': float(row['weight']),
                        'category': row['category']
                    }
        except FileNotFoundError:
            raise FileNotFoundError(f"Elements file {elements_file} not found. Please ensure it exists.")
        
        # Load category weights from CSV
        self.category_weights = {}
        try:
            with open(category_weights_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.category_weights[row['category']] = float(row['weight'])
        except FileNotFoundError:
            raise FileNotFoundError(f"Category weights file {category_weights_file} not found. Please ensure it exists.")
    
    def evaluate_offering(self, offering_scores, buyer_preferences=None):
        """Evaluate a B2B offering based on its element scores and buyer preferences"""
        logging.debug(f"Evaluating offering: {offering_scores} with preferences: {buyer_preferences}")
        
        # Check table stakes
        for element, details in self.elements.items():
            if details['category'] == 'table_stakes':
                if element in offering_scores and offering_scores[element] < 6:
                    logging.debug(f"Table stakes failed for element: {element}")
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
        
        # Ensure the overall score is meaningful
        overall_score = max(0.0, min(overall_score, 10.0))  # Clamp between 0 and 10
        
        logging.debug(f"Overall score: {overall_score}, Category scores: {category_scores}")
        return overall_score, category_scores