'''
Created on 24 apr. 2017

@author: Robin Knoet
'''
import unittest
from messageParser import parse


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
        nickMessage = parse(":KaTaai|coding!~KaTaai@ip54529f55.speed.planet.nl NICK :KaTaai|German")
        self.assertListEqual(nickMessage, ['KaTaai|coding', 'NICK', 'KaTaai|German'], "Nick type message was parsed incorrectly")
        
    def testParseNoticeAuthMessage(self):
        authMessage = parse("NOTICE AUTH :*** Looking up your hostname")
        self.assertListEqual(authMessage,["NOTICE AUTH","Looking up your hostname"],"NOTICE AUTH message was parsed incorrectly")
    
    def testParseNoticeMessage(self):
        noticeMessage = parse(":underworld1.no.quakenet.org NOTICE PyBeeKaT :Highest connection count: 2472 (2471 clients)")
        self.assertListEqual(noticeMessage, ["NOTICE","PyBeeKaT","Highest connection count: 2472 (2471 clients)"], "Notice message was parsed incorrectly")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testParsePrivmsg','Test.testParsePingNumeric','Test.testParsePingTextual']
    unittest.main()