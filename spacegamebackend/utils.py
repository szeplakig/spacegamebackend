import math
import random


def calculate_spread(min_value: int, max_value: int, desired_probability: float = 0.95) -> float:
    """
    Calculate the spread parameter for the Pareto-like distribution to achieve a specific probability
    that the generated integer does not exceed max_value, accounting for min_value being zero.

    Parameters:
    - min_value (int): The minimum integer value (can be zero or a positive integer).
    - max_value (int): The maximum integer value.
    - desired_probability (float): The desired probability (default is 0.95).

    Returns:
    - spread (float): The calculated spread parameter.
    """
    if not (0 < desired_probability < 1):
        raise ValueError("Desired probability must be between 0 and 1.")

    if min_value < 0:
        raise ValueError("Min value must be a natural number.")

    if min_value > max_value:
        raise ValueError("Min value must be less than or equal to max value.")

    if min_value == 0:
        # Adjusted formula when min_value is zero
        numerator = -math.log(1 - desired_probability)
        denominator = math.log(max_value + 1)
        spread = numerator / denominator
    else:
        # Original formula when min_value > 0
        numerator = math.log(1 - desired_probability)
        denominator = math.log(min_value / (max_value + min_value))
        spread = numerator / denominator

    if spread <= 0:
        raise ValueError("Calculated spread must be a positive number. Check your min_value and max_value.")

    return spread


def generate_pareto_integer(
    *,
    min_value: int = 1,
    max_value: int | None = None,
    spread: float | None = None,
    desired_probability: float = 0.95,
) -> int:
    """
    Generate a single integer sample from a Pareto-like distribution with controllable spread.

    Parameters:
    - spread (float): Controls how spread out the values are. Smaller values result in more spread.
    - min_value (int): The minimum integer value to generate (default is 1).

    Returns:
    - An integer sampled from the distribution.
    """
    if spread is None:
        if max_value is None:
            raise ValueError("Spread or max_value must be provided.")
        spread = calculate_spread(min_value, max_value, desired_probability)

    if spread <= 0:
        raise ValueError("Spread must be a positive number.")

    if min_value < 0:
        raise ValueError("Min value must be a natural number.")

    if min_value == 0:
        offset = 1
        min_value += 1
    else:
        offset = 0

    u = random.uniform(0, 1)
    return int(math.floor(min_value / (u ** (1.0 / spread)))) - offset
