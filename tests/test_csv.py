import os.path
import pandas as pd
from unittest import TestCase

# Path to the csv file we're writing tests for. This indirect way of getting
# to it is needed so that we can initiate the tests both from within this folder
# as well as from outside it (e.g. for Travis Integration)
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'FFMetadata20180626.csv')


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

    def testSurvey(self):
        """
        All rows should have a 'respondent' that comes from one of our instruments
        :return:
        """
        surveys = ['d', 'e', 'f', 'h', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
        self.assertEqual(len(self.df[self.df.survey.notnull()][~self.df.survey.isin(surveys)]), 0)

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

        self.assertEqual(len(self.df[self.df.topic1.notnull()][~self.df.topic1.isin(topics)]), 0)
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

    def _testFocalPerson(self):
        """
        All rows should have either a 0 or 1 for each of the 6 focal person columns
        :return:
        """
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_child.between(0, 1)]), 0)
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_mother.between(0, 1)]), 0)
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_father.between(0, 1)]), 0)
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_PCG.between(0, 1)]), 0)
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_partner.between(0, 1)]), 0)
        self.assertEqual(len(self.df[self.df.fp_child.notnull()][~self.df.fp_other.between(0, 1)]), 0)

    def _testRespondent(self):
        """
        All rows should have a respondent within the list of possible respondents
        :return:
        """
        respondents = ["Child", "Child Care Provider", "Father", "Interviewer", "Mother", "PCG", "Interviewer"]
        self.assertEqual(len(self.df[self.df.respondent.notnull()][~self.df.respondent.isin(respondents)]), 0)

    def _testMeasures(self):
        """
        All rows should have a measure within the list of possible measures
        :return:
        """
        measures = ["01 CIDI-SF for Depression", "02 CIDI-SF for Generalized Anxiety Disorder", "03 Impulsivity Scale",
                    "04 Child’s Emotionality and Shyness", "05 Aggravation in Parenting", "06 Family Mental Health History",
                    "07 Economic Hardship", "08 Alcohol Dependence", "09 Drug Dependence", "10 CED-S for Depression",
                    "11 BSI 18 for Anxiety", "12 Teen Tobacco Use", "13 Couple Relationship Quality",
                    "14 Caregiver-Child Relationship", "15 Parental Monitoring", "16 Conflict Tactics Scale",
                    "17 Pubertal Development Scale", "18 Adolescent Partner Abuse", "19 Child Behavior Problems (CBCL)",
                    "20 Task Completion and Behavior", "21 Self Description Questionnaire", "22 Delinquent Behavior",
                    "23 Legal Cynicism", "24 Adolescent Extracurricular and Community Involvement", "25 Peer Bullying",
                    "26 Social Skills Rating System (SSRS)", "27 School Climate", "28 Connectedness at School",
                    "29 Trouble at School", "30 Conner's Teacher Rating Scale - RSF",
                    "31 WISC-IV Forward and Backward Digit Span", "32 Peabody Picture Vocabulary Test-IIIA (PPVT/TVIP)",
                    "33 Woodcock Johnson Passage Comprehension and Applied Problems", "34 Scale of Positive Adolescent Functioning",
                    "35 Neighborhood Collective Efficacy", "36 Environmental Confusion Scale",
                    "37 Home Observation to Measurement of the Environment", "38 Attachment q-sort",
                    "39 Adaptive Social Behavior Inventory (ASBI)", "40 Walk a line", "41 Leiter-R Attention Sustained",
                    "42 Early Childhood Environment Rating Scale (ECERS)", "43 Family Day Care Scale (FDCRS)",
                    "44 Household Food Security"]
        self.assertEqual(len(self.df[self.df.measures.notnull()][~self.df.measures.isin(measures)]), 0)
