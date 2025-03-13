import unittest

import generation


class TestGeneration(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(generation.extract_title("# hello"), "hello")