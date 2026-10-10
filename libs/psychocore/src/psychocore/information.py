import numpy as np

from psychocore.irt import probability_correct


def item_information(theta, a, b):
    """
    Calculate Fisher information for a 2PL IRT item.

    theta = learner ability
    a = item discrimination
    b = item difficulty
    """

    probability = probability_correct(theta, a, b)

    information = (a ** 2) * probability * (1 - probability)

    return information


def test_information(theta, a_values, b_values):
    """
    Calculate the total Fisher information
    provided by multiple items.

    theta = learner ability
    a_values = discrimination values of items
    b_values = difficulty values of items
    """

    total_information = 0.0

    for a, b in zip(a_values, b_values):
        total_information += item_information(theta, a, b)

    return total_information