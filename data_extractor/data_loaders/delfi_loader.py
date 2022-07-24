from bs4 import BeautifulSoup

from data_loaders.news_loader_without_api import NewsLoaderWithoutAPI


class DelfiLoader(NewsLoaderWithoutAPI):
    country = "LT"
    main_page_link = "https://www.delfi.lt"

    def get_article_links(self, link):
        response = self.do_get_request(link)
        html = BeautifulSoup(response.content, 'html.parser')
        links = html.findAll("h3", class_="headline-title")
        return [i.find("a")["href"] for i in links if i.find("a")["href"].startswith("https://www.delfi.lt")]

    def get_article_data(self, article_link):
        response = self.do_get_request(article_link)
        article = BeautifulSoup(response.content, 'html.parser')

        try:
            return {
                "country": self.country,
                "date": article.find("meta", attrs={"name": "cXenseParse:recs:publishtime"})["content"],
                "title": article.find("meta", attrs={"property": "og:title"})["content"],
                "author": self.get_author(article),
                "text": self.get_text(article)
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
