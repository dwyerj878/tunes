#!/usr/bin/python

from PyQt4 import QtCore,QtGui
import pygst
pygst.require("0.10")
import gst


class Controller():
     
    mf = None
    player = None
    view = None
    
    def __init__(self,  file_list_window,  player):
        self.view = file_list_window
        self.player = player
    
    def set_song(self,  mf):
        self.mf = mf
        self.view.set_song_name(mf.name)
        self.view.set_song_pitch(mf.pitch)
        self.view.set_song_tempo(mf.tempo)
        self.view.set_song_volume(mf.volume)
        self.player.play(mf)
        position,  duration = self.player.query_position()
        self.view.set_seek_values(position,  duration)
        #self.update_start_button()
        
    def start_stop(self):
        state = self.player.start_stop()
        #self.update_start_button()
    
    def update_start_button(self):
        if self.player.is_playing():
            self.view.startPauseButton.setText(QtGui.QApplication.translate("MusicFileListDialog", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.view.startPauseButton.setText(QtGui.QApplication.translate("MusicFileListDialog", "Start", None, QtGui.QApplication.UnicodeUTF8))

    def set_master_volume(self,  value):
        self.player.set_master_volume(value)
        
    def set_song_volume(self,  value):
        self.player.set_song_volume(value)
    
    def set_song_pitch(self,  value):
        self.player.set_song_pitch(value)
        
    def set_song_tempo(self,  value):
        self.player.set_song_tempo(value)
    
    def handle_gst_message(self, bus, message):
        if message.type == gst.MESSAGE_STATE_CHANGED:
            self.update_start_button()
        elif message.type == gst.MESSAGE_EOS:
            self.update_start_button()
        elif message.type == gst.MESSAGE_TAG:
            """message tag"""
        else :
            print message
            
    def seek(self,  value):
        self.player.seek(value)
