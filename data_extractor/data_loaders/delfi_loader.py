import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from data_loaders.news_loader import NewsLoader


class DelfiLoader(NewsLoader):
    country = "LT"

    def load_data(self):
        main_page_link = "https://www.delfi.lt"
        article_links = list(set(self.get_article_links(main_page_link)))
        print(len(article_links))
        return list(filter(None, [self.get_article_data(link) for link in article_links]))

    def get_article_links(self, link):
        response = requests.get(link)
        html = BeautifulSoup(response.content, 'html.parser')
        links = html.findAll("h3", class_="headline-title")
        return [i.find("a")["href"] for i in links if i.find("a")["href"].startswith("https://www.delfi.lt")]

    def get_article_data(self, article_link):
        translator = Translator()
        response = requests.get(article_link)
        article = BeautifulSoup(response.content, 'html.parser')

        try:
            return {
                "country": self.country,
                "date": article.find("meta", attrs={"name": "cXenseParse:recs:publishtime"})["content"],
                "title": translator.translate(article.find("meta", attrs={"property": "og:title"})["content"],
                                              src="lt").text,
                "author": self.get_author(article),
                "text": translator.translate(self.get_text(article), src="lt").text

            }

        except Exception as _ex:
            print(_ex)
            print(article_link)
        return None

    def get_author(self, article):
        article_author_tag = article.find("div", class_="delfi-source-name")
        if article_author_tag is not None:
            return article_author_tag.text
        return "John Doe"

    def get_text(self, article):
        article_text_column_tag = article.find("div", class_="col-xs-8")
        text = ""
        if article_text_column_tag is not None:
            article_text_tag = article_text_column_tag.findAll("p")
            if len(article_text_tag) != 0:
                text = "\n".join([i.text for i in article_text_tag])

        article_text_column_tag = article.find("div", class_="video-article-body cXenseParse")

        if article_text_column_tag is not None:
            text = article_text_column_tag.text
        if len(text) > 0:
            return text
        raise Exception("no text parsed")
