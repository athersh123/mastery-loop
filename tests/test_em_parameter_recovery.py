import numpy as np

from psychocore.irt import (
    fit_2pl_em_multi,
    probability_correct
)


def test_em_parameter_recovery():

    rng = np.random.default_rng(42)

    # Simulate learner abilities
    theta = rng.normal(
        0.0,
        1.0,
        2000
    )

    # Known item parameters
    true_a = np.array([
        1.2,
        0.8,
        1.5,
        1.0,
        1.3
    ])

    true_b = np.array([
        0.5,
        -0.5,
        1.0,
        0.0,
        -1.0
    ])

    # Generate learner responses
    responses = np.column_stack([
        rng.binomial(
            1,
            probability_correct(
                theta,
                true_a[j],
                true_b[j]
            )
        )
        for j in range(5)
    ])

    # Estimate parameters using EM
    estimated_a, estimated_b = fit_2pl_em_multi(
        responses,
        iterations=30
    )

    # Calculate recovery errors
    a_error = np.abs(
        estimated_a - true_a
    )

    b_error = np.abs(
        estimated_b - true_b
    )

    print("True a:", true_a)
    print("Estimated a:", estimated_a)

    print("True b:", true_b)
    print("Estimated b:", estimated_b)

    print("Maximum a error:", np.max(a_error))
    print("Mean a error:", np.mean(a_error))

    print("Maximum b error:", np.max(b_error))
    print("Mean b error:", np.mean(b_error))

    # Recovery tolerance
    assert np.max(a_error) < 0.2
    assert np.max(b_error) < 0.2

    print("EM parameter recovery test PASSED")


if __name__ == "__main__":
    test_em_parameter_recovery()