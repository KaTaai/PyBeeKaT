import re

def parse(message):
    """
    Parses 3 types of messages that the bot received
    """
    matchdict = {}
    regexdict = {
        1:r"(PING)\s:(.*)",  #the Ping message
        2:r":([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)![a-zA-Z_\\\[\]\{\}\^`|\d\~-]+@[\w\.-]+\s([A-Z]+)\s([#&]?[a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s?:?(.*)", #evaluates f-ex the MODE message
        3:r":[\w\.]+\s(\d{3})\s?\*?\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)\s(.*)",    # Parses the messages including the /MOTD
        4:r"([A-Z]+)\s:([\w\s]+):\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)?\s.*\s[\w\.]+\s(.*)", #rudimentary parse of error messages
        5:r":([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)!~?.*@[\w\.]+\s([A-Z]+)\s:(.*)",
        6:r"([A-Z]+\s[A-Z]+)\s:[\*]{3}\s(.*)",  #NOTICE AUTH messages
        7:r":[\w\.]+\s([A-Z]+)\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s:(.*)" #NOTICE messages
    }
    for key, value in regexdict.items():
        remsg = re.match(value,message)
        if remsg is not None:
            matchdict[key] = remsg.groups()

    #print(matchdict)
    # messageRegex = re.compile(r"""
    #     (PING)\s:(.*)|  #the Ping message
    #     :([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)![a-zA-Z_\\\[\]\{\}\^`|\d\~-]+@[\w\.-]+\s([A-Z]+)\s([#&]?[a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s?:?(.*)| #evaluates f-ex the MODE message
    # :[\w\.]+\s(\d{3})\s?\*?\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)\s(.*)|    # Parses the messages including the /MOTD
    # ([A-Z]+)\s:([\w\s]+):\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)?\s.*\s[\w\.]+\s(.*)| #rudimentary parse of error messages
    # :([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)!~?.*@[\w\.]+\s([A-Z]+)\s:(.*)|
    # ([A-Z]+\s[A-Z]+)\s:[\*]{3}\s(.*)|  #NOTICE AUTH messages
    # :[\w\.]+\s([A-Z]+)\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s:(.*) #NOTICE messages
    # """, re.VERBOSE)
    # messageList = messageRegex.findall(message)
    # if len(messageList) == 0:
    #     return messageList
    # else:
    #     return list(filter(None, messageList[0]))
    return matchdict

def messageEvaluator(m_Message,commandChar):
    message = parse(m_Message)
    print(message)
    if len(message)==0:
        return [{"action":"RELAX",
                 "raw":m_Message
                 }]
        
    elif 1 in message:
        return [{"action":"REACT",
                 "raw":m_Message,
                 "type":"PING",
                 "value":message[1][1]
                 }]

    elif 2 in message:
        if message[2][1] == 'PRIVMSG':
            if message[2][3].startswith(commandChar):
                if len(message[2][3].split(None,1))>1:
                    dictMessage = message[2][3].split(None,1)[1]
                else:
                    dictMessage = ""
                return [{"action":"REACT",
                         "raw":m_Message,
                         "type":"PRIVMSG",
                         "subtype":"COMMAND",
                         "sender":message[2][0],
                         "target":message[2][2],
                         "messageAction":message[2][3].split()[0][1:],
                         "message": dictMessage
                     }]
            else:
                return [{"action":"RELAX",
                 "raw":m_Message
                 }]


                
        elif message[2][1] == 'PART':
            if len(message[2])<4:
                partMessage = ""
            else:
                partMessage = message[2][3]
            return [{"action":"REACT",
                     "raw":m_Message,
                     "type":"PART",
                     "sender":message[2][0],
                     "target":message[2][2],
                     "message":partMessage
                     }]
            
        elif message[2][1] == "NOTICE":
            return [{"action":"RELAX",
                     "raw":m_Message
                     }]
        
        elif message[2][1] == "NICK":
            return [{"action":"REACT",
                     "raw":m_Message,
                     "type":"NICK",
                     "sender":message[2][0],
                     "message":message[2][2]
                     }]
        
        elif message[2][1] == "MODE":
            return [{"action":"REACT",
                     "raw":m_Message,
                     "type":"MODE",
                     "sender":message[2][0],
                     "target":message[2][2],
                     "message":message[2][3]
                     }]
            
        else:
            return [{"action":"RELAX",
             "raw":m_Message}]

    elif 3 in message:
        code = int(message[3][0])
        return [{"action":"REACT",
         "raw":m_Message,
         "type":"SERVER_CODE",
         "code":code,
         "recipient":message[3][1],
         "value":message[3][2]
         }]

    else:
        return [{"action":"RELAX",
             "raw":m_Message}]
