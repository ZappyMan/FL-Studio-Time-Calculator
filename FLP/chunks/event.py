'''
Created on 15 Sep 2019

@author: julianporter
'''

from FLP.base import FLPBase
from FLP.messagetypes import messageType, UnknownMessage 


def printable(c):
    if c>30 and c<128 : return chr(c)
    return '.'

class Event(FLPBase):
    
    def __init__(self,buffer):
        super().__init__(buffer[1:])
        self.header=buffer[0]        
        self.isNumeric=self.header<192
         
        generator = messageType(self.header)
        self.payloadLength = generator.payloadLength()
        try:  
            self.message = generator(self.header)
            self.name = self.message.name
            #print(f'Message and name are {self.message} & {self.name}')
        except:
            self.message = UnknownMessage.Unknown 
            self.name = 'Unknown'
            #print(f'Message and name are {self.message} & {self.name}')
        
        if self.isNumeric:
            self.data=self.getInt(self.payloadLength)
            n=0
        else:
            length, n=self.getVarLengthInt()
            self.data=self.getChunk(length)
            self.payloadLength=length
            
        self.length=self.payloadLength+n+1
        self.code=generator.__name__
        
    def __len__(self):
        return self.length
    
    def value(self):
            return self.message.asString(self.data)
        
        
        
    
    def __str__(self):
        return f'{self.code} {self.header}({self.name}) = {self.value()}'
        
    
        
        
    
