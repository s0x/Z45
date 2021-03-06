'''
Created on 06.01.2012

@author: Benjamin K.
'''
from net.connection import Connection
from util.message import Message
from util.private_message import PrivateMessage
from util.system_message import SystemMessage

import logging

from threading import Thread
import socket
import string

HOST="irc.freenode.net"
PORT=6667
CHANNEL="#fh-giessen"

class IrcConnection(Connection):
    '''
    Connection to an IRC server.
    '''


    def __init__(self, username, password, server, port=6667, channel=None, listener=None):
        '''
        Contructor
        listener should handle a Message
        '''
        Connection.__init__(self, username, password, server, port, channel, listener)
        self._socket = None
        self._receiver = None
        
    def connect(self):
        '''
        Connects to the defined server.
        Only the username is needed.
        '''
        if self._username == None:
            logging.info("An IRC connection without a username is not possible.")
            return False
        self._socket = socket.socket()
        self._socket.connect((self._server, self._port))
        self._socket.send("NICK %s\r\n" % self._username)
        self._socket.send("USER %s %s bla :%s\r\n" % (self._username, self._server, self._username))
        
        self._socket.send("JOIN %s\r\n" % self._channel)
        
        self._receiver = Receiver(self._listener, self._socket, self._username, self._channel)
        self._receiver.start()
        logging.debug("IRC connection established.")
        return True
    
    def disconnect(self):
        '''
        Disconnects from the server.
        '''
        self._socket.send("QUIT :%s\r\n"  % ("divided by zero"))
        if self._receiver != None:
            self._receiver.stop_listening()
        self._socket.close()
        logging.debug("IRC connection closed.")
        return True
    
    def send(self, msg):
        '''
        Sends a message to the server.
        msg has to be a Message, PrivateMessage or SystemMessage.
        '''
        if isinstance(msg, SystemMessage):
            self._socket.send("PRIVMSG %s :%s\r\n" % (self._channel, msg.get_body()))
        elif isinstance(msg, PrivateMessage):
            self._socket.send("PRIVMSG %s :%s\r\n" % (msg.get_target(), msg.get_source() +": "+ msg.get_body()))
        else:
            self._socket.send("PRIVMSG %s :%s\r\n" % (self._channel, msg.get_source() +": "+ msg.get_body()))
        return True
    
class Receiver(Thread):
    '''
    Thread which manages new messages by the server.
    '''
    
    def __init__(self, function, socket, name, channel):
        '''
        Constructor
        function should be able to handle a Message.
        socket should be the socket of the connection.
        '''
        Thread.__init__(self)
        self._running = True
        self._function = function
        self._socket = socket
        self._name = name
        self._channel = channel
        
    def stop_listening(self):
        '''
        Stops the thread.
        '''
        self._running = False
        
    def run(self):
        '''
        Run method which reads all messages received by the server.
        '''
        readbuffer = ""
        while self._running:
            readbuffer=readbuffer+self._socket.recv(1024)
            temp=string.split(readbuffer, "\n")
            readbuffer=temp.pop()
        
            for line in temp:
                self._parse_msg(line)
                line=string.rstrip(line)
                line=string.split(line)
        
                if(line[0]=="PING"):
                    self._socket.send("PONG %s\r\n" % line[1])
                    
    def _parse_msg(self, msg):
        '''
        Parses a message, makes a protocol independent message and sends
        it to the callback function.
        '''
        if len(msg) == 0:
            logging.debug("IRC listener received empty message.")
        source = string.split(msg, "!")[0]
        if len(source) > 1:
            source = source[1:]
        if source == self._name:
            return
        parts = string.split(msg, " ")
        operation = None
        content = string.split(msg, ":")
        if len(content) > 2:
            content = string.join(content[2:], ":")
        else:
            content = ""
        content = string.strip(content)
        if len(parts) > 1:
            operation = parts[1]
        if operation == None:
            return
        elif operation == "PRIVMSG":
            if len(parts) < 3:
                return
            elif parts[2] == self._channel:
                message = Message(source, self._channel, content)
                self._function(message)
            else:
                message = PrivateMessage(source, parts[2], content)
                self._function(message)
        else:
            message = SystemMessage("SYSTEM", self._channel, content)
            self._function(message)
