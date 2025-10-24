from collections import Counter
from typing import List
import json
import sys


def sumOfUnique(nums: List[int]) -> int:
    """Return the sum of elements that appear exactly once."""
    counts = Counter(nums)
    return sum(value for value, freq in counts.items() if freq == 1)


def _parse_input(raw: str) -> List[int]:
    """Decode test runner input which is provided as a JSON array."""
    if not raw.strip():
        return []

    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise ValueError("Input must be a JSON array of integers.")

    return [int(value) for value in parsed]


if __name__ == "__main__":
    numbers = _parse_input(sys.stdin.read())
    print(sumOfUnique(numbers))
