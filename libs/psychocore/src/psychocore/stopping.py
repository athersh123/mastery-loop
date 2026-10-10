import math


def standard_error(test_information):
    """
    Calculate the standard error of ability estimation.

    SE = 1 / sqrt(test information)
    """

    if test_information <= 0:
        return float("inf")

    return 1 / math.sqrt(test_information)


def should_stop(
    test_information,
    item_count,
    se_threshold=0.3,
    max_items=20
):
    """
    Decide whether an adaptive test should stop.

    test_information = total Fisher information
    item_count = number of questions answered
    se_threshold = maximum acceptable standard error
    max_items = maximum number of questions
    """
    se = standard_error(test_information)
    if se <= se_threshold:
        return True

    if item_count >= max_items:
        return True

    return False