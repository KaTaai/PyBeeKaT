from time import sleep

import logging, socket

import Config, messageParser
from modules.moduleLoader import moduleLoader
from collections import deque
#from modules.module.module import Module
logging.basicConfig(level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Bot(object):
    """
    The bot
    Initialises it and houses all the connection commands
    """
    currentchannels = []
    def __init__(self):
        """
        Loads the settings.
        Initialises any modules
        """
        
        self.settings = Config.Config("config.ini")
        #Needed for the loading of modules http://stackoverflow.com/a/8719100
        self.ML = moduleLoader([self.settings.commandCharacter])
        logging.info("settings and modules loaded.")
        self.startConnection()
        
    def startConnection(self):
        self.irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.irc.settimeout(0.5)
        self.isConnected = False
        logging.info("Bot initialised")
        
    def initialContact(self):
        """
        Handles connecting to the server
        """
        self.irc.connect((self.settings.server,self.settings.port))
        self.messageUser(self.settings.botnick, self.settings.botnick, self.settings.botnick, self.settings.botDescription)
        self.messageNick(self.settings.botnick)
        self.isConnected = True
        logging.info("Bot is connected")
        
    def __message(self,message):
        self.irc.send(message.encode())
        
    def messageUser(self, username, hostname, servername, realname):
        self.__message(" ".join(["USER", username, hostname, servername, realname,"\n"]))
        
    def messageNick(self, username):
        self.__message(" ".join(["NICK", username, "\n"]))
        
    def messageJoin(self, channel):
        self.__message(" ".join(["JOIN", channel, "\n"]))
        logging.info("Joining :"+ channel)
        
    def messagePing(self,response):
        self.__message(" ".join(["PONG", response, "\n"]))
#        logging.debug("PONG :"+ response)
        
    def messagePart(self, channel):
        self.__message(" ".join(["PART", channel,"\n"]))
        logging.info("leaving the channel: "+ channel)
        
    def messageQuit(self,message=""):
        self.__message("".join(["QUIT :", message,"\n"]))
        logging.info("quitting and shutting down: "+ message)
        self.isConnected = False
        
    def messageWhois(self,nick):
        self.__message(" ".join(["WHOIS", nick, "\n"]))
        logging.info("Whois query sent about: " + nick)
        
    def messagePRIVMSG(self,receiver,message):
        
        self.__message(" ".join([
            ":"+self.settings.botnick,
            "PRIVMSG",
            receiver,
            ":"+message,
            "\n"
            ]))
        logging.info("Message: '" + message + "' sent to: '" + receiver + "'")

    def messageNotice(self,receiver,message):
        
        self.__message(" ".join([
            ":"+self.settings.botnick,
            "NOTICE",
            receiver,
            ":"+message,
            "\n"
            ]))
        logging.info("Notice: '" + message + "' sent to: '" + receiver + "'")
    
    def servermsgParser(self, m_dictionary):
        """
        parses servermessages and provides new actions for the queue
        """
        logging.debug("code: %s , value: %s",str(m_dictionary.get("code")),m_dictionary.get("value"))
        if m_dictionary.get("code")==376: #end of /MOTD
            return [{"action":"REACT",
                     "raw":m_dictionary.get("raw"),
                     "type":"JOIN",
                     "value":self.settings.channel
                     }]
        elif m_dictionary.get("code")==353:
            self.currentchannels.append(dictionary.get("value").split()[1])
            #nicks = m_dictionary.get("value").split(":")[1].split()
            #takes the #channel that has just been joined from the /NAMES command
            #adds the channel to the currentchannels list
            
        elif m_dictionary.get("code")==433:
            self.settings.botnick = "_".join([m_dictionary.get("recipient"),str(1)])
            self.messageUser(self.settings.botnick, self.settings.botnick, self.settings.botnick, self.settings.botDescription)
            self.messageNick(self.settings.botnick)
        #433 * PyBeeKaT :Nickname is already in use.
        #403 PyBeeKaT "#KaTaai" :No such channel
        
        #[{"action":"REACT",
        #"raw":m_Message,
        #"type":"SERVER_CODE",
        #"code":code,
        #"recipient":message[1], the person receiving the message
        #"value":message[2] the body of the message
        #}]

    
    def commandParser(self, dictionary):
        """
        parses commandmessages and provides new actions for the queue
        """
        return self.ML.moduleCommand(dictionary)
        #[{"action":"REACT",
        #"raw":m_Message,
        #"type":"PRIVMSG",
        #"subtype":"COMMAND",
        #"sender":message[0],
        #"target":message[2],
        #"messageAction":message[3].split()[0][1:],
        #"message":message[3].split(None,1)
        #}]
    
    
    
    
    
B=Bot()

B.initialContact()
DQ = deque()
textBuffer=""

while B.isConnected:
    try:
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
            #message = messageParser.parse(message=textBufferList[i].strip())
            parsedMessageList = messageParser.messageEvaluator(textBufferList[i].strip(),B.settings.commandCharacter)
            for d in parsedMessageList:
                DQ.append(d)
            i+=1
        
    except socket.timeout:
        sleep(1)
        
    tempDQ=deque()
    for i in range(len(DQ)):
        dictionary = DQ.popleft()
        if dictionary.get("action")=="RELAX":
            logging.debug("message that isn't parsed: %s", dictionary.get("raw"))
            
        elif dictionary.get("action")=="REACT":
            if dictionary.get("type")=="PING":
                B.messagePing(dictionary.get("value"))
#                logging.debug("PING: %s", dictionary.get("value"))
                
            elif dictionary.get("type")=="SERVER_CODE":
                serverMessageList = B.servermsgParser(dictionary)
                if serverMessageList is not None:
                    for d in serverMessageList:
                        tempDQ.append(d)
                        
            elif dictionary.get("type")=="PRIVMSG":
                logging.info("User: %s sent command: %s with message: %s into: %s",dictionary.get("sender"),dictionary.get("messageAction"),dictionary.get("message"),dictionary.get("target"))
                messageCommandList = B.commandParser(dictionary)
                if messageCommandList is not None:
                    for d in messageCommandList:
                        tempDQ.append(d)
                
            elif dictionary.get("type")=="JOIN":
                if dictionary.get("value") not in B.currentchannels:
                    B.messageJoin(dictionary.get("value"))
#                    tempDQ.append({"action":"REMEMBER",
#                         "raw":dictionary.get("raw"),
#                         "type":"JOIN",
#                         "value":dictionary.get("value")
#                         })
                
            elif dictionary.get("type")=="PART":
                if dictionary.get("value") in B.currentchannels:
                    B.currentchannels.remove(dictionary.get("value"))
                    B.messagePart(dictionary.get("value"))
                    logging.info("%s said to leave %s from: %s",dictionary.get("sender"),dictionary.get("value"),dictionary.get("target"))
            
            elif dictionary.get("type")=="QUIT":
                logging.info("%s said to shutdown in %s with message: %s",dictionary.get("sender"),dictionary.get("target"),dictionary.get("value"))
                B.messageQuit(dictionary.get("value"))
                
        elif dictionary.get("action")=="REMEMBER":
            if dictionary.get("type")=="JOIN":
                if dictionary.get("value") in B.currentchannels:
                    pass
                else:

                    joinList = {"action":"REACT",
                                "raw":dictionary.get("raw"),
                                "type":"JOIN",
                                "value":dictionary.get("value")
                                }
                    tempDQ.append(joinList)

        elif dictionary.get("action")=="RESPOND":
            if dictionary.get("type")=="PRIVMSG":
                B.messagePRIVMSG(dictionary.get("target"), dictionary.get("message"))
            elif dictionary.get("type")=="NOTICE":
                B.messageNotice(dictionary.get("target"), dictionary.get("message"))
    DQ = deque(tempDQ)
    tempDQ.clear()
    

