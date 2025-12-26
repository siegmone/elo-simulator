def expected_score(r_a: float, r_b: float, alpha: float) -> (float, float):
    """
    Compute expected score in elo rating
    """
    e_a = 1.0 / (1.0 + 10 ** ((r_b - r_a) / alpha))
    e_b = 1.0 - e_a
    return e_a, e_b


def delta_elo(expected: float, score: float, k: float, alpha: float) -> float:
    """
    Compute new elo rating from score.
    """
    return k * (score - expected)
