import logging, socket

import Config, messageParser

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Bot(object):
    """
    The bot
    Initialises it and houses all the connection commands
    """
    
    def __init__(self):
        """
        Loads the settings.
        Initialises any modules
        """
        self.settings = Config.Config("config.ini")
        self.irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.isConnected = False
        logging.info("Bot initialised")
        
    def initialContact(self):
        """
        Handles connecting to the server
        """
        self.irc.connect((self.settings.server,self.settings.port))
        self.userMessage(self.settings.botnick, self.settings.botnick, self.settings.botnick, self.settings.botDescription)
        self.nickMessage(self.settings.botnick)
        self.isConnected = True
        logging.info("Bot is connected")
        
        
    def userMessage(self, username, hostname, servername, realname):
        self.irc.send(" ".join(["USER", username, hostname, servername, realname,"\n"]).encode())
        
    def nickMessage(self, username):
        self.irc.send(" ".join(["NICK", username, "\n"]).encode())
        
    def joinMessage(self, channel):
        self.irc.send(" ".join(["JOIN", channel, "\n"]).encode())
        logging.info("Joining :"+ channel)
        
    def pingMessage(self,response):
        self.irc.send(" ".join(["PONG", response, "\n"]).encode())
        logging.debug("PONG :"+ response)
        
    def quitMessage(self,message=""):
        self.irc.send(" ".join(["QUIT", message,"\n"]).encode())
        logging.info("quitting and shutting down: "+ message)
        self.isConnected = False
    
B=Bot()

B.initialContact()
textBuffer=""
while B.isConnected:
    text=B.irc.recv(2040)
    textBuffer = textBuffer + text.decode()
    textBufferList = textBuffer.split("\n")
    logging.debug("End of the textBufferList: "+ textBufferList[-1])
    if textBufferList[-1].endswith("\r"):
        a=1
        textBuffer = ""
    else:
        a=0
        textBuffer = textBufferList[-1]
    i = 0
    while i <= len(textBufferList)-2+a:
        message = messageParser.parse(message=textBufferList[i].strip())
        logging.debug(message)
        logging.debug(textBufferList[i].strip())
        if len(message)==0:
            pass
        elif message[0] == "PING":
            B.pingMessage(message[1])
        elif 'End of /MOTD command.' in message[2]:
            B.joinMessage(B.settings.channel)
        elif message[2] == 'PRIVMSG':
            if message[4][0] == B.settings.commandCharacter:
                commandsep = message[4][1:].strip().split(" ",1)
                if commandsep[0].lower()=="join":
                    if len(commandsep) == 2:
                        B.joinMessage(commandsep[1])
                elif commandsep[0].lower() == "quit":
                    if len(commandsep) == 1:
                        B.quitMessage()
                    else:
                        B.quitMessage(commandsep[1])
    
        i+=1
        
        