from django.test import TestCase


class FirstTest(TestCase):
    def testFour(self):
        four = 2+2
        tFour = (four == 4)
        self.assertIs(tFour, True)