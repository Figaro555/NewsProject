import json
import os
import unittest
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

import data_loaders
from data_loaders.delfi_loader import DelfiLoader
from test_data.delfi.get_links_results import links


class DelfiTest(unittest.TestCase):
    files_path = "test/test_data/delfi/"

    @classmethod
    def setUpClass(cls):
        cls.loader = DelfiLoader()

    @patch.object(data_loaders.delfi_loader.DelfiLoader, "do_get_request")
    def test_get_links(self, requests_mock):

        with open(self.files_path + "main_page.html", "r", encoding="utf-8") as file:
            page = file.read()

        request_content_mock = MagicMock()
        request_content_mock.content = page
        requests_mock.return_value = request_content_mock

        result = self.loader.get_article_links("")

        self.assertListEqual(result, links)

    @patch.object(data_loaders.delfi_loader.DelfiLoader, "do_get_request")
    def test_get_article_data(self, requests_mock):
        result = []

        for page in self.files_generator():
            request_content_mock = MagicMock()
            request_content_mock.content = page
            requests_mock.return_value = request_content_mock

            res = self.loader.get_article_data("")
            result.append(res)

        with open(self.files_path + "article_data_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(expected_result, result)

    def test_get_text(self):
        result = []

        for page in self.files_generator():

            article = BeautifulSoup(page, 'html.parser')
            try:
                result.append(self.loader.get_text(article))
            except Exception as _ex:
                result.append(None)

        with open(self.files_path + "text_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(result, expected_result)

    def test_get_author(self):
        result = []

        for page in self.files_generator():
            article = BeautifulSoup(page, 'html.parser')
            result.append(self.loader.get_author(article))

        with open(self.files_path + "author_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(result, expected_result)

    def files_generator(self):

        file_count = len(os.listdir(self.files_path + "/pages"))
        for i in range(1, file_count + 1):
            with open(self.files_path + "pages/page" + str(i) + ".html", "r", encoding="utf-8") as file:
                yield file.read()
