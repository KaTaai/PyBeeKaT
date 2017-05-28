'''
Created on 26 mei 2017

@author: Robin Knoet
'''

import configparser
import os


class unitConverter(object):
    '''
    classdocs
    '''
    __MODULECOMMAND = "convert"
    __isPublicOnError = False
    __isPublicOnHelp = False
    __helpMessage = """
        Convert message part command
        Expected format:
        convert <unit> <unit> <value>
        """
    
    @property
    def moduleCommand(self):
        return [self.__MODULECOMMAND]
    
    @property
    def isPublicOnError(self):
        return self.__isPublicOnError
    
    @property
    def isPublicHelp(self):
        return self.__isPublicOnHelp
    
    @property
    def helpMessage(self):
        return self.__helpMessage


    def addToGraph(self, unit_pair,graph = {}):
        if unit_pair.get("units")[0] not in graph: #New node
            graph[unit_pair.get("units")[0]] = [unit_pair.get("units")[1]]
        elif unit_pair.get("units")[1] not in graph.get(unit_pair.get("units")[0]): #new arc (vertex in a directed graph)
            graph.get(unit_pair.get("units")[0]).append(unit_pair.get("units")[1])
        else:
            print("There seems to be a double unitPair: " + unit_pair)
            
        if unit_pair.get("units")[1] not in graph: #New node
            graph[unit_pair.get("units")[1]] = [unit_pair.get("units")[0]]
        elif unit_pair.get("units")[0] not in graph.get(unit_pair.get("units")[1]): #new arc (vertex in a directed graph)
            graph.get(unit_pair.get("units")[1]).append(unit_pair.get("units")[0])
        else:
            print("There seems to be a double unitPair: " + unit_pair)
        return graph
    
    
    def createGraph(self, unit_pairs):
        graph = {}
        for d in unit_pairs: #build a directed graph
            graph = self.addToGraph(d,graph)
        return graph
    
    

    
    def __init__(self, params):
        '''
        Constructor
        '''
        config = configparser.RawConfigParser()
        config.readfp(open(os.path.join(params[1],"modules","convert","config.ini")))
        
        unitList = config.get("Vertices","distanceVertices").strip().split("\n")
        self.distanceUnitPairs = []
        for s in unitList:
            spaceSplit = s.split()
            factorSplit = spaceSplit[2].split(":")
            self.distanceUnitPairs.append({"units":(spaceSplit[0],spaceSplit[1]),
                                   "values":(float(factorSplit[0]),float(factorSplit[1]))})

        self.distanceGraph= self.createGraph(self.distanceUnitPairs)

    def findShortestPath(self, graph, start, end, path=[]):
        """
        finds shortest path, code from:
        https://www.python.org/doc/essays/graphs/
        """
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.findShortestPath(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath)<len(shortest):
                        shortest = newpath
        return shortest

    def command(self,m_dictionary):
        pass
    

    
    def help(self,m_dictionary):
        pass