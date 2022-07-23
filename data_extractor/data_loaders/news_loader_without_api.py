from abc import abstractmethod

from data_loaders.news_loader import NewsLoader


class NewsLoaderWithoutAPI(NewsLoader):
    country = ""
    main_page = ""

    def load_data(self):
        article_links = list(set(self.get_article_links(self.main_page_link)))
        return list(filter(None, [self.get_article_data(link) for link in article_links]))

    @abstractmethod
    def get_article_links(self, link):
        pass

    @abstractmethod
    def get_article_data(self, article):
        pass
