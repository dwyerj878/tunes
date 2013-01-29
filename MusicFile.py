#!/usr/bin/python

#
# Music file
#
class MusicFile():
    
    pitch=0
    tempo=0
    volume=100

    def __init__(self, name,  path):
        self.name = name
        self.path = path

