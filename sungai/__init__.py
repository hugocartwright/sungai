"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import argparse
import sys

from .sungai import DirectoryRater

__version__ = "0.1.0"


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
        "--min_score",
        type=float,
        help="The minimum score to pass.",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Add if you want verbose output.",
        required=False,
        default=False,
    )
    args = parser.parse_args()

    try:
        directory_rater = DirectoryRater(
            args.target,
        )
        sys.exit(directory_rater.run(args.verbose, args.min_score))
    except KeyboardInterrupt:
        sys.exit(1)
