'''
Created on 06.01.2012

@author: Benjamin K.
'''

class Connection(object):
    '''
    A abstract connection to a chat protocol.
    '''


    def __init__(self, username, password, server, port=None, channel=None, listener=None):
        '''
        Constructor
        The message listener of this connection could be set.
        '''
        self._username = username
        self._password = password
        self._server = server
        self._port = port
        self._channel = channel
        self._listener = listener
    
    def send(self, msg):
        '''
        Abstract method for sending a message in the protocol.
        '''
        return False
    
    def register_msg_listener(self, listener):
        '''
        Sets the message listener of this connection.
        '''
        self._listener = listener
        return True
        
    def notify_msg_listener(self, msg):
        '''
        Calls the message listener with the new message.
        '''
        if self._listener != None:
            try: 
                self._listener(msg)
                return True
            except TypeError:
                # TODO log_e "Connection: listener with wrong signature"
                self._listener = None
                return False
        
    def connect(self):
        '''
        Abstract method to connect to the chat protocol.
        '''
        return False
    
    def disconnect(self):
        '''
        Abstract method to disconnect.
        '''
        return False
    