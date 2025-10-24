import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCORE_PER_TEST = 100
TIMEOUT_SECONDS = 2
FLAG_VALUE = "flag{your_flag_here}"


def load_testcases(name: str) -> List[Dict[str, Any]]:
    """Load testcases from the companion JSON file."""
    base_dir = Path(__file__).resolve().parent
    path = base_dir / "tests" / f"{name}.json"
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            raise ValueError(f"{name}.json must contain a list of cases")
        for case in data:
            if not isinstance(case, dict) or "input" not in case or "expected" not in case:
                raise ValueError(f"Malformed testcase in {name}.json: {case!r}")
        return data
    except FileNotFoundError:
        print(f"Missing {path}. Make sure the testcase file exists.")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Unable to parse {path}: {exc}")
        sys.exit(1)


def run_solution(solution_path: str, input_data: Any) -> Tuple[str, str]:
    """Execute the contestant solution with the provided JSON input."""
    cmd = [sys.executable, solution_path]
    try:
        proc = subprocess.run(
            cmd,
            input=json.dumps(input_data).encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except OSError as exc:
        return "", f"Execution error: {exc}"
    return proc.stdout.decode().strip(), proc.stderr.decode().strip()


def parse_output(raw: str) -> Tuple[Optional[Any], Optional[str]]:
    """Convert the raw stdout into a Python object for comparison."""
    if raw == "TIMEOUT":
        return None, "TIMEOUT"
    if raw == "":
        return None, "No output"
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        try:
            return int(raw), None
        except ValueError:
            return None, f"Invalid JSON output: {raw!r}"


def evaluate_group(label: str, tests: List[Dict[str, Any]], solution: str, reveal_expected: bool) -> int:
    print(f"{label} Tests")
    passed = 0

    for idx, case in enumerate(tests, 1):
        input_payload = case.get("input")
        expected = case.get("expected")
        output, stderr = run_solution(solution, input_payload)

        parsed, error = parse_output(output)
        if error:
            reason = error
        elif parsed == expected:
            print(f"  Test {idx}: PASS ✅")
            passed += 1
            continue
        else:
            reason = "Wrong Answer"

        if error is None and parsed != expected and reveal_expected:
            reason = f"Expected {expected!r}, got {parsed!r}"

        if stderr:
            reason = f"{reason} (stderr: {stderr.strip()})"

        display_reason = reason if reveal_expected else reason
        print(f"  Test {idx}: FAIL ❌ {display_reason}")
    print()
    return passed


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py solution.py")
        sys.exit(1)

    solution_path = sys.argv[1]
    visible_tests = load_testcases("visible_tests")
    hidden_tests = load_testcases("hidden_tests")

    print("🧪 Running Visible Tests...")
    visible_passed = evaluate_group("Visible", visible_tests, solution_path, reveal_expected=True)
    print("🔒 Running Hidden Tests...")
    hidden_passed = evaluate_group("Hidden", hidden_tests, solution_path, reveal_expected=False)

    total_passed = visible_passed + hidden_passed
    total_tests = len(visible_tests) + len(hidden_tests)
    total_score = total_passed * SCORE_PER_TEST
    maximum_score = total_tests * SCORE_PER_TEST

    print(f"Visible Passed: {visible_passed}/{len(visible_tests)}")
    print(f"Hidden Passed: {hidden_passed}/{len(hidden_tests)}")
    print(f"Score: {total_score}/{maximum_score}")

    if total_passed == total_tests:
        print(f"\n🎉 All tests passed! FLAG: {FLAG_VALUE}")
    else:
        print("\n⚠️ Some tests failed. Keep trying!")


if __name__ == "__main__":
    main()
