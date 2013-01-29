#!/usr/bin/python

import os
import dbm
import pickle
import shelve
import sys

from MusicFile import MusicFile

from PyQt4 import QtCore, QtGui
import logging

#
# Music File List
#
class MusicFileList():
        
    def __init__(self,  path):        
        self.music_files = {}
        self.logger = logging.getLogger('tunes.mfl')
        self.populate(path)
        

    def populate(self, base_directory):
        self.logger.debug("Populate : "+base_directory)
        for r,d,f in os.walk(base_directory):
            for files in f:
                if files.endswith(".flac"):
                    mf = MusicFile(files,  r)
                    self.add(mf)
                    
    def add(self,  mf):
        if not mf.name in self.music_files:
            self.music_files[mf.name] = mf
        else:
            music_file = self.music_files[mf.name]
            music_file.name = mf.name
            music_file.path = mf.path
            music_file.pitch = mf.pitch
            music_file.tempo= mf.tempo
            
     
    def load(self):
        db = shelve.open("MusicFiles.db")
        for key in db:
            self.add(db[key])
        db.close()  
        
    def save(self):
        db = shelve.open("MusicFiles.db")
        for mf in self.music_files.values():
            db[mf.name] = mf
        db.close()  

                    
                    
