'''
Created on 1 mei 2017

@author: Robin Knoet
'''
import unittest

from modules.module.module import Module


class Test(unittest.TestCase):


    def testCommandRetrieval(self):
        mod = Module("Boe","Helptext")
        self.assertEqual(mod.moduleCommand, "Boe", "The command parameter has not been returned correctly")
        
    def testHelpTextRetrieval(self):
        mod = Module("Boe","Helptext", True, True)
        self.assertDictEqual(mod.getHelpText(),
                             {"result":"Helptext", "isPublic":True,"command":"Boe"},
                             "The HelpText parameter has not been returned correctly")
        
    def testGetResult(self):
        mod = Module("Boe","Helptext", True, True)
        self.assertDictEqual(mod.getResult(),
                             {"result":None,"isPublic": True,"command":"Boe"},
                             "The result dict is incorrect")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()