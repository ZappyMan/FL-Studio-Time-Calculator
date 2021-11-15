from .core import BaseMessage,UnknownMessage
from .int8messages import BYTE
from .int16messages import WORD
from .int32messages import DWORD
from .textmessages import VAR 

MessageTypes = [BYTE,WORD,DWORD,VAR]
PayloadLengths = [1,2,4,-1]

from FLP.base import FLPParserError

def payloadLength(idx):
    try:
        return PayloadLengths[idx//64]
    except:
        raise FLPParserError(f'Received bad event index {idx}')

def messageType(idx):
    try:
        return MessageTypes[idx//64]
    except:
        raise FLPParserError(f'Received bad event index {idx}')  
    
def isNumeric(idx):
    return payloadLength(idx)>0

def isText(idx):
    return payloadLength(idx)<0