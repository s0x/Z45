'''
Created on 07.01.2012

@author: Marcel M.
'''
class Message (object):
    def __init__(self, message_type, recipient, message_body):
        self._Message_Type = message_type
        self._Recipient = recipient
        self._Message_Body = message_body
        
    def get_type (self):
        return self._Message_Type
    def get_recipient (self):
        return self._Recipient
    def get_body (self):
        return self._Message_Body
    def __str__ (self):
        rep = self._Message_Type +" | "+ self._Recipient +" | "+ self._Message_Body
        return rep