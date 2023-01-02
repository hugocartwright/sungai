"""Sungai."""
import argparse
import sys


class DirectoryRater():
    """Directory Rater."""

    def __init__(self, target, min_score):
        """Class constructor."""
        self.target = target
        self.min_score = min_score

    def get_structure(self, root, dirs, files):
        """Get the directory's structure."""

    def run(self):
        """Run."""
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="calculate X to the power of Y"
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
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    args = parser.parse_args()
    verbose = args.verbose
    directory_rater = DirectoryRater(args.target, args.min_score)
    sys.exit(directory_rater.run())
