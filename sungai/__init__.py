"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import argparse
import sys

from .sungai import DirectoryRater

__version__ = "0.0.1"


def run_sungai():
    """Run sungai."""
    parser = argparse.ArgumentParser(
        description="Sungai"
    )
    parser.add_argument(
        "target",
        type=str,
        help="The path to the target directory.",
    )
    parser.add_argument(
        "min_score",
        type=float,
        help="The minimum score to pass.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Add if you want verbose output.",
    )
    args = parser.parse_args()

    try:
        directory_rater = DirectoryRater(
            args.target,
            args.min_score,
        )
        sys.exit(directory_rater.run(args.verbose))
        sys.exit(directory_rater.run(False))

    except KeyboardInterrupt:
        sys.exit(1)
