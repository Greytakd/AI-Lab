"""
Tests for two_sum. One example is filled in to show the shape.
Add more yourself: the second example, an edge case, negatives, etc.
"""

from two_sum import two_sum


def test_basic_example():
    # nums[0] + nums[1] == 9
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]


# TODO: add a test where the answer is NOT the first two elements
# TODO: add a test with negative numbers
# TODO: add a test with duplicate values, e.g. two_sum([3, 3], 6)
