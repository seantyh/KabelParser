import os
import unittest
from unittest import TestCase
import KabelParser

BASEPATH = os.path.abspath(os.path.dirname(__file__))
class TestKabelParser(TestCase):
    def testParser(self):
        kabelFile = BASEPATH+"/data/social_studies_outline.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)
        print(ret)

if __name__ == "__main__":
    unittest.main()
