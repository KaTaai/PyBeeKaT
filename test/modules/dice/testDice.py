'''
Created on 24 apr. 2017

@author: Robin Knoet
'''
import unittest
from modules.dice.dice import Dice


class Test(unittest.TestCase):

    def testUniformDist(self):
        dice = Dice(5)
        uniform = dice.uniform(a=0,b=1)
        self.assertEqual(uniform, 0.6229016948897019, "The Uniform value does not equal the given value")
        
    def testIntUniformDist(self):
        dice = Dice(5)
        uniformInt = dice.uniformInt(a=1,b=10)
        self.assertEqual(uniformInt, 10, "Integer does not match")
        
    def testCommandRetrieval(self):
        dice = Dice(5,"Boe","Helptext")
        self.assertEqual(dice.moduleCommand, "Boe", "The command parameter has not been returned correctly")
        
    def testDice1d7Test(self):
        dice = Dice(5,"Boe","Helptext",True,True)
        self.assertDictEqual(dice.getResult("1d7"),
                             {"result":"1d7 is: 4", "isPublic":True,"command":"Boe"},
                             "The 1d7 dice is incorrect")
    
    def testDice11d9Test(self):
        dice = Dice(5,"Boe","Helptext",True,True)
        self.assertDictEqual(dice.getResult("11d9"),
                             {"result":"11d9 is: 44", "isPublic":True,"command":"Boe"},
                             "The 11d9 dice is incorrect")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUniformDice']
    unittest.main()