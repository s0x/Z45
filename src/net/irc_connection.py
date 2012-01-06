'''
Created on 06.01.2012

@author: Benjamin K.
'''
from net.connection import Connection

class IrcConnection(Connection):
    '''
    classdocs
    '''


    def __init__(self, listener=None):
        '''
        Constructor
        '''
        Connection.__init__(self, listener)
        
    def connect(self, username=None, passwort=None):
        return False
    
    def disconnect(self):
        return False
    
    def send(self):
        return False
        