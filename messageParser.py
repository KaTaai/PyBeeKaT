import re

def parse(message):
    """
    Parses 3 types of messages that the bot received
    """
    messageRegex = re.compile(r"""(PING)\s:(\d+)|  #the Ping message
:([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)!\~?([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)@[\w\.-]+\s([A-Z]+)\s([#@]?[a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|\d-]+)\s?:?(.*)| #evaluates f-ex the MODE message
:[\w\.]+\s(\d{3})\s([a-zA-Z_\\\[\]\{\}\^`|][a-zA-Z_\\\[\]\{\}\^`|]+)\s(.*)    # Parses the messages including the /MOTD
""", re.VERBOSE)
    messageList = messageRegex.findall(message)
    if len(messageList) == 0:
        return messageList
    else:
        return list(filter(None, messageList[0]))