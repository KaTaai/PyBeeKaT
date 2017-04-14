import re

def parse(message):
    messageRegex = re.compile(r"""(PING)\s:(\d+)|  #the Ping message
:([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)!\~([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)@[\w\.]+\s([A-Z]+)\s(.*)| #evaluates f-ex the MODE message
:[\w\.]+\s(\d{3})\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)\s(.*)""", re.VERBOSE)
    messageList = messageRegex.findall(message)
    if len(messageList) == 0:
        return messageList
    else:
        return list(filter(None, messageList[0]))