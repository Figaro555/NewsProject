from abc import ABC, abstractmethod

import requests


class NewsLoader(ABC):

    country = ""
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def get_article_data(self, article):
        pass

    def do_get_request(self, link):
        response = requests.get(link)
        if response.status_code//100 != 2:
            raise Exception("failed to make request")
        return response
