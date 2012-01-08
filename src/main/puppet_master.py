'''
Created on 07.01.2012

@author: benjamin
'''

from util.system_message import SystemMessage
from bot.bot import Bot
import string

class PuppetMaster(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        bots = {"<protokol>:<name>" : <bot>}
        '''
        self._bots = {}
        
    def receive(self, sender, msg):
        if isinstance(msg, SystemMessage):
            return
        print("msg: " + str(msg))
        for x in self._bots.itervalues():
            if sender != x:
                x.send(msg)
        """source_protokol = msg.get_source()
        source_protokol = string.split(source_protokol, ":")[0]
        if source_protokol == "IRC":
            if "XMPP:Master" in self._bots.keys():
                target_bot = self._bots["XMPP:Master"]
            else:
                target_bot = self.create_bot("XMPP", "Master")
            target_bot.send(msg)
        else:
            if "IRC:Master" in self._bots.keys():
                target_bot = self._bots["IRC:Master"]
            else:
                target_bot = self.create_bot("IRC", "Master")
            target_bot.send(msg)
    """
    def create_bot(self, protocol, username, password, server, port, channel):
        bot = Bot()
        bot.callback(self.receive)
        bot.new_connection(protocol, username=username, password=password, server=server, port=port, channel=channel)
        self._bots[protocol+":"+channel] = bot
        return bot
    
if __name__ == '__main__':
    puppet_master = PuppetMaster()
    puppet_master.create_bot("IRC", username="z45", password=None, server="irc.freenode.net", port="6667", channel="#fh-giessen")
    puppet_master.create_bot("XMPP", "user@example.com", "password", "conference.jabber.ccc.de", "5222", "thm")
    