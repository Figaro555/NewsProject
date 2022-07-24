import json
import unittest

from data_loaders.nyt_loader import NYTLoader


class NYTimesTest(unittest.TestCase):
    files_path = "test/test_data/nytimes/"

    def test_get_article_data(self):
        loader = NYTLoader()

        data = json.load(open(self.files_path + "response.json", "r", encoding="utf-8"))
        result = [loader.get_article_data(article) for article in data["results"]]

        expected_result = json.load(open(self.files_path + "result.json", "r", encoding="utf-8"))

        self.assertListEqual(expected_result, result)
