import random


def falloff_distribution(min_val: int, max_val: int, falloff_factor: float = 0.5) -> int:
    """
    Generate a random integer within the specified range [min_val, max_val]
    with a probability falloff. The falloff_factor determines how quickly
    the probability decreases as the numbers increase.

    Args:
    - min_val (int): The minimum value in the range (inclusive).
    - max_val (int): The maximum value in the range (inclusive).
    - falloff_factor (float): The probability falloff factor (default 0.5).
        !!! The lower the value, the faster the propability decreases.

    Returns:
    - int: A random number from the range [min_val, max_val] with decreasing probability.
    """
    # Create the range of values
    range_values = range(min_val, max_val + 1)
    # Generate the probabilities with an exponential falloff
    probabilities = [(falloff_factor**i) for i in range(len(range_values))]
    # Normalize the probabilities so that they sum to 1
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    # Use random.choices to select a number based on the weights
    result = random.choices(range_values, weights=probabilities, k=1)
    return result[0]
