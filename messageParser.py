import re

def parse(message):
    """
    Parses 3 types of messages that the bot received
    """
    messageRegex = re.compile(r"""
        (PING)\s:(.*)|  #the Ping message
        :([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)![a-zA-Z_\\\[\]\{\}\^`|\d\~-]+@[\w\.-]+\s([A-Z]+)\s([#&]?[a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s?:?(.*)| #evaluates f-ex the MODE message
    :[\w\.]+\s(\d{3})\s?\*?\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)\s(.*)|    # Parses the messages including the /MOTD
    ([A-Z]+)\s:([\w\s]+):\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)?\s.*\s[\w\.]+\s(.*)| #rudimentary parse of error messages
    :([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)!~?.*@[\w\.]+\s([A-Z]+)\s:(.*)|
    ([A-Z]+\s[A-Z]+)\s:[\*]{3}\s(.*)|  #NOTICE AUTH messages
    :[\w\.]+\s([A-Z]+)\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s:(.*) #NOTICE messages
    """, re.VERBOSE)
    messageList = messageRegex.findall(message)
    if len(messageList) == 0:
        return messageList
    else:
        return list(filter(None, messageList[0]))

def messageEvaluator(m_Message,commandChar):
    message = parse(m_Message)
    if len(message)==0:
        return [{"action":"RELAX",
                 "raw":m_Message
                 }]
        
    elif message[0] == "PING":
        return [{"action":"REACT",
                 "raw":m_Message,
                 "type":"PING",
                 "value":message[1]
                 }]
        
    else:
        try:
            code = int(message[0])
            return [{"action":"REACT",
             "raw":m_Message,
             "type":"SERVER_CODE",
             "code":code,
             "recipient":message[1],
             "value":message[2]
             }]
            
        except ValueError:
            if message[1] == 'PRIVMSG':
                if message[3].startswith(commandChar):
                    if len(message[3].split(None,1))>1:
                        dictMessage = message[3].split(None,1)[1]
                    else:
                        dictMessage = ""
                    return [{"action":"REACT",
                             "raw":m_Message,
                             "type":"PRIVMSG",
                             "subtype":"COMMAND",
                             "sender":message[0],
                             "target":message[2],
                             "messageAction":message[3].split()[0][1:],
                             "message": dictMessage
                             }]
                    
            elif message[1] == 'PART':
                if len(message)<4:
                    partMessage = ""
                else:
                    partMessage = message[3]
                return [{"action":"REACT",
                         "raw":m_Message,
                         "type":"PART",
                         "sender":message[0],
                         "target":message[2],
                         "message":partMessage
                         }]
                
            elif message[1] == "NOTICE":
                return [{"action":"RELAX",
                         "raw":m_Message
                         }]
            
            elif message[1] == "NICK":
                return [{"action":"REACT",
                         "raw":m_Message,
                         "type":"NICK",
                         "sender":message[0],
                         "message":message[2]
                         }]
            
            elif message[1] == "MODE":
                return [{"action":"REACT",
                         "raw":m_Message,
                         "type":"MODE",
                         "sender":message[0],
                         "target":message[2],
                         "message":message[3]
                         }]
                
            else:
                return [{"action":"RELAX",
                 "raw":m_Message}]
    return [{"action":"RELAX",
             "raw":m_Message}]

