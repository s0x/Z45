'''
Created on 07.01.2012

@author: Marcel M.
'''
from util.message import Message

class SystemMessage(Message):
    
    def __init__(self, source, target, body):
        Message.__init__(self, source, target, body)