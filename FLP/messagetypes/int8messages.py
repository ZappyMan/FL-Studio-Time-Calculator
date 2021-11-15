from .core import BaseMessage 
from .text import BYTEConv

class BYTE(BaseMessage):
    
    ChannelEnabled = 0
    NoteOn = 1
    ChannelVolume = 2
    ChannelPan = 3
    MIDIChannel = 4
    MIDINote = 5
    MIDIPatch = 6
    MIDIBank = 7
    # 8 does not exist
    LoopActive = 9
    ShowInfo = 10
    Shuffle = 11
    MainVolume = 12
    FitToSteps = 13
    Pitchable = 14
    Zipped = 15
    DelayFlags = 16
    Numerator = 17
    Denominator = 18
    UseLoopPoints = 19
    LoopType = 20
    ChannelType = 21
    TargetFXTrack = 22
    PanVolumeTab = 23
    NStepsShown = 24
    SSLength = 25
    SSLoop = 26
    FXProps = 27
    Registered = 28
    APDC = 29
    TruncateClipNotes = 30
    EEAutoMode = 31
    
    @classmethod
    def allObsolete(cls):
        return [BYTE.ChannelVolume,
                BYTE.ChannelPan,
                BYTE.MainVolume,
                BYTE.FitToSteps,
                BYTE.Pitchable,
                BYTE.DelayFlags,
                BYTE.NStepsShown]
    
    @classmethod
    def payloadLength(cls):
        return 1
    
    def getConverter(self):
        return BYTEConv
    
