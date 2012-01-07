'''
Created on 06.01.2012

@author: Benjamin K.
'''
from net.connection import Connection
import socket
import string

HOST="irc.freenode.net"
PORT=6667
CHANNEL="#fh-giessen"

class IrcConnection(Connection):
    '''
    classdocs
    '''


    def __init__(self, listener=None):
        '''
        Constructor
        '''
        Connection.__init__(self, listener)
        self._socket = None
        
    def connect(self, username=None, passwort=None, server=None, channel=None):
        if username == None:
            # TODO: log
            return False
        self._socket = socket.socket()
        self._socket.connect((HOST, PORT))
        self._socket.send("NICK %s\r\n" % username)
        
        self._socket.send("JOIN %s\r\n" % CHANNEL)
        # TODO start thread to handle msgs
        return True
    
    def disconnect(self):
        return False
    
    def send(self):
        return False
        