'''
Created on 07.01.2012

@author: Marcel M.
'''
class Message (object):
    
    def __init__(self, source, target, message_body):
        self._Source = source
        self._Target = target
        self._Message_Body = message_body
          
    def get_source (self):
        return self._Source
    
    def get_target (self):
        return self._Target
    
    def get_body (self):
        return self._Message_Body
    
    def __str__ (self):
        rep = self._Source +" | "+ self._Target +" | "+ self._Message_Body
        return rep