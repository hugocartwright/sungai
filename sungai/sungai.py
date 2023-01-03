"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import math
import os

from scipy import stats


def get_r2_ln(y_values):
    """Linear regression."""
    x_values = [math.log(i + 1) for i in range(len(y_values))]

    # slope, intercept, r, p, se = linregress(x, y)
    slope, intercept, r_value, _, _ = stats.linregress(x_values, y_values)
    return [slope, intercept, r_value * r_value]


def nested_sum(nested_list):
    """Sum of nested list."""
    return sum(
        nested_sum(x) if isinstance(x, list) else x for x in nested_list
    )


class DirectoryRater():
    """Directory Rater."""

    def __init__(self, target, min_score):
        """Class constructor."""
        self.target = target
        self.min_score = min_score

        self.suggestions = []
        self.nodes = []
        self.warnings = []
        self.structure = []
        self.previous_dir = ""

    # def check_is_symlink(self, root):
    #     """Check directory is a symlink."""
    #     if os.path.islink(root):
    #         if not self.symlink:
    #             self.symlink = root
    #         return True
    #     return False

    def get_structure(self, root, dirs, files):
        """Get the directory's structure."""
        if len(root) > 280:
            self.warnings.append(f"Target path too long: {root}")
        elif len(files) == 0:
            if len(dirs) == 0:
                self.warnings.append(f"Empty leaf directory: {root}")
            elif len(dirs) == 1:
                self.warnings.append(f"Empty node directory: {root}")
        elif len(files) > 10000:
            self.warnings.append(
                f"Too many files in single directory: {root}"
            )

        if root not in self.previous_dir:
            self.structure.append([])
        else:
            self.structure = self.structure[:-len(dirs)] + [
                self.structure[-len(dirs):]
            ]

        self.structure[-1].append(len(files))
        self.structure[-1].append(0)

        self.append_current_node(root)

    def append_current_node(self, root):
        """Append current node."""
        y_values = [nested_sum([x]) for x in self.structure[-1]]
        y_values.sort(reverse=True)
        if y_values != [0, 0]:
            self.nodes.append(
                [
                    root,
                    sum(y_values),
                    get_r2_ln(y_values)[2],
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
                self.get_structure(root, dirs, files)
            self.previous_dir = root

    def score_nodes(self, root_score):
        """Score nodes."""
        b_value = self.min_score - 1.0

        max_x = root_score[1]
        max_x = math.log(max_x + 1)

        a_value = 1.0 / (max_x)

        for i, node in enumerate(self.nodes):
            # y = ax + b
            score = node[2] - ((a_value * math.log(node[1] + 1)) + b_value)
            self.nodes[i].append(score)

    def get_bad_nodes(self):
        """Get bad nodes."""
        self.nodes = [x for x in self.nodes if x[3] < 0]

        for node in self.nodes:
            self.suggestions.append(
                f"Score: {node[1]} - {node[2]} - {node[3]} - {node[0]}"
            )

    def process_nodes(self):
        """Process the nodes after directory traversal."""
        root_score = self.nodes[-1]
        self.score_nodes(root_score)
        self.nodes.sort(key=lambda node: node[3])
        self.get_bad_nodes()
        return root_score

    def results_message(self, root_score, verbose):
        """Build results message."""
        prefix = "[sungai]"
        message = f"{prefix} Target directory: {self.target}\r\n"
        message += f"{prefix} Score: {root_score}\r\n"
        message += f"{prefix} Errors: {len(self.suggestions)}\r\n"

        if len(self.suggestions) > 0:
            message += f"{prefix} Suggested fixes:\r\n"
            for suggestion in self.suggestions:
                message += f"{prefix} - {suggestion}\r\n"

        if verbose and len(self.warnings) > 0:
            message += f"{prefix} Warnings issued:\r\n"
            for warning in self.warnings:
                message += f"{prefix} - {warning}\r\n"

        return message

    def run(self, verbose=False):
        """Run."""
        self.preprocess()
        root_score = self.process_nodes()
        print(self.results_message(root_score[2], verbose))
        return len(self.suggestions)
