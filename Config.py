import configparser, os

class Config(object):
    
    def __init__(self, filename):
        """Opens the config file and gathers all the settings"""
        print(os.path.abspath(""))
        config = configparser.RawConfigParser()
        config.readfp(open(filename))
        
        #bot details
        self.botnick = config.get("botDetails","botnick")
        self.admin = config.get("botDetails","admin")
        self.botDescription = config.get("botDetails","botDescription")
        self.commandCharacter = config.get("botDetails","commandCharacter")
        
        #connection details
        self.server = config.get("connectionDetails", "server")
        self.port = config.getint("connectionDetails", "port")
        self.channel = config.get("connectionDetails", "channel")
        
        #Module List
        self.modules = self.getModuleList(filename)
        
    def getModuleList(self, filename):
        print(os.path.abspath(""))
        config = configparser.RawConfigParser()
        config.readfp(open(filename))
        
        moduleStringList = config.get("modules", "moduleList")
        moduleList = moduleStringList.strip().split("\n")
        for i in range(len(moduleList)):
            moduleList[i] = moduleList[i].strip()
            
        return moduleList
    
def getModuleSettings(filename):
    print(os.path.abspath(""))
    config = configparser.RawConfigParser()
    moduleSettings = {}
    print("c")
    try:
        config.readfp(open(filename))
        for s in config.options("moduleConfig"):
            print(s)
        print("d")
    except FileNotFoundError:
        print("f")
    return moduleSettings