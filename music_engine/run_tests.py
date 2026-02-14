#!/usr/bin/env python3
"""
Test runner script for the Music Theory Engine.

This script provides an easy way to run the test suite with different options.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=False):
    """Run the test suite.

    Args:
        test_type: Type of tests to run ('unit', 'integration', 'all')
        verbose: Enable verbose output
        coverage: Enable coverage reporting
    """
    print("Music Theory Engine - Test Suite")
    print("=" * 40)

    # Base command
    cmd = ["python", "-m", "pytest"]

    # Add test type filter
    if test_type == "unit":
        cmd.extend(["-m", "not integration"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    # 'all' runs everything

    # Add verbosity
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")

    # Add coverage
    if coverage:
        cmd.extend([
            "--cov=core",
            "--cov=models",
            "--cov=utils",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

    # Add test directory
    cmd.append("tests/")

    print(f"Running command: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)

        if result.returncode == 0:
            print("\n" + "=" * 40)
            print("✅ ALL TESTS PASSED!")
            if coverage:
                print("📊 Coverage report generated in htmlcov/")
        else:
            print("\n" + "=" * 40)
            print("❌ SOME TESTS FAILED!")
            print("Check the output above for details.")

        return result.returncode

    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        if coverage:
            print("For coverage: pip install pytest-cov")
        return 1


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run Music Theory Engine tests")
    parser.add_argument(
        "type",
        choices=["unit", "integration", "all"],
        default="all",
        nargs="?",
        help="Type of tests to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )

    args = parser.parse_args()

    return run_tests(
        test_type=args.type,
        verbose=args.verbose,
        coverage=args.coverage
    )


if __name__ == "__main__":
    sys.exit(main())