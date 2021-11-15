'''
Created on 9 May 2021

@author: julianporter
'''
from .core import BaseMessage
from .text import DWORDConv

class DWORD(BaseMessage):
    Color        =128
    PlayListItem   =129          # +Pos (word) +PatNum (word)
    Echo         =130
    FXSine       =131
    CutCutBy     =132
    WindowH      =133
    # 134 does not exist
    MiddleNote    =135
    Reserved      =136            # may contain an invalid version info
    MainResoCutOff    =137
    DelayReso    =138
    Reverb       =139
    StretchTime    =140
    SSNote       =141                      
    FineTune     =142
    SampleFlags    =143
    LayerFlags        =144
    ChanFilterNum    =145
    CurrentFilterNum    =146
    FXOutChanNum    =147     # FX track output channel
    NewTimeMarker    =148    # + Time & Mode in higher bits
    FXColor          =149
    PatColor         =150
    PatAutoMode    =151      # obsolete
    SongLoopPos    =152
    AUSmpRate    =153
    FXInChanNum    =154      # FX track input channel
    PluginIcon        =155
    FineTempo        =156

    @classmethod
    def allObsolete(cls):
        return [DWORD.PlayListItem,
                DWORD.MainResoCutOff,
                DWORD.SSNote,
                DWORD.PatAutoMode] 

    @classmethod
    def payloadLength(cls):
        return 4
    
    def getConverter(self):
        return DWORDConv
    