'''
Created on 25 mei 2017

@author: Robin Knoet
'''

class quitBot(object):
    '''
    quitBot module
    '''

    __MODULECOMMAND = "quit"
    __isPublicOnError = False
    __isPublicOnHelp = False
    __helpMessage = """
        Help message quit command
        Expected format:
        quit [<quit message>]
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

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def command(self,m_dictionary):
        result = [{"action": "REACT",
                "raw": m_dictionary.get("raw"),
                "type": "QUIT",
                "sender":m_dictionary.get("sender"),
                "target":m_dictionary.get("target"),
                "value": m_dictionary.get("message")
                }]
        return result
        

    
    def help(self,m_dictionary):
        if self.isPublicHelp:
            if m_dictionary.get("target").startswith("#") or m_dictionary.get("target").startswith("&"):
                    target = m_dictionary.get("target")
                    messageType = "PRIVMSG"
            else:
                target = m_dictionary.get("sender")
                messageType = "PRIVMSG"
        else:
            target = m_dictionary.get("sender")
            messageType = "NOTICE"
            
        dictList = []
        for s in self.helpMessage.split("\n").trim():
            dictList.append({"action":"RESPOND",
                             "raw": m_dictionary.get("raw"),
                             "type":messageType,
                             "target":target,
                             "message":s
                             })