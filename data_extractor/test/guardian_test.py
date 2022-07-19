import json
import os
import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from data_loaders.guardian_loader import GuardianLoader
from test_data.guardian.get_links_results import links


class GuardianTest(unittest.TestCase):
    files_path = "test_data/guardian/"

    @classmethod
    def setUpClass(cls):
        cls.loader = GuardianLoader()

    @patch("data_loaders.guardian_loader.requests")
    def test_get_links(self, requests_mock):
        with open(self.files_path + "main_page.html", "r", encoding="utf-8") as file:
            page = file.read()

        request_content_mock = MagicMock()
        request_content_mock.content = page
        requests_mock.get.return_value = request_content_mock
        result = self.loader.get_article_links("")

        self.assertListEqual(result, links)

    @patch("data_loaders.guardian_loader.requests")
    def test_get_article_data(self, requests_mock):
        result = []

        for page in self.files_generator():
            request_content_mock = MagicMock()
            request_content_mock.content = page
            requests_mock.get.return_value = request_content_mock

            article = BeautifulSoup(page, 'html.parser')
            link = self.get_link(article)
            res = self.loader.get_article_data(link)

            result.append(res)

        with open(self.files_path + "article_data_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(expected_result, result)

    def test_get_text(self):
        result = []

        for page in self.files_generator():
            article = BeautifulSoup(page, 'html.parser')
            link = self.get_link(article)

            result.append(self.loader.get_text(article, link))

        with open(self.files_path + "text_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(result, expected_result)

    def test_get_author(self):
        result = []

        for page in self.files_generator():
            article = BeautifulSoup(page, 'html.parser')
            title_with_author = article.find("meta", attrs={"property": "og:title"})["content"].split("|")

            result.append(self.loader.get_author(article, title_with_author))

        with open(self.files_path + "author_result.json", "r", encoding="utf-8") as file:
            expected_result = json.load(file)

        self.assertListEqual(result, expected_result)

    def files_generator(self):
        file_count = len(os.listdir(self.files_path + "/pages"))
        for i in range(1, file_count):
            with open(self.files_path + "pages/page" + str(i) + ".html", "r", encoding="utf-8") as file:
                yield file.read()

    def get_link(self, article):
        link_tag = article.find("script", attrs={"type": "application/ld+json", "data-schema": "WebPage"})
        if link_tag is not None:
            return json.loads(link_tag.text)["@id"]
        else:
            return json.loads(article.find("script", attrs={"type": "application/ld+json"}).text)[0]["@id"]
