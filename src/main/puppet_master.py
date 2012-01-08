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
        
    def receive(self, msg):
        if isinstance(msg, SystemMessage):
            return
        print("msg: " + str(msg))
        source_protokol = msg.get_source()
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
    
    def create_bot(self, protocol, name):
        bot = Bot()
        bot.callback(self.receive)
        bot.new_connection(protocol, name)
        self._bots[protocol+":"+name] = bot
        return bot
    
if __name__ == '__main__':
    puppet_master = PuppetMaster()
    puppet_master.create_bot("IRC", "Master")
    puppet_master.create_bot("XMPP", "Master")
    