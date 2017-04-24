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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUniformDice']
    unittest.main()