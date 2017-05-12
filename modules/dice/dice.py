import random
import re

from modules.module.module import Module

class Dice(Module):
    
    def __init__(self,seed = None, moduleCommand = "", helpText = "", helpIsPublic = None, commandIsPublic = None):
        """check for help and return it or return the dice values requested"""
        super().__init__(moduleCommand, helpText, helpIsPublic, commandIsPublic)
        self.rnd = random.Random()
        self.rnd.seed(seed)

    
    def uniform(self, a, b):
        return self.rnd.uniform(a,b)

    
    def uniformInt(self, a, b):
        return self.rnd.randint(a, b)
    
    def getResult(self,message):
        messageRegex = re.compile(r"""
        (\d*)(d)(\d*)| #dice notation f-ex 1d6
        (int)\s(\d*)\s(\d*) #integer between the first and 2nd integer
        (unif)\s(\d*)\s(\d*) #uniform value between the first and second integer
    """, re.VERBOSE)
        messageList = messageRegex.findall(message)
        if len(messageList) == 0:
            return {"result":"Message: '" + message + "' does not contain a valid string. Try the help for more information.",
                    "isPublic":self.__COMMANDISPUBLIC,
                    "command":self.moduleCommand}
        else:
            l = list(filter(None, messageList[0]))
            if len(l)==3:
                if l[1] == "d":
                    diceVals = 0
                    for i in range(int(l[0])):
                        diceVals += self.uniformInt(1,int(l[2]))
                    return {"result":message + " is: " +str(diceVals),
                    "isPublic":self.isPublicCommand,
                    "command":self.moduleCommand}
                elif l[0] == "int":
                    pass #integer
                elif l[0] == "unif":
                    pass #uniform
                else:
                    return {"result":"Message: '" + message + "' does not contain a valid string. Try the help for more information.",
                    "isPublic":self.__COMMANDISPUBLIC,
                    "command":self.moduleCommand}
            else:
                return {"result":"Message: '" + message + "' does not contain a valid string. Try the help for more information.",
                    "isPublic":self.__COMMANDISPUBLIC,
                    "command":self.moduleCommand}