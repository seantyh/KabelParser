import os
import unittest
from unittest import TestCase
import KabelParser

BASEPATH = os.path.abspath(os.path.dirname(__file__))
class TestKabelParser(TestCase):

    def testIndividual1(self):
        kabelFile = BASEPATH+"/data/idv_test_1.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)
        self.assertTrue(ret.find("Individual: 測試") >= 0)

    def testIndividual2(self):
        kabelFile = BASEPATH+"/data/idv_test_2.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)        
        self.assertTrue(ret.find("Individual: 試驗概念") >= 0)
    
    def testIndividual3(self):
        kabelFile = BASEPATH+"/data/idv_test_3.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)            
        self.assertTrue(ret.find("Individual: 試驗概念") >= 0)
        self.assertTrue(ret.find("Type: 類別") >= 0)
    
    def testBlockIndividual1(self):
        kabelFile = BASEPATH+"/data/idv_test_4.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)            
        self.assertTrue(ret.find("Individual: 試驗概念") >= 0)
        self.assertTrue(ret.find("Type: 類別") >= 0)

    def testIndividualExpansion(self):
        kabelFile = BASEPATH+"/data/idv_test_5.kabel.txt"
        ret = KabelParser.parseFile(kabelFile)                    
        self.assertTrue(ret.find("Individual: 試驗概念") >= 0)
        self.assertTrue(ret.find("Type: 類別") >= 0)
        self.assertTrue(ret.find("Individual: test") < 0)

if __name__ == "__main__":
    unittest.main()
