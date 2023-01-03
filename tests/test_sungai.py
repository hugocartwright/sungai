"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import tempfile
import unittest

from sungai.sungai import DirectoryRater, get_r2_ln, nested_sum


class TestUtils(unittest.TestCase):
    """Test sungai utils."""

    def test_get_r2_ln(self):
        """Test linear regression."""
        assert round(get_r2_ln([17, 7, 4, 3])[2], 5) == 0.94668
        assert get_r2_ln([1, 0])[2] == 1.0
        assert get_r2_ln([0, 0])[2] == 0.0
        assert get_r2_ln([2, 2, 2, 2, 2])[2] == 0.0

    def test_nested_sum(self):
        """Test sum of nested list."""
        assert nested_sum([3, [4, 4, 2, 0], 0, 2, [3, [4, 2]]]) == 24
        assert nested_sum([3, 4, 5]) == 12


class TestDirectoryRater(unittest.TestCase):
    """Test DirectoryRater."""

    def setUp(self):
        """Create test directory tree."""
        self.test_dir = tempfile.TemporaryFile()

    def tearDown(self):
        """Tear down test directory tree."""
        self.test_dir.close()

    def test_get_structure(self):
        """Test get_structure method."""
        directory_rater = DirectoryRater("tests/directory_tree", 1.0)
        directory_rater.run(False)

        assert directory_rater.structure == [
            [
                [2, 0],
                [
                    [
                        [
                            [0, 0], [1, 0], 0, 0
                        ], 2, 0
                    ],
                    [1, 0],
                    [2, 0], 1, 0
                ],
                [
                    [
                        [0, 0], 17, 0
                    ],
                    [
                        [
                            [5, 0], [1, 0], 1, 0
                        ], 0, 0
                    ],
                    [
                        [2, 0], 2, 0
                    ], 3, 0
                ], 6, 0
            ]
        ]

    def test_score_nodes(self):
        """Test score_nodes method."""

    def test_run(self):
        """Test sungai output."""
        directory_rater = DirectoryRater(
            "tests/directory_tree",
            0.8786859111811026,
        )
        assert directory_rater.run(False) == 0

        directory_rater = DirectoryRater(
            "tests/directory_tree",
            1.0,
        )
        assert directory_rater.run(False) == 1
