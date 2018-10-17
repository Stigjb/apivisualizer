import random
from itertools import combinations

import pytest

from apivisualizer.highestproduct import highest_product


class TestHighestProduct:
    def test_too_short_input(self):
        with pytest.raises(ValueError):
            highest_product([0, 6])

    def test_all_positive(self):
        numbers = [1, 6, 5, 10, 5]
        assert highest_product(numbers) == 10 * 6 * 5

    def test_all_negative(self):
        numbers = [-1, -6, -5, -10, -5]
        assert highest_product(numbers) == -1 * -5 * -5

    def test_mixed_sign_positive_result(self):
        numbers = [1, -6, -5, 10, 5]
        assert highest_product(numbers) == 10 * -6 * -5

    def test_mixed_sign_negative_result(self):
        numbers = [1, -10, 5]
        assert highest_product(numbers) == 1 * -10 * 5

    def test_zero_result(self):
        numbers = [-10, -5, -2, 0]
        assert highest_product(numbers) == 0

    def test_long_input(self):
        numbers = [6, 5, 10] + [1, 2] * 350
        assert highest_product(numbers) == 300

    def test_very_long_input(self):
        numbers = [6, 5, 10] + [1, 2] * 350 + [-10, -5] * 1000
        assert highest_product(numbers) == -10 * -10 * 10

    def test_random_inputs(self):
        def naive_implementation(numbers):
            return max(a * b * c for (a, b, c) in combinations(numbers, 3))
        for _ in range(100):
            nums = random.sample(range(-100, 100), 20)
            assert naive_implementation(nums) == highest_product(nums)
