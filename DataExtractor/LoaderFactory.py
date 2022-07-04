from DataLoaders.NYTLoader import NYTLoader
from DataLoaders.DelfiLoader import DelfiLoader
from DataLoaders.GuardianLoader import GuardianLoader


class LoaderFactory:
    @staticmethod
    def create_loader(loader_name):
        if loader_name == "NYTimes":
            return NYTLoader()
        if loader_name == "Guardian":
            return GuardianLoader()
        if loader_name == "Delfi":
            return DelfiLoader()
        raise Exception("No such loader")

