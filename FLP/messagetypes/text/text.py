'''
Created on 13 May 2021

@author: julianporter
'''

from .base import Converter

def decodeASCII(d):
    decoder = lambda d : chr(d) if d>30 and d<128 else '.'
    return ''.join([decoder(c) for c in d])


class String8Converter(Converter):
    
    def __init__(self):
        super().__init__(separator='')
        
    def process(self,d):
        return chr(d) if d>30 and d<128 else '.'

'''
class String16Converter(String8Converter):
    
    def __init__(self):
        super().__init__()
        
        
        
    def __call__(self,data):
        s=super().__call__(data)
        if len(s)>0: return s[0:-1:2]
        return ''
'''    
    
class String16Converter(Converter):
    
    def __init__(self):
        super().__init__()
        
        
        
    def __call__(self,data):
        try:
            return data.decode('utf16')
        except:
            s=decodeASCII(data)
            if len(s)==0 : return ''
            return s[0:-1:2]


    