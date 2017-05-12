#import os

#from Config import getModuleSettings


class Module(object):
    __MODULECOMMAND = ""
    __HELPTEXT = ""
    __HELPISPUBLIC = None
    __COMMANDISPUBLIC = None
    def __init__(self, moduleCommand = "", helpText = "", helpIsPublic = None, commandIsPublic = None):
        self.__MODULECOMMAND = moduleCommand
        self.__HELPTEXT = helpText
        #os.path.join("config.ini")
        #getModuleSettings(os.path.join("modules","module","config.ini"))
        #C:\Users\Robin Knoet\workspaces\default_workspace\PyBeeKaT
        if helpIsPublic is not None:
            self.__HELPISPUBLIC = helpIsPublic
        else:
            pass
        
        if commandIsPublic is not None:
            self.__COMMANDISPUBLIC = commandIsPublic
        else:
            pass
        
    @property
    def moduleCommand(self):
        return self.__MODULECOMMAND
    
    @property
    def isPublicCommand(self):
        return self.__COMMANDISPUBLIC
    
    def getHelpText(self):
        return {"result":self.__HELPTEXT,"isPublic":self.__HELPISPUBLIC,"command":self.moduleCommand}
    
    def getResult(self,):
        return {"result":None,"isPublic":self.__COMMANDISPUBLIC,"command":self.moduleCommand}
    

