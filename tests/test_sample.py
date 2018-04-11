from unittest import TestCase


class UtilsTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGreet(self):
        """
        A trivial test that should always pass. Useful to ensure a working CI workflow.
        :return:
        """
        self.assertEqual(42, 42)
