from data_loaders.nyt_loader import NYTLoader
from data_loaders.delfi_loader import DelfiLoader
from data_loaders.guardian_loader import GuardianLoader


class LoaderFactory:
    @staticmethod
    def create_loader(loader_name):
        if loader_name == "NYTimes":
            return NYTLoader()
        if loader_name == "guardian":
            return GuardianLoader()
        if loader_name == "Delfi":
            return DelfiLoader()
        raise Exception("No such loader")

