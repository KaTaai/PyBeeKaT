'''
Created on 24 apr. 2017

@author: Robin Knoet
'''
import unittest
from messageParser import parse, messageEvaluator


class Test(unittest.TestCase):


    def testParsePrivmsg(self):
        parsedMessage = parse(":Clayres!~Clayres@ip-80-226-0-6.vodafone-net.de PRIVMSG #ssss :Yay?")
        self.assertListEqual(parsedMessage, ['Clayres', 'PRIVMSG', '#ssss', 'Yay?'], "The Privmsg was parsed incorrect")

    def testParsePingNumeric(self):
        PingMessage = parse("PING :175826047")
        self.assertListEqual(PingMessage, ["PING","175826047"], "The numeric ping was parsed incorrectly")
        
    def testParsePingTextual(self):
        PingMessage = parse("PING :underworld1.no.quakenet.org")
        self.assertListEqual(PingMessage, ["PING","underworld1.no.quakenet.org"], "The textual ping was parsed incorrectly")
        
    def testParseCodedMessage(self):
        codeMessage = parse(":portlane.se.quakenet.org 376 PyBeeKaT :End of /MOTD command.")
        self.assertListEqual(codeMessage, ['376', 'PyBeeKaT', ':End of /MOTD command.'], "Message with code was parsed incorrectly")
        
    def testParseNickMessage(self):
        messageNick = parse(":KaTaai|coding!~KaTaai@ip54529f55.speed.planet.nl NICK :KaTaai|German")
        self.assertListEqual(messageNick, ['KaTaai|coding', 'NICK', 'KaTaai|German'], "Nick type message was parsed incorrectly")
        
    def testParseNoticeAuthMessage(self):
        authMessage = parse("NOTICE AUTH :*** Looking up your hostname")
        self.assertListEqual(authMessage,["NOTICE AUTH","Looking up your hostname"],"NOTICE AUTH message was parsed incorrectly")
    
    def testParseNoticeMessage(self):
        noticeMessage = parse(":underworld1.no.quakenet.org NOTICE PyBeeKaT :Highest connection count: 2472 (2471 clients)")
        self.assertListEqual(noticeMessage, ["NOTICE","PyBeeKaT","Highest connection count: 2472 (2471 clients)"], "Notice message was parsed incorrectly")
        
    def testParsePartMessage(self):
        partMessage = parse(":KaTaai|coding!~KaTaai@KaTaai.users.quakenet.org PART #KaTaai :Leaving")
        self.assertListEqual(partMessage, ['KaTaai|coding','PART','#KaTaai','Leaving'], "Partmessage is parsed incorrectly")
    
    def testEvaluatePing(self):
        PingMessage = messageEvaluator("PING :175826047", "|")
        self.assertListEqual(PingMessage,
                             [{"action":"REACT",
                               "raw":"PING :175826047",
                               "type":"PING",
                               "value":"175826047"}]
                             , "The returned Pingmessage is incorrect")
    def testEvaluateCodedMessage(self):
        codedMessage = messageEvaluator(":portlane.se.quakenet.org 376 PyBeeKaT :End of /MOTD command.", "|")
        self.assertListEqual(codedMessage,
                             [{"action":"REACT",
                               "raw":":portlane.se.quakenet.org 376 PyBeeKaT :End of /MOTD command.",
                               "type":"SERVER_CODE",
                               "code":376,
                               "recipient":"PyBeeKaT",
                               "value":":End of /MOTD command."}]
                             , "Coded message isn't parsed correctly")
        
    def testEvaluatePrivmsgCommand(self):
        Privmsg = messageEvaluator(":Clayres!~Clayres@ip-80-226-0-6.vodafone-net.de PRIVMSG #ssss :|Join #KaTaai", "|")
        self.assertListEqual(Privmsg,
                             [{"action":"REACT",
                               "raw":":Clayres!~Clayres@ip-80-226-0-6.vodafone-net.de PRIVMSG #ssss :|Join #KaTaai",
                               "type":"PRIVMSG",
                               "subtype":"COMMAND",
                               "sender":"Clayres",
                               "target":"#ssss",
                               "messageAction":"Join",
                               "message":"#KaTaai"}]
                             , "The command privmsg is parsed incorrectly")
        
        pass
    
    def testEvaluatePrivmsgNonCommand(self):
        pass
    
    def testEvaluateNickMessage(self):
        nickMessage = messageEvaluator(":KaTaai|coding!~KaTaai@ip54529f55.speed.planet.nl NICK :KaTaai|German", "|")
        self.assertListEqual(nickMessage,
                             [{"action":"REACT",
                               "raw":":KaTaai|coding!~KaTaai@ip54529f55.speed.planet.nl NICK :KaTaai|German",
                               "type":"NICK",
                               "sender":"KaTaai|coding",
                               "message":"KaTaai|German"}]
                             , "NickMessage isn't parsed correctly")
    def testEvaluateNoticeAuth(self):
        pass
    
    def testEvaluateNoticeMessage(self):
        pass
    
    def testEvaluatePartMessage(self):
        PartMessage = messageEvaluator(":KaTaai|coding!~KaTaai@KaTaai.users.quakenet.org PART #KaTaai :Leaving", "|")
        self.assertListEqual(PartMessage,
                             [{"action":"REACT",
                               "raw":":KaTaai|coding!~KaTaai@KaTaai.users.quakenet.org PART #KaTaai :Leaving",
                               "type":"PART",
                               "sender":"KaTaai|coding",
                               "target":"#KaTaai",
                               "message":"Leaving"}]
                             ,"The partmessage isn't evaluated correctly")
    
    def testEvaluateModeMessage(self):
        modeMessage = messageEvaluator(":PyBeeKaT!~PyBeeKaT@ip54529f55.speed.planet.nl MODE PyBeeKaT +i", "|")
        self.assertListEqual(modeMessage, [{"action":"REACT",
                                            "raw":":PyBeeKaT!~PyBeeKaT@ip54529f55.speed.planet.nl MODE PyBeeKaT +i",
                                            "type":"MODE",
                                            "sender":"PyBeeKaT",
                                            "target":"PyBeeKaT",
                                            "message":"+i"
                                            }], "Modemessage isn't parsed correctly.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testParsePrivmsg','Test.testParsePingNumeric','Test.testParsePingTextual']
    unittest.main()