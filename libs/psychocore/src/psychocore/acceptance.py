def evaluate_item_acceptance(
    sample_size,
    point_biserial,
    min_sample_size=100,
    min_point_biserial=0.20,
):
    """Apply preliminary pilot sample-size and correlation checks."""
    reasons = []

    if sample_size < min_sample_size:
        reasons.append("Insufficient pilot responses")

    if point_biserial is None or point_biserial < min_point_biserial:
        reasons.append("Point-biserial is below the minimum threshold")

    return {
        "accepted": len(reasons) == 0,
        "reasons": reasons,
    }
