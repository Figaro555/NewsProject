import requests

from Config.NYTConfig import NYTkey
from DataLoaders.NewsLoader import NewsLoader


class NYTLoader(NewsLoader):
    country = "USA"

    def load_data(self):
        url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key=" + NYTkey
        response = requests.get(url)
        content = response.json()

        return [self.get_article_data(article) for article in content["results"]]

    def get_article_data(self, article):
        return {"country": self.country,
                "title": article["title"],
                "author": article["byline"][3:],
                "date": article["created_date"],
                "article": article["abstract"]}
