import pandas as pd
from unittest import TestCase


class CsvTestCase(TestCase):
    def setUp(self):
        self.df = pd.read_csv("../FFMetadata20171101.csv", encoding="cp1252")

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
