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


def depth_set(nested_list, depth, value):
    """Set nested list to value at given depth."""
    if depth > 0:
        nested_list[0] = depth_set(nested_list[0], depth - 1, value)
    else:
        nested_list.insert(0, value)
    return nested_list


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

    def check_is_symlink(self, root):
        """Check directory is a symlink."""
        if os.path.islink(root):
            return True
        return False

    def get_structure(self, root, files):
        """Get the directory's structure."""
        depth = len(root.split("/")) - len(self.target.split("/"))

        if self.previous_dir not in root:
            self.append_current_nodes(self.previous_dir, depth, self.structure)

        if self.previous_dir != "":
            self.structure = depth_set(self.structure, depth - 1, [])

        self.structure = depth_set(self.structure, depth, 0)
        self.structure = depth_set(self.structure, depth, len(files))

    def append_current_nodes(self, root, depth, nested_structure):
        """Append current nodes."""
        if isinstance(nested_structure[0], list):
            nested_structure[0], root = self.append_current_nodes(
                root,
                depth - 1,
                nested_structure[0],
            )
            root = "/".join(root.split("/")[:-1])
        if depth <= 0:
            # print(root, depth, nested_structure)
            nested_structure.sort(reverse=True)
            if nested_structure != [0, 0]:
                self.nodes.append(
                    [
                        root,
                        sum(nested_structure),
                        get_r2_ln(nested_structure)[2],
                    ]
                )
            nested_structure = sum(nested_structure)

        return nested_structure, root

    def update_ignore_rules(self, root, files):
        """Look for any .ignore files here and add rules."""

    def ignorable(self, element, category="file"):
        """Directory or file is ignorable."""
        if category == "file":
            return False
        if category == "dir":
            return self.check_is_symlink(element)
        # print("Category not recognized")
        return False

    def preprocess(self):
        """
        Preprocess directory.

        Pre-order traversal of the target directory.
        - The objective is to go through each Element in the Tree.
        - Each node should have: the number of Elements it contains.
        - should include the current working directory count if it is > 0
        - Get information on which files or directories need ignoring
        - Allows to control traversal order when using os.walk by
            ignoring files or dirs
        """
        for root, dirs, files in os.walk(self.target, topdown=True):
            # basic validity check for root
            if len(root) > 280:
                self.warnings.append(
                    f"Target path too long or too nested: {root}"
                )
            elif len(files) == 0:
                if len(dirs) == 0:
                    self.warnings.append(f"Empty leaf directory: {root}")
                elif len(dirs) == 1:
                    self.warnings.append(f"Empty node directory: {root}")
            elif len(files) > 10000:
                self.warnings.append(
                    f"Too many files in single directory: {root}"
                )

            self.update_ignore_rules(root, files)

            dirs.sort()
            dirs = [x for x in dirs if not self.ignorable(x, category="dir")]

            files.sort()
            files = [x for x in files if not self.ignorable(x)]

            self.get_structure(root, files)
            # print(self.structure)
            self.previous_dir = root

        self.append_current_nodes(self.previous_dir, 0, self.structure)

    def get_nodes(self):
        """Get nodes."""
        return self.nodes

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
        for node in [
            x for x in sorted(
                self.nodes,
                key=lambda node: node[3],
            ) if x[3] < 0
        ]:
            self.suggestions.append(
                f"Score: {node[1]} - {node[2]} - {node[3]} - {node[0]}"
            )

    def process_nodes(self):
        """Process the nodes after directory traversal."""
        root_score = self.nodes[-1]
        self.score_nodes(root_score)
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
