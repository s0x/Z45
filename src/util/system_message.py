'''
Created on 07.01.2012

@author: Marcel M.
'''
from util.message import Message

class SystemMessage(Message):
    
    def __init__(self, target, body):
        Message.__init__(self, None, target, body)
    
    def __str__ (self):
        rep = self._Target +" | "+ self._Message_Body
        return rep