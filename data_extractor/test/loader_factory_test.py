import unittest

from data_loaders.delfi_loader import DelfiLoader
from data_loaders.guardian_loader import GuardianLoader
from data_loaders.nyt_loader import NYTLoader
from loader_factory import LoaderFactory


class FactoryLoaderTest(unittest.TestCase):
    def test_create_loader_success_delfi(self):
        loader = LoaderFactory.create_loader("Delfi")
        self.assertIsInstance(loader, type(DelfiLoader()))

    def test_create_loader_success_nytimes(self):
        loader = LoaderFactory.create_loader("NYTimes")
        self.assertIsInstance(loader, type(NYTLoader()))

    def test_create_loader_success_guardian(self):
        loader = LoaderFactory.create_loader("guardian")
        self.assertIsInstance(loader, type(GuardianLoader()))

    def test_create_loader_failure(self):
        with self.assertRaises(Exception) as context:
            LoaderFactory.create_loader("")
        self.assertTrue("No such loader" in str(context.exception))



