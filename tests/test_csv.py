import os.path
import pandas as pd
from unittest import TestCase

import ffmeta

# Path to the csv file folder we're writing tests for. Only the 'latest' file in this folder is tested.
# The 'latest' file is defined as the alphabetically last file found in this folder.
# This directly corresponds to the latest file as long as we stick to the predefined convention of naming
# files as FFMetadataYYYYMMDD.csv

# This indirect way of getting to the folder is needed so that we can initiate the tests both from within this folder
# as well as from outside it (e.g. for Travis Integration)
CSV_FOLDER_PATH = os.path.join(os.path.dirname(ffmeta.__file__), 'data')


class CsvTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Since creating the DataFrame is a semi-expensive operation,
        # we do that as a class method and avoid doing it as part of setUp
        cls.df = pd.read_csv(
            os.path.join(
                CSV_FOLDER_PATH,
                sorted(os.listdir(CSV_FOLDER_PATH), reverse=True)[0]
            ),
            encoding="cp1252"
        )

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

    def testWave(self):
        """
        All rows should have a 'wave' between 0 and 6.
        :return:
        """
        self.assertEqual(len(self.df[self.df.wave.notnull()][~self.df.wave.between(1, 6)]), 0)

    def _testScope(self):
        # TODO: Enable when appropriate
        """
        All rows should have a 'scope' which matches our predefined list.
        :return:
        Come back to this when the metadata file is up to date
        """
        self.assertEqual(len(self.df[self.df.scope.notnull()][~self.df.scope.isin([2, 15, 16, 18, 20])]), 0)

    def testRespondent(self):
        """
        All rows should have a 'respondent' that comes from one of our instruments
        :return:
        """
        respondents = ['d', 'e', 'f', 'h', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
        self.assertEqual(len(self.df[self.df.respondent.notnull()][~self.df.respondent.isin(respondents)]), 0)

    def testSources(self):
        """
        All rows should have a 'source' from our predefined list
        :return:
        """
        sources = ['constructed', 'idnum', 'questionnaire', 'weight']
        self.assertEqual(len(self.df[self.df.source.notnull()][~self.df.source.isin(sources)]), 0)

    def _testTopics(self):
        """
        All rows should have a topic1 and topic2 from our predefined list
        :return:
        """
        # TODO: Enable when appropriate
        topics = ["attitudes/expectations/happiness", "behavior", "cognitive skills", "childcare - calendar",
                  "childcare services and availability",
                  "childcare center composition", "childcare staff characteristics", "accidents and injuries",
                  "disabilities", "fertility history",
                  "health behavior", "health care access and insurance", "height and weight", "medication",
                  "mental health", "physical health",
                  "sexual health and behavior", "substance use and abuse", "child living arrangements",
                  "current partner living arrangements", 'home environment',
                  "household composition", "housing status", "parents' living arrangements", "residential mobility",
                  "grandparents", "parents' family background",
                  "social support", "community participation", "neighborhood conditions", "age",
                  "citizenship and nativity", "language", "mortality",
                  "race/ethnicity", "religion", "sex/gender", "child support", "earnings", "expenses",
                  "financial assets", "household income/poverty",
                  "income tax", "material hardship", "private transfers", "public transfers and social services",
                  "educational attainment/achievement",
                  "parent school involvement", "peer characteristics", "school characteristics", "school composition",
                  "student experiences", "teacher characteristics", "employment - calendar",
                  "employment - traditional work", "employment - non-traditional work",
                  "unemployment", "work stress/flexibility", "criminal justice involvement", "legal custody",
                  "paternity", "police contact and attitudes",
                  "new partner relationship quality", "new partner relationship status",
                  "parental relationship history", "parental relationship quality",
                  "parental relationship status", "paradata", "survey weights", "child welfare services",
                  "parent-child contact", "parenting abilities", "parenting behavior"]

        self.assertEqual(len(self.df[self.df.topic1.notnull()][~self.df.topic1.isin(topics)]),0)
        self.assertEqual(len(self.df[self.df.topic2.notnull()][~self.df.topic2.isin(topics)]), 0)

    def _testWarning(self):
        """
        All rows should have a warning code from 0-5
        :return:
        """
        # TODO: Enable when appropriate

        self.assertEqual(len(self.df[self.df.warning.notnull()][~self.df.warning.between(0, 5)]), 0)

    def _testWarning2(self):
        # TODO: Enable when appropriate
        """
        All rows that have a 'warning' == 2 should have 'type' == 'cont'
        :return: the data frame of mismatches and their type
        """
        mismatches = self.df[(self.df.warning == 2) & (self.df.type != 'cont')]
        self.assertEqual(len(mismatches), 0, "The following types had warning=2 but are not continuous: {}".format(mismatches))

    def _testWarning5(self):
        # TODO: Enable when appropriate
        """
        All rows that have a 'warning' == 5 should have 'type' == 'bin'
        :return: the data frame of mismatches and their type
        """
        failed = self.df[(self.df.warning == 5) & (self.df.type != 'bin')]
        self.assertEqual(len(failed), 0, "The following types had warning=2 but are not binary: {}".format(failed))


