import heapq
from typing import List


def _product(a: int, b: int, c: int) -> int:
    """Multiply three integers together."""
    return a * b * c


def highest_product(numbers: List[int]) -> int:
    """Find the highest product of three numbers in the input.

    For non-negative numbers, this is simply the product of the three
    greatest numbers in the input. For a mix of positive and negative
    numbers, this is not as simple. In that case, the result may be the
    product of two negative and one positive number, since the two signs
    cancel out.

    A naïve solution that is simple and correct, but doesn't scale well with
    input length is to simply test all combinations of three numbers:

      from itertools import combinations
      return max(a * b * c for (a, b, c) in combinations(numbers, 3))

    We can do better than this. The solution will always include the biggest
    number in the input. The remaining two numbers will either be the next
    two biggest numbers, or the two smallest numbers. This allows us to find
    the answer in time linear with the input, using a heap data structure to
    quickly find the three biggest and two smallest numbers in the input and
    compare only two products.

    Args:
        numbers: The selection from which the factors of the highest
            product will be found.

    Raises:
        ValueError if the input contains less than three items.
    """
    if len(numbers) < 3:
        raise ValueError("Input must contain at least three numbers.")

    three_largest = heapq.nlargest(3, numbers)
    largest = three_largest[0]
    two_smallest = heapq.nsmallest(2, numbers)
    candidate_1 = _product(*three_largest)
    candidate_2 = _product(largest, *two_smallest)
    return max(candidate_1, candidate_2)
