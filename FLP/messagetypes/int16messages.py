'''
Created on 9 May 2021

@author: julianporter
'''
from .core import BaseMessage
from .text import WORDConv 


  
 

class WORD(BaseMessage):
    
    NewChan      =64
    NewPat       =64+1      
    Tempo        =64+2
    CurrentPatNum    =64+3
    PatData      =64+4
    FX           =64+5
    Fade_Stereo    =64+6
    CutOff       =64+7
    DotVol       =64+8
    DotPan       =64+9
    PreAmp       =64+10
    Decay        =64+11
    Attack       =64+12
    DotNote      =64+13
    DotPitch     =64+14
    DotMix       =64+15
    MainPitch    =64+16
    RandChan     =64+17
    MixChan      =64+18
    Resonance    =64+19
    OldSongLoopPos      =64+20
    StDel        =64+21
    FX3          =64+22
    DotReso      =64+23
    DotCutOff    =64+24
    ShiftDelay    =64+25
    LoopEndBar    =64+26
    Dot          =64+27
    DotShift     =64+28
    TempoFine    =64+29
    LayerChan   =64+30
    FXIcon       =64+31
    DotRel       =63+32
    SwingMix     =63+33
    
    @classmethod
    def allObsolete(cls):
        return [WORD.Tempo,
                WORD.RandChan,
                WORD.MixChan,
                WORD.OldSongLoopPos,
                WORD.TempoFine]
    
    @classmethod
    def payloadLength(cls):
        return 2
    
    def getConverter(self):
        return WORDConv