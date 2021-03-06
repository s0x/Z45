'''
Created on 07.01.2012

@author: benjamin
'''

from util.system_message import SystemMessage
from bot.bot import Bot

import config

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
        
        msg._Message_Body = msg._Message_Body + " {" + self._bots[sender] + "}"
        print("msg: " + str(msg))
        for x in self._bots.iterkeys():
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
        self._bots[bot] = protocol
        return bot
    
if __name__ == '__main__':
    puppet_master = PuppetMaster()
    for conf in config.configs:
        puppet_master.create_bot(*conf)
    