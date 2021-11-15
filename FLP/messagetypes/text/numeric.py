'''
Created on 13 May 2021

@author: julianporter
'''

from .base import Converter

class HexConverter(Converter):
    
    def __init__(self):
        super().__init__()
         
    def process(self,d):
        return '{0:0>2X}'.format(d)
    
class IntConverter(Converter):
    
    def __init__(self,size=1):
        super().__init__()
        self.fmt = f'{{0}} ({{0:0>{2*size}X}})'
        
    def process(self,d):
        return self.fmt.format(d)