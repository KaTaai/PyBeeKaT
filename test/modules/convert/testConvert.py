'''
Created on 26 mei 2017

@author: Robin Knoet
'''
import unittest
import os

from modules.convert.convert import unitConverter


class Test(unittest.TestCase):


    #def testConvert(self):
    #    C = unitConverter(["|","C:/Users/Robin Knoet/workspaces/default_workspace/PyBeeKaT"])
        
    def testTraverseGraph(self):
        C = unitConverter(["|","C:/Users/Robin Knoet/workspaces/default_workspace/PyBeeKaT"])
        foundPath = C.findShortestPath({'m': ['dm'], 'dm': ['m', 'cm'], 'cm': ['dm', 'mm', 'in'], 'mm': ['cm'], 'in': ['cm', 'ft'], 'ft': ['in']},"in", "m",[])
        self.assertListEqual(foundPath, ['in', 'cm', 'dm', 'm'], "The found path is not the same")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConvert']
    unittest.main()