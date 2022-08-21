import unittest

from test.test_data.rdd_transformer.words_to_find import words
from test.test_data.rdd_transformer.res import expected_result
from test.test_data.rdd_transformer.data import test_data

from transformers.rdd_transformer import RDDTransformer


class RDDTransformerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transformer = RDDTransformer()

    def test_find_words_success(self):
        result = [self.transformer.find_words(data, words) for data in test_data]
        self.assertListEqual(result, expected_result)

    def test_find_words_exception_with_wrong_config(self):
        with self.assertRaises(Exception) as context:
            [self.transformer.find_words(data, {"a": 3}) for data in test_data]
        self.assertTrue("Schema or config file is incorrect" in str(context.exception))

    def test_find_words_exception_with_wrong_data(self):
        with self.assertRaises(Exception) as context:
            self.transformer.find_words({"a": 3}, words)
        self.assertTrue("Schema or config file is incorrect" in str(context.exception))
