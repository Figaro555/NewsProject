from abc import ABC, abstractmethod


class NewsLoader(ABC):

    country = ""
    @abstractmethod
    def load_data(self):
        pass
