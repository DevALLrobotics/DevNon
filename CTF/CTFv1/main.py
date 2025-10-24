# -*- coding: utf-8 -*-
"""Local test runner for the Sum of Unique Elements challenge."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"


def _load_tests(filename: str) -> List[dict]:
    """Load tests from the given JSON file inside the tests directory."""
    path = TESTS_DIR / filename
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    tests: List[dict] = []
    for index, case in enumerate(payload.get("tests", []), start=1):
        name = case.get("name") or f"case_{index}"
        nums = case.get("input", {}).get("nums")
        expected = case.get("expected")
        if nums is None or expected is None:
            raise ValueError(f"Malformed test case in {filename}: {case}")

        tests.append({"name": name, "nums": nums, "expected": expected})
    return tests


def _run_solution(solution_path: Path, nums: Iterable[int]) -> Tuple[str, str, int]:
    """Execute the competitor solution and return stdout, stderr, and exit code."""
    cmd = [sys.executable, str(solution_path)]
    try:
        process = subprocess.run(
            cmd,
            input=json.dumps(list(nums)).encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", -1
    return process.stdout.decode().strip(), process.stderr.decode().strip(), process.returncode


def _execute_suite(label: str, solution_path: Path, tests: List[dict]) -> Tuple[int, int]:
    """Run an entire test suite and report individual outcomes."""
    print(f"\n🧪 {label}")
    passed = 0
    for index, case in enumerate(tests, start=1):
        stdout, stderr, code = _run_solution(solution_path, case["nums"])
        try:
            value = int(stdout)
        except (ValueError, TypeError):
            value = None

        name = case["name"]
        expected = case["expected"]
        if stdout == "TIMEOUT":
            print(f"  {index}. {name}: ❌ timeout")
            continue
        if code != 0:
            print(f"  {index}. {name}: ❌ runtime error (exit {code})")
            if stderr:
                print(f"     stderr: {stderr}")
            continue
        if value == expected:
            print(f"  {index}. {name}: ✅")
            passed += 1
        else:
            print(f"  {index}. {name}: ❌ expected {expected}, got {stdout or '∅'}")
            if stderr:
                print(f"     stderr: {stderr}")
    return passed, len(tests)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <solution.py>")
        raise SystemExit(1)

    solution_path = Path(sys.argv[1]).resolve()
    if not solution_path.exists():
        print(f"Solution file not found: {solution_path}")
        raise SystemExit(1)

    visible = _load_tests("visible_tests.json")
    hidden = _load_tests("hidden_tests.json")

    passed_visible, total_visible = _execute_suite("Visible Tests", solution_path, visible)
    print(f"\nVisible summary: {passed_visible}/{total_visible} passed")
    if passed_visible != total_visible:
        print("Fix visible failures before attempting hidden tests.")
        raise SystemExit(1)

    passed_hidden, total_hidden = _execute_suite("Hidden Tests", solution_path, hidden)
    print(f"\nHidden summary: {passed_hidden}/{total_hidden} passed")
    if passed_hidden == total_hidden:
        print("\n🎉 All tests passed! FLAG: flag{sum_of_unique_master}")
    else:
        print("\n⚠️ Some hidden tests failed. Keep iterating!")


if __name__ == "__main__":
    main()
