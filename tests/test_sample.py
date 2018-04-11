from unittest import TestCase


class SampleTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSample(self):
        """
        A trivial test that should always pass. Useful to ensure a working CI workflow.
        :return:
        """
        self.assertEqual(42, 42)
