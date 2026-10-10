from psychocore.information import item_information


def select_max_information(theta, items):
    """
    Select the item that provides the maximum
    Fisher information for the learner.

    theta = learner ability

    items = list of dictionaries containing:
        id = item ID
        a = discrimination
        b = difficulty
    """

    best_item = None
    best_information = -1.0

    for item in items:
        information = item_information(
            theta,
            item["a"],
            item["b"]
        )

        if information > best_information:
            best_information = information
            best_item = item

    return best_item
def select_with_exposure_control(theta, items, max_exposure=5):
    """
    Select the maximum-information item while
    respecting an exposure limit.

    Each item should contain:
        id = item ID
        a = discrimination
        b = difficulty
        exposure = number of times the item was used
    """

    eligible_items = []

    for item in items:
        if item.get("exposure", 0) < max_exposure:
            eligible_items.append(item)

    if not eligible_items:
        return None

    return select_max_information(theta, eligible_items)
def select_with_coverage(theta, items, covered_skills):
    """
    Select an item while considering skill coverage.

    theta = learner ability

    items = list of dictionaries containing:
        id = item ID
        a = discrimination
        b = difficulty
        skill = skill name

    covered_skills = skills that have already been tested
    """

    uncovered_items = []

    for item in items:
        if item["skill"] not in covered_skills:
            uncovered_items.append(item)

    if uncovered_items:
        return select_max_information(theta, uncovered_items)

    return select_max_information(theta, items)

def select_with_coverage_and_exposure(
    theta,
    items,
    covered_skills,
    max_exposure=5,
):
    """Prefer uncovered skills while respecting item exposure limits."""
    eligible_items = [
        item for item in items
        if item.get("exposure", 0) < max_exposure
    ]

    if not eligible_items:
        return None

    uncovered_items = [
        item for item in eligible_items
        if item["skill"] not in covered_skills
    ]

    candidates = uncovered_items or eligible_items
    return select_max_information(theta, candidates)
