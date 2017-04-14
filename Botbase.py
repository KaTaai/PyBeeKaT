import socket

import Config,messageParser

class Bot(object):
    
    def __init__(self):
        self.settings = Config.Config("config.ini")
        self.irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.isConnected = False
        
    def initialContact(self):
        self.irc.connect((self.settings.server,self.settings.port))
        self.userMessage(self.settings.botnick, self.settings.botnick, self.settings.botnick, self.settings.botDescription)
        self.nickMessage(self.settings.botnick)
        self.isConnected = True
        
    def userMessage(self, username, hostname, servername, realname):
        self.irc.send(" ".join(["USER", username, hostname, servername, realname,"\n"]).encode())
        
    def nickMessage(self, username):
        self.irc.send(" ".join(["NICK", username, "\n"]).encode())
        
    def joinMessage(self, channel):
        self.irc.send(" ".join(["JOIN", channel, "\n"]).encode())
        print("Joining :"+ channel)
        
    def pingMessage(self,response):
        self.irc.send(" ".join(["PONG", response, "\n"]).encode())
        print("PONG :"+ response)
        
    def quitMessage(self,message=""):
        self.irc.send(" ".join(["QUIT", message,"\n"]).encode())
        print("quitting and shutting down")
        self.isConnected = False
    
B=Bot()

B.initialContact()
textBuffer=""
while B.isConnected:
    text=B.irc.recv(2040)
    message = messageParser.parse(message=text.decode())
    
    if len(message)==0:
        print(text)
        print(message)
    elif message[0] == "PING":
        B.pingMessage(message[1])
    elif 'End of /MOTD command.' in message[2]:
        B.joinMessage(B.settings.channel)
    elif message[2] == 'PRIVMSG':
        privmsg = message[3].split(" :")
        if privmsg[1][0] == B.settings.commandCharacter:
            commandsep = privmsg[1][1:].split(" ",1)
            if commandsep[0].lower()=="join":
                if len(commandsep) == 2:
                    B.joinMessage(commandsep[1].strip())
            elif commandsep[0].lower() == "quit":
                if len(commandsep) == 1:
                    B.quitMessage()
                else:
                    B.quitMessage(commandsep[1].strip())
    else:
        print(text)#.decode().strip())
        print(message)
    
    
        