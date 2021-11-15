'''
Created on 13 May 2021

@author: julianporter
'''


class Converter(object):
    
    def __init__(self,separator=' '):
        self.separator=separator
        
    def __call__(self,data : bytes) -> str:
        try:
            return self.separator.join([self.process(d) for d in data]) 
        except:
            return self.process(data)
    
    def process(self,d : int) -> str:
        return str(d)