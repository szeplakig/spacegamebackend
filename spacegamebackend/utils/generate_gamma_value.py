import random


def generate_gamma_value(mean: float, minimum: int = 0) -> int:
    assert mean > 0, "Mean must be a positive number."
    alpha = 1
    beta = mean / alpha

    value = random.gammavariate(alpha, beta)
    return int(value) + minimum
