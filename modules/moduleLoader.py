'''
Created on 25 mei 2017

@author: Robin Knoet
'''



class moduleLoader(object):
    '''
    Loads the modules
    '''
    moduleDict={}

    def __init__(self, params):
        '''
        initiates the modules
        '''
        self.commandCharacter = params[0]
        from modules.join.join import JoinChannel
        M = JoinChannel([])
        for c in M.moduleCommand:
            self.moduleDict[c.lower()] = M
        
        from modules.quit.quit import quitBot
        M = quitBot([])
        self.moduleDict[M.moduleCommand.lower()] = M
        
        from modules.part.part import PartChannel
        M = PartChannel([])
        self.moduleDict[M.moduleCommand.lower()] = M
        
        print(self.moduleDict)
        
    def moduleCommand(self,m_dictionary):
        if m_dictionary.get("subtype") == "COMMAND":
            if m_dictionary.get("messageAction").lower() in self.moduleDict.keys():
                result = self.moduleDict.get(m_dictionary.get("messageAction")).command(m_dictionary)
                return result
                