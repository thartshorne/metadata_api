import os.path
import pandas as pd
from unittest import TestCase

import ffmeta

# Path to the csv file we're writing tests for. This indirect way of getting
# to it is needed so that we can initiate the tests both from within this folder
# as well as from outside it (e.g. for Travis Integration)
CSV_PATH = os.path.join(os.path.dirname(ffmeta.__file__), 'data', 'FFMetadata20171101.csv')


class CsvTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Since creating the DataFrame is a semi-expensive operation,
        # we do that as a class method and avoid doing it as part of setUp
        cls.df = pd.read_csv(CSV_PATH, encoding="cp1252")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTypes(self):
        """
        All rows should have a 'type' which matches our predefined list.
        :return:
        """
        types = ["bin", "cont", "oc", "uc", "string", "ID Number"]
        self.assertEqual(len(self.df[self.df.type.notnull()][~self.df.type.isin(types)]), 0)

    def _testWarning2(self):
        # TODO: Enable when appropriate
        mismatches = self.df[(self.df.warning == 2) & (self.df.type != 'cont')]
        self.assertEqual(len(mismatches), 0, "The following types had warning=2 but are not continuous: {}".format(mismatches))
