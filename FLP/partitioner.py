'''
Created on 8 May 2021

@author: julianporter
'''

from FLP.chunks import FLPHeader,FLPTrack
from FLP.base import FLPBase

class FLPFile(object):

    def __init__(self,filename):
        with open(filename,mode='rb') as file:
            self.bytes=file.read()
        self.header=None
        self.tracks=[]

    def readHeader(self):
        try:
            if len(self.bytes)<14:
                raise Exception('FLP file requires at least 14 bytes')
            buffer=self.bytes[0:14]
            header=buffer[0:4].decode()
            length=FLPBase.getInt32(buffer[4:8])
            if header=='FLhd' : # header
                if length != 6:
                    raise Exception('Header chunk must have length 6')
                self.header = FLPHeader(buffer[8:])
                return True
            else:
                return False
        except:
            return False

    def parse(self):
        buffer=self.bytes
        while len(buffer)>8:
            header=buffer[0:4].decode()
            length=FLPBase.getInt32(buffer[4:8])
            if header=='FLhd' : # header
                if length != 6:
                    raise Exception(f'Header chunk must have length 6 : got {hex(length)}')

                self.header = FLPHeader(buffer[8:])
                # print(f"Header is {self.header}")

            elif header=='FLdt' : # track
                self.tracks.append(FLPTrack(buffer[8:160]))
            else:
                print(f'Unknown chunk type {header} - skipping')
            buffer = buffer[8+length:]

    def __str__(self):
        out=[]
        if self.header:
            out.append(str(self.header))
        else:
            out.append('No header!')
        for idx, track in enumerate(self):
            out.append(f'\tTrack {idx} of length {len(track)}')
        return '\n'.join(out)

    def __iter__(self):
        return iter(self.tracks)

    def __len__(self):
        return len(self.tracks)

    def __getitem__(self,index):
        return self.tracks[index]

    @property
    def format(self):
        return self.header.format

    @property
    def division(self):
        return self.header.division
