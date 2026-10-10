import numpy as np

from psychocore.irt import probability_correct


def simulate_responses(theta, a, b, n_responses=100, random_seed=42):
    """
    Generate synthetic learner responses using the 2PL IRT model.

    theta = learner ability
    a = item discrimination
    b = item difficulty
    n_responses = number of simulated responses
    random_seed = seed for reproducible results
    """

    rng = np.random.default_rng(random_seed)

    probability = probability_correct(theta, a, b)

    responses = rng.binomial(
        n=1,
        p=probability,
        size=n_responses
    )

    return responses