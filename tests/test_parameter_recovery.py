import numpy as np

from psychocore.irt import fit_item_2pl
from psychocore.simulate import simulate_responses


def test_parameter_recovery():
    """
    Test whether 2PL fitting can recover
    known item parameters from synthetic data.
    """

    rng = np.random.default_rng(42)

    theta = rng.normal(0.0, 1.0, 1000)

    true_a = 1.2
    true_b = 0.5

    responses = np.array([
        simulate_responses(
            t,
            true_a,
            true_b,
            1,
            1000 + i
        )[0]
        for i, t in enumerate(theta)
    ])

    estimated_a, estimated_b = fit_item_2pl(
        theta,
        responses
    )

    a_error = abs(estimated_a - true_a)
    b_error = abs(estimated_b - true_b)

    print("True a:", true_a)
    print("Estimated a:", estimated_a)
    print("a error:", a_error)

    print("True b:", true_b)
    print("Estimated b:", estimated_b)
    print("b error:", b_error)

    assert a_error < 0.2
    assert b_error < 0.2

    print("Parameter recovery test PASSED")


if __name__ == "__main__":
    test_parameter_recovery()