'''
Created on 8 May 2021

@author: julianporter
'''
from FLP.base import FLPBase

class FLPChunk(FLPBase):
    
    def __init__(self,data=b''):
        super().__init__()
        self.data=data
        self.code=''
        
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        return self.stringify(self.data)
