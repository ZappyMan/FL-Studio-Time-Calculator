'''
Created on 9 May 2021

@author: julianporter
'''

from enum import Enum
from .text import STR8Conv,SAFEConv   

    

class BaseMessage(Enum):
    
    @classmethod
    def all(cls):
        return list(cls.__members__.values())
    
    @classmethod
    def names(cls):
        return list(cls.__members__.keys())
    
    @classmethod
    def byName(cls,name):
        return cls.__members__[name]
    
    @classmethod
    def payloadLength(cls):
        return None
    
    
    @classmethod
    def allObsolete(cls):
        return []
    
    def isObsolete(self):
        return self in self.allObsolete()
 
    def getConverter(self):
        return STR8Conv
    
    def asString(self,value):
        converter = self.getConverter()
        return converter(value)
    

class UnknownMessage(BaseMessage):
    
    Unknown = 0
    
    def getConverter(self):
        return SAFEConv
    
    
    



    

