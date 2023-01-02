"""Sungai."""
import argparse
import math
import os
import sys

from scipy import stats


def get_r2_ln(y_values):
    """Linear regression."""
    x_values = [math.log(i + 1) for i in range(len(y_values))]

    return stats.linregress(x_values, y_values)


def nested_sum(nested_list):
    """Sum of nested list."""
    return sum(nested_list)


class DirectoryRater():
    """Directory Rater."""

    def __init__(self, target, min_score):
        """Class constructor."""
        self.target = target
        self.min_score = min_score

        self.suggestions = []
        self.nodes = []
        self.skip = False
        self.warnings = []
        self.structure = []
        # self.symlink = None

    # def check_is_symlink(self, root):
    #     """Check directory is a symlink."""
    #     if os.path.islink(root):
    #         if not self.symlink:
    #             self.symlink = root
    #         return True
    #     return False

    def get_structure(self, root, dirs, files):
        """Get the directory's structure."""

    def check_unwanted_cases(self, root, dirs, files):
        """Check for empty directories leaves and nodes."""
        if len(root) > 280:
            self.warnings.append(f"Target path too long: {root}")
        elif len(files) == 0:
            if len(dirs) == 0:
                self.warnings.append(f"Empty leaf directory: {root}")
                self.skip = True
            elif len(dirs) == 1:
                self.warnings.append(f"Empty node directory: {root}")
        elif len(files) > 10000:
            self.warnings.append(f"Too many files in single directory: {root}")

    def append_current_node(self, root):
        """Append current node."""
        this_structure = self.structure[-2]
        self.nodes.append(
            [
                root,
                nested_sum(this_structure),
                # slope, intercept, r, p, se = linregress(x, y)
                get_r2_ln(this_structure)[2],
            ]
        )

    def is_ignorable(self):
        """Directory or file is ignorable."""
        return False

    def preprocess(self):
        """
        Preprocess directory.

        Post-order traversal of the target directory.
        - The objective is to go through each Element in the Tree.
        - Each node should have: the number of Elements it contains.
        - should include the current working directory count if it is > 0
        """
        for root, dirs, files in os.walk(self.target, topdown=False):
            if not self.is_ignorable():
                # self.check_is_symlink(root)
                self.check_unwanted_cases(root, dirs, files)
                if not self.skip:
                    self.get_structure(root, dirs, files)
                self.skip = False

    def score_nodes(self):
        """Score nodes."""
        # b = self.min_score - 1.0
        # y = ax + b

    def get_bad_nodes(self):
        """Get bad nodes."""

    def add_bad_nodes_to_suggestions(self):
        """Add bad nodes to suggestions."""

    def process_nodes(self):
        """Process the nodes after directory traversal."""
        self.score_nodes()
        self.nodes.sort(key=lambda node: node[3])
        self.get_bad_nodes()
        self.add_bad_nodes_to_suggestions()

    def results_message(self, verbose):
        """Build results message."""
        prefix = "[sungai]"
        message = f"{prefix} Target directory: {self.target}"
        message += f"{prefix} Score: {self.nodes[-1][1]}"
        message += f"{prefix} Errors: {len(self.suggestions)}"

        if len(self.suggestions) > 0:
            message += f"{prefix} Suggested fixes:"
            for suggestion in self.suggestions:
                message += f"{prefix} - {suggestion}"

        if verbose and len(self.warnings) > 0:
            message += f"{prefix} Warnings issued:"
            for warning in self.warnings:
                message += f"{prefix} - {warning}"

        return message

    def run(self, verbose=False):
        """Run."""
        self.preprocess()
        self.process_nodes()
        print(self.results_message(verbose))
        return len(self.suggestions)


if __name__ == "__main__":
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
        "-v",
        "--verbose",
        action="store_true",
        help="Add if you want verbose output.",
    )
    args = parser.parse_args()
    directory_rater = DirectoryRater(args.target, args.min_score)
    sys.exit(directory_rater.run(args.verbose))
