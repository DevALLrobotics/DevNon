import json
import sys
from collections import Counter


def read_input() -> list:
    """Read JSON-encoded list from stdin."""
    data = sys.stdin.read().strip()
    if not data:
        return []
    return json.loads(data)


def sum_unique(values: list) -> int:
    """Sum numbers that appear exactly once."""
    counts = Counter(values)
    return sum(num for num, freq in counts.items() if freq == 1)


def main() -> None:
    numbers = read_input()
    result = sum_unique(numbers)
    print(result)


if __name__ == "__main__":
    main()
