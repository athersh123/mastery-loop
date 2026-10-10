import numpy as np

from psychocore.irt import fit_item_2pl


def calibrate_item(theta, responses):
    """
    Calibrate one item using learner abilities
    and observed responses.
    """

    a, b = fit_item_2pl(
        theta,
        responses,
        initial_a=1.0,
        initial_b=0.0
    )

    return {
        "a": a,
        "b": b
    }


def run_calibration():
    """
    Run a small demonstration IRT calibration batch.
    """

    rng = np.random.default_rng(42)

    theta = rng.normal(
        0.0,
        1.0,
        1000
    )

    # Example item responses.
    true_a = 1.2
    true_b = 0.5

    from psychocore.simulate import simulate_responses

    responses = np.array([
        simulate_responses(
            ability,
            true_a,
            true_b,
            1,
            1000 + i
        )[0]
        for i, ability in enumerate(theta)
    ])

    result = calibrate_item(
        theta,
        responses
    )

    print("IRT Calibration Result")
    print("----------------------")
    print("Estimated discrimination (a):", result["a"])
    print("Estimated difficulty (b):", result["b"])


if __name__ == "__main__":
    run_calibration()