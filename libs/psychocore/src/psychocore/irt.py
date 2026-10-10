import numpy as np

def probability_correct(theta, a, b):
    """
    Calculate the probability that a learner
    answers an item correctly using the 2PL IRT model.

    theta = learner ability
    a = item discrimination
    b = item difficulty
    """

    exponent = -a * (theta - b)

    probability = 1 / (1 + np.exp(exponent))

    return probability

def log_likelihood(theta, responses, a, b):
    """
    Calculate the log-likelihood of a learner's responses.

    responses = 1 for correct, 0 for incorrect
    a = item discrimination values
    b = item difficulty values
    """

    probabilities = probability_correct(theta, a, b)

    probabilities = np.clip(probabilities, 1e-10, 1 - 1e-10)

    likelihood = (
        responses * np.log(probabilities)
        + (1 - responses) * np.log(1 - probabilities)
    )

    return np.sum(likelihood)
def estimate_ability_mle(responses, a, b, theta_min=-4.0, theta_max=4.0, steps=801):
    """
    Estimate learner ability using Maximum Likelihood Estimation (MLE).

    responses = 1 for correct, 0 for incorrect
    a = item discrimination values
    b = item difficulty values
    """

    theta_values = np.linspace(theta_min, theta_max, steps)

    likelihoods = np.array([
        log_likelihood(theta, responses, a, b)
        for theta in theta_values
    ])

    best_index = np.argmax(likelihoods)

    return theta_values[best_index]
from scipy.optimize import minimize


def fit_item_2pl(theta, responses, initial_a=1.0, initial_b=0.0):
    """
    Estimate the 2PL item parameters a and b.

    theta = learner ability values
    responses = 1 for correct, 0 for incorrect
    initial_a = starting discrimination value
    initial_b = starting difficulty value
    """

    theta = np.asarray(theta, dtype=float)
    responses = np.asarray(responses, dtype=float)

    def negative_log_likelihood(parameters):
        a, b = parameters

        # Keep discrimination positive
        if a <= 0:
            return 1e10

        probabilities = probability_correct(theta, a, b)

        probabilities = np.clip(
            probabilities,
            1e-10,
            1 - 1e-10
        )

        log_likelihood_value = np.sum(
            responses * np.log(probabilities)
            + (1 - responses) * np.log(1 - probabilities)
        )

        return -log_likelihood_value

    result = minimize(
    negative_log_likelihood,
    x0=[initial_a, initial_b],
    method="Nelder-Mead",
    bounds=[
        (0.1, 3.0),
        (-4.0, 4.0)
    ]
)

    estimated_a, estimated_b = result.x

    return estimated_a, estimated_b
def fit_2pl_em(
    responses,
    initial_a=1.0,
    initial_b=0.0,
    iterations=20,
    theta_min=-4.0,
    theta_max=4.0,
    quadrature_points=41
):
    """
    Estimate 2PL item parameters using
    Marginal Maximum Likelihood EM.

    responses:
        2D array where each row is a learner
        and each column is an item.

        Example:
        [
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1]
        ]

    initial_a:
        Starting discrimination value.

    initial_b:
        Starting difficulty value.

    iterations:
        Number of EM iterations.

    theta_min / theta_max:
        Range of latent learner ability.

    quadrature_points:
        Number of ability points used in numerical integration.

    Returns:
        estimated_a, estimated_b
    """

    responses = np.asarray(
        responses,
        dtype=float
    )

    # Make sure responses are 2D
    if responses.ndim != 2:
        raise ValueError(
            "responses must be a 2D array"
        )

    # Number of learners and items
    n_learners, n_items = responses.shape

    # This function estimates ONE item's parameters.
    # Therefore, select one item column.
    if n_items < 1:
        raise ValueError(
            "At least one item is required"
        )

    # Use the first item
    item_responses = responses[:, 0]

    # -------------------------------------------------
    # Initial item parameters
    # -------------------------------------------------

    a = float(initial_a)
    b = float(initial_b)

    # -------------------------------------------------
    # Create quadrature ability grid
    # -------------------------------------------------

    theta_grid = np.linspace(
        theta_min,
        theta_max,
        quadrature_points
    )

    # Standard normal prior
    prior = np.exp(
        -0.5 * theta_grid ** 2
    )

    prior = prior / np.sum(prior)

    # -------------------------------------------------
    # EM iterations
    # -------------------------------------------------

    for iteration in range(iterations):

        # =================================================
        # E-STEP
        # =================================================

        # Probability of correct response
        p = probability_correct(
            theta_grid,
            a,
            b
        )

        p = np.clip(
            p,
            1e-10,
            1 - 1e-10
        )

        # Calculate likelihood for each learner
        # at every possible ability value.
        likelihood = np.where(
            item_responses[:, None] == 1,
            p[None, :],
            1 - p[None, :]
        )

        # Multiply likelihood by prior
        posterior = (
            likelihood * prior[None, :]
        )

        # Normalize posterior
        posterior_sum = np.sum(
            posterior,
            axis=1,
            keepdims=True
        )

        posterior_sum = np.maximum(
            posterior_sum,
            1e-12
        )

        posterior = (
            posterior / posterior_sum
        )

        # =================================================
        # M-STEP
        # =================================================

        # Expected response count at
        # every quadrature point.
        expected_correct = np.sum(
            posterior
            * item_responses[:, None],
            axis=0
        )

        expected_total = np.sum(
            posterior,
            axis=0
        )

        # Expected probability of a correct response
        expected_probability = (
            expected_correct
            / np.maximum(
                expected_total,
                1e-12
            )
        )

        expected_probability = np.clip(
            expected_probability,
            1e-6,
            1 - 1e-6
        )

        # Optimize a and b using the
        # expected complete-data likelihood.
        def negative_expected_log_likelihood(
            parameters
        ):
            new_a, new_b = parameters

            if new_a <= 0:
                return 1e10

            probability = probability_correct(
                theta_grid,
                new_a,
                new_b
            )

            probability = np.clip(
                probability,
                1e-10,
                1 - 1e-10
            )

            value = np.sum(
                expected_total
                * (
                    expected_probability
                    * np.log(probability)
                    +
                    (1 - expected_probability)
                    * np.log(1 - probability)
                )
            )

            return -value

        result = minimize(
            negative_expected_log_likelihood,
            x0=[a, b],
            method="Nelder-Mead",
            bounds=[
                (0.1, 3.0),
                (-4.0, 4.0)
            ]
        )

        new_a, new_b = result.x

        new_a = np.clip(
            new_a,
            0.1,
            3.0
        )

        new_b = np.clip(
            new_b,
            -4.0,
            4.0
        )

        # Check convergence
        parameter_change = max(
            abs(new_a - a),
            abs(new_b - b)
        )

        a = new_a
        b = new_b

        if parameter_change < 1e-5:
            break

    return a, b
def estimate_ability_eap(
    responses,
    a,
    b,
    theta_min=-4.0,
    theta_max=4.0,
    steps=801
):
    """
    Estimate learner ability using Expected A Posteriori (EAP).

    responses = 1 for correct, 0 for incorrect
    a = item discrimination values
    b = item difficulty values

    A standard normal distribution is used
    as the prior distribution.
    """

    theta_values = np.linspace(
        theta_min,
        theta_max,
        steps
    )

    # Standard normal prior
    prior = np.exp(-0.5 * theta_values ** 2)

    # Calculate likelihood for every theta value
    likelihoods = np.array([
        np.exp(
            log_likelihood(
                theta,
                responses,
                a,
                b
            )
        )
        for theta in theta_values
    ])

    # Combine likelihood and prior
    posterior = likelihoods * prior

    # Normalize posterior
    posterior_sum = np.sum(posterior)

    if posterior_sum <= 0:
        return 0.0

    posterior = posterior / posterior_sum

    # Expected value of theta
    eap = np.sum(
        theta_values * posterior
    )

    return eap
def fit_2pl_em_multi(
    responses,
    initial_a=None,
    initial_b=None,
    iterations=20,
    theta_min=-4.0,
    theta_max=4.0,
    quadrature_points=41
):
    """
    Estimate 2PL parameters for multiple items
    using Marginal Maximum Likelihood EM.

    responses:
        2D array:
        rows = learners
        columns = items

        Example:
        [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ]

    Returns:
        estimated_a, estimated_b
    """

    responses = np.asarray(
        responses,
        dtype=float
    )

    if responses.ndim != 2:
        raise ValueError(
            "responses must be a 2D array"
        )

    n_learners, n_items = responses.shape

    if n_learners < 10:
        raise ValueError(
            "At least 10 learners are recommended"
        )

    # -------------------------------------------------
    # Initial item parameters
    # -------------------------------------------------

    if initial_a is None:
        a = np.ones(n_items)

    else:
        a = np.asarray(
            initial_a,
            dtype=float
        ).copy()

    if initial_b is None:
        b = np.zeros(n_items)

    else:
        b = np.asarray(
            initial_b,
            dtype=float
        ).copy()

    # -------------------------------------------------
    # Ability quadrature grid
    # -------------------------------------------------

    theta_grid = np.linspace(
        theta_min,
        theta_max,
        quadrature_points
    )

    # Standard normal prior
    prior = np.exp(
        -0.5 * theta_grid ** 2
    )

    prior = prior / np.sum(prior)

    # -------------------------------------------------
    # EM loop
    # -------------------------------------------------

    for iteration in range(iterations):

        # =================================================
        # E-STEP
        # =================================================

        # Start with prior probability
        posterior = np.tile(
            prior,
            (n_learners, 1)
        )

        # Multiply likelihood of every item
        for j in range(n_items):

            p = probability_correct(
                theta_grid,
                a[j],
                b[j]
            )

            p = np.clip(
                p,
                1e-10,
                1 - 1e-10
            )

            correct = responses[:, j][:, None]

            likelihood = np.where(
                correct == 1,
                p[None, :],
                1 - p[None, :]
            )

            posterior *= likelihood

        # Normalize posterior
        posterior_sum = np.sum(
            posterior,
            axis=1,
            keepdims=True
        )

        posterior_sum = np.maximum(
            posterior_sum,
            1e-300
        )

        posterior /= posterior_sum

        # =================================================
        # M-STEP
        # =================================================

        old_a = a.copy()
        old_b = b.copy()

        for j in range(n_items):

            item_responses = responses[:, j]

            # Expected response probability
            expected_correct = np.sum(
                posterior
                * item_responses[:, None],
                axis=0
            )

            expected_total = np.sum(
                posterior,
                axis=0
            )

            expected_probability = (
                expected_correct
                / np.maximum(
                    expected_total,
                    1e-12
                )
            )

            expected_probability = np.clip(
                expected_probability,
                1e-6,
                1 - 1e-6
            )

            def negative_expected_log_likelihood(
                parameters
            ):
                new_a, new_b = parameters

                if new_a <= 0:
                    return 1e10

                p = probability_correct(
                    theta_grid,
                    new_a,
                    new_b
                )

                p = np.clip(
                    p,
                    1e-10,
                    1 - 1e-10
                )

                value = np.sum(
                    expected_total
                    * (
                        expected_probability
                        * np.log(p)
                        +
                        (1 - expected_probability)
                        * np.log(1 - p)
                    )
                )

                return -value

            result = minimize(
                negative_expected_log_likelihood,
                x0=[a[j], b[j]],
                method="Nelder-Mead",
                bounds=[
                    (0.1, 3.0),
                    (-4.0, 4.0)
                ]
            )

            a[j] = np.clip(
                result.x[0],
                0.1,
                3.0
            )

            b[j] = np.clip(
                result.x[1],
                -4.0,
                4.0
            )

        # =================================================
        # CONVERGENCE
        # =================================================

        change = max(
            np.max(np.abs(a - old_a)),
            np.max(np.abs(b - old_b))
        )

        if change < 1e-5:
            break

    return a, b