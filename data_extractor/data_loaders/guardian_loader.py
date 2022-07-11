import requests
from bs4 import BeautifulSoup

from data_loaders.news_loader_without_api import NewsLoaderWithoutAPI


class GuardianLoader(NewsLoaderWithoutAPI):
    country = "UK"
    main_page_link = "https://www.theguardian.com/international"

    def get_article_links(self, link):
        response = requests.get(link)
        html = BeautifulSoup(response.content, 'html.parser')
        items = html.findAll("div", class_="fc-item__content")

        return [i.find("a", class_="fc-item__link")["href"] for i in items]

    def get_article_data(self, article_link):

        response = requests.get(article_link)
        article = BeautifulSoup(response.content, 'html.parser')

        title_with_author = article.find("meta", attrs={"property": "og:title"})["content"].split("|")
        try:
            return {"country": self.country,
                    "date": article.find("meta", attrs={"property": "article:published_time"})["content"],
                    "title": title_with_author[0],
                    "text": self.get_text(article, article_link),
                    "author": self.get_author(article, title_with_author)}

        except Exception as _ex:
            print(_ex)
            print(article_link)

        return None

    def get_author(self, article, title_with_author):
        if len(title_with_author) == 2:
            return title_with_author[1].strip()

        author_tag = article.find("address")
        if author_tag is not None:
            return author_tag.text

        author_tag = article.find("div", attrs={"data-gu-name": "byline"})
        if author_tag is not None:
            author = author_tag.find("span")
            if author is not None:
                return author.text

        return "John Doe"

    def get_text(self, article, link):

        if link.find("gallery") >= 0:
            text_tags_arr = article.findAll("div", class_="gallery__caption")
            return "\n".join([i.text for i in text_tags_arr])

        return article.find("div", id="maincontent").text
