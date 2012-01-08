'''
Created on 07.01.2012

@author: Marcel M.
'''

from net.irc_connection import IrcConnection
from net.xmpp_connection import XmppConnection

class Bot (object):
    def __init__ (self):
        self._connection = None
        self._function = None
    
    def new_connection (self, protocol, name):
        if protocol == "IRC":
            self._connection = IrcConnection(self.listen)
            self._connection.connect(username="Z45_"+name)
        if protocol == "XMPP":
            self._connection = XmppConnection(self.listen)
            self._connection.connect(username="Z45@becauseimaweso.me", password="12345", channel="thm@conference.jabber.ccc.de")
    
    def listen (self, msg):
        if self._function != None:
            self._function(msg)
            return True
        return False
    
    def send (self, msg):
        if self._connection != None:
            return self._connection.send(msg)
        return False
    
    def callback (self, function):
        self._function = function
        return True