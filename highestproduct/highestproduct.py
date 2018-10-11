from typing import List
from itertools import combinations


def highest_product(numbers: List[int]) -> int:
    """Find the highest product of three numbers in the input."""
    if len(numbers) < 3:
        raise ValueError("Input must contain at least three numbers.")
    # Naive, unscaleable solution
    return max(a * b * c for (a, b, c) in combinations(numbers, 3))
