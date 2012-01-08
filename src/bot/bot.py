'''
Created on 07.01.2012

@author: Marcel M.
'''

from net.irc_connection import IrcConnection
from net.xmpp_connection import XmppConnection

import config

class Bot (object):
    def __init__ (self):
        self._connection = None
        self._function = None
    
    def new_connection (self, protocol, username, password, server, port=None, channel=None):
        if protocol == "IRC":            
#<<<<<<< HEAD
#            self._connection = IrcConnection(self.listen)
#            self._connection.connect(username=config.IRC_NAME+"_"+name, server=config.IRC_SERVER+":"+str(config.IRC_PORT), channel=config.IRC_CHANNEL)
#        if protocol == "XMPP":
#            self._connection = XmppConnection(self.listen)
#            self._connection.connect(username=config.XMPP_NAME, password=config.XMPP_PASSWORD, channel=config.XMPP_CHANNEL)
#=======
            self._connection = IrcConnection(username=username, password=password, server=server, channel=channel, listener=self.listen)
            self._connection.connect()
        if protocol == "XMPP":
            self._connection = XmppConnection(username=username, password=password,
                                              server="conference.jabber.ccc.de", channel="thm", listener=self.listen)
            self._connection.connect()
#>>>>>>> 9181cf3aa7585579e34c30e22683cf1beaf64c0e
    
    def listen (self, msg):
        if self._function != None:
            self._function(self, msg)
            return True
        return False
    
    def send (self, msg):
        if self._connection != None:
            return self._connection.send(msg)
        return False
    
    def callback (self, function):
        self._function = function
        return True