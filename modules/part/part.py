'''
Created on 25 mei 2017

@author: Robin Knoet
'''

import re

class PartChannel(object):
    '''
    PartChannel module
    
    '''
    __MODULECOMMAND = "part"
    __isPublicOnError = False
    __isPublicOnHelp = False
    __helpMessage = """
        Help message part command
        Expected format:
        part <channel> [<channel>, ..]
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
        partRegex = re.compile(r"""([#&][a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+) #a channel definition""",re.VERBOSE)
        partList = partRegex.findall(m_dictionary.get("message"))
        print(partList)
        if len(partList) == 0:
            if self.isPublicOnError:
                if m_dictionary.get("target").startswith("#") or m_dictionary.get("target").startswith("&"):
                    target = m_dictionary.get("target")
                    messageType = "PRIVMSG"
                else:
                    target = m_dictionary.get("sender")
                    messageType = "PRIVMSG"
            else:
                target = m_dictionary.get("sender")
                messageType = "NOTICE"
                
            return[{"action":"RESPOND",
                    "raw": m_dictionary.get("raw"),
                    "type":messageType,
                    "target":target,
                    "message":"".join(["The given channel(s) is/are incorrect, send the \"help ",self.moduleCommand,"\" command for more information."])
                    }]
            
        else:
            dictList = []
            for r in partList:
                dictList.append({"action": "REACT",
                        "raw": m_dictionary.get("raw"),
                        "sender":m_dictionary.get("sender"),
                        "target":m_dictionary.get("target"),
                        "type": "PART",
                        "value": r
                        })
            return dictList

    
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