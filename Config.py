import configparser

class Config(object):
    
    def __init__(self, filename):
        """Opens the config file and gathers all the settings"""
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