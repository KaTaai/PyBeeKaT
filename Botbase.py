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
        
        
    def message(self,message):
        self.irc.send(message.encode())
        
    def userMessage(self, username, hostname, servername, realname):
        self.message(" ".join(["USER", username, hostname, servername, realname,"\n"]))
        
    def nickMessage(self, username):
        self.message(" ".join(["NICK", username, "\n"]))
        
    def joinMessage(self, channel):
        self.message(" ".join(["JOIN", channel, "\n"]))
        logging.info("Joining :"+ channel)
        
    def pingMessage(self,response):
        self.message(" ".join(["PONG", response, "\n"]))
        logging.debug("PONG :"+ response)
        
    def partMessage(self, channel):
        self.message(" ".join(["PART", channel,"\n"]))
        logging.info("leaving the channel: "+ channel)
        
    def quitMessage(self,message=""):
        self.message(" ".join(["QUIT :", message,"\n"]))
        logging.info("quitting and shutting down: "+ message)
        self.isConnected = False
        
    def whoisMessage(self,nick):
        self.message(" ".join(["WHOIS", nick, "\n"]))
        logging.info("Whois query sent about: " + nick)
        
    def PRIVMSGMessage(self,receiver,message):
        
        self.message(" ".join([
            ":"+self.settings.botnick,
            "PRIVMSG",
            receiver,
            ":"+message,
            "\n"
            ]))
        logging.info("Message: '" + message + "' sent to: '" + receiver + "'")
    
B=Bot()

B.initialContact()
textBuffer=""
while B.isConnected:
    text=B.irc.recv(2040)
    textBuffer = textBuffer + text.decode()
    textBufferList = textBuffer.split("\n")
    if textBufferList[-1].endswith("\r"):
        a=1
        textBuffer = ""
    else:
        a=0
        textBuffer = textBufferList[-1]
    i = 0
    while i <= len(textBufferList)-2+a:
        message = messageParser.parse(message=textBufferList[i].strip())
        #logging.debug(message)
        #logging.debug(textBufferList[i].strip())
        if len(message)==0:
            logging.debug("message that isn't parsed: "+ textBufferList[i].strip())
        elif message[0] == "PING":
            B.pingMessage(message[1])
            
        else:
            try:
                code = int(message[0])
                if code == 376:
                    B.joinMessage(B.settings.channel)
                elif code == 372:
                    pass
                else:
                    logging.debug("codemessage that is parsed: "+ textBufferList[i].strip())
            except ValueError:
                if message[1] == 'PRIVMSG':
                    logging.debug("PRIVMSG that is parsed: "+ textBufferList[i].strip())
                    if message[3][0] == B.settings.commandCharacter:
                        commandsep = message[3][1:].strip().split(" ",1)
                        if commandsep[0].lower()=="join":
                            if len(commandsep) == 2:
                                B.joinMessage(commandsep[1])
                        elif commandsep[0].lower() == "quit":
                            if len(commandsep) == 1:
                                B.quitMessage()
                            else:
                                B.quitMessage(commandsep[1])
                        elif commandsep[0].lower() == "part":
                            if len(commandsep) == 1:
                                B.partMessage(message[3])
                            else:
                                B.partMessage(commandsep[1])
                        elif commandsep[0].lower() == "whois":
                            if len(commandsep)> 1:
                                B.whoisMessage(commandsep[1])
                        elif commandsep[0].lower() == "say":
                            if len(commandsep)> 1:
                                B.PRIVMSGMessage(message[2],commandsep[1])
                elif message[1] == "NOTICE":
                    logging.info("Notice from: '" + message[0] + "' on: '" + message[2] + "' with: '" + message[3] + "'")
                else:
                    logging.debug("message that is parsed: "+ textBufferList[i].strip())
    
        i+=1
        
        