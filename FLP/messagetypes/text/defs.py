'''
Created on 17 May 2021

@author: julianporter
'''

from .numeric import HexConverter,IntConverter 
from .text import String8Converter,String16Converter


   

HEXConv = HexConverter()
BYTEConv = IntConverter(1)
WORDConv = IntConverter(2)
DWORDConv = IntConverter(4)
STR8Conv = String8Converter()
STR16Conv = String16Converter()

def SAFEConv(value):
    try:
        if len(value)>1: return STR8Conv(value)
        return BYTEConv(value[0])
    except:
        return f'{value}'
