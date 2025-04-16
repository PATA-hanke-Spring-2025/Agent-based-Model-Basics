import pandas as pd
from reading import read_excel, read_value_elements
import importlib


def load():
    elements_df = read_excel("value_elements.csv")
    print(f"Loaded value elements:\n{elements_df}")
    weights_df = read_excel("category_weights.csv")
    elements, weights = read_value_elements(elements_df, weights_df)

    return {
        "elements": elements,
        "category_weights": weights
    }


def evaluate_offering(probabilities, elements, category_weights, states, current_state):
    """Evaluate offering and adjust transition probabilities based on value elements."""
    print(f"[Plugin] Evaluating from state: {current_state}")

    # Sample offering scores for the simulation
    offering_scores = {key: 7 for key in elements.keys()}

    # Table stakes check
    for element, details in elements.items():
        if details['category'] == 'table_stakes':
            if offering_scores.get(element, 0) < 6:
                print(
                    f"[Plugin] ❌ Table stake '{element}' failed. Penalizing all transitions.")
                # Nearly block all transitions
                return [0.01 for _ in probabilities]

    category_scores = {cat: 0 for cat in category_weights}
    category_counts = {cat: 0 for cat in category_weights}

    for element, score in offering_scores.items():
        if element not in elements:
            continue
        category = elements[element]['category']
        weight = elements[element]['weight']

        if score >= 8:
            weighted = weight * score / 10
        elif score >= 6:
            weighted = 0.5 * weight * score / 10
        else:
            weighted = 0.1 * weight * score / 10

        category_scores[category] += weighted
        category_counts[category] += 1

    # Normalize by count
    for cat in category_scores:
        if category_counts[cat] > 0:
            category_scores[cat] /= category_counts[cat]

    # Final score (weighted across all categories)
    final_score = sum(
        category_scores[cat] * category_weights[cat] for cat in category_scores)

    print(f"[Plugin] Final value score: {final_score:.2f}")

    # Adjust probabilities: boost next state if score is high
    new_probabilities = list(probabilities)

    try:
        current_index = states.index(current_state)
        next_index = current_index + 1 if current_index + \
            1 < len(states) else current_index

        # Example boost: if value score is high, increase chance of moving to next state
        if final_score >= 0.6:
            new_probabilities[next_index] *= 1.5
        elif final_score < 0.3:
            new_probabilities[next_index] *= 0.5

        # Normalize
        total = sum(new_probabilities)
        if total > 0:
            new_probabilities = [p / total for p in new_probabilities]

    except Exception as e:
        print(f"[Plugin] Error adjusting probabilities: {e}")

    return new_probabilities


# Load plugin data on import
plugin_data = load()
elements = plugin_data["elements"]
category_weights = plugin_data["category_weights"]
