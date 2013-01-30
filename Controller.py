#!/usr/bin/python

from PyQt4 import QtCore,QtGui
import pygst
pygst.require("0.10")
import gst
import logging
import sys

#
# The C in MVC
#
# model : player / music file
# view : music file list window
#
class Controller():
    
    #
    # create a new controller
    def __init__(self,  file_list_window,  player):
        self.mf = None
        self.view = file_list_window
        self.player = player
        self.logger = logging.getLogger('tunes.controller')
    
    #
    # Set the song and play it
    #
    def set_song(self,  mf):
        self.logger.debug("set song")
        self.mf = mf
        self.view.set_song_name(mf.name)
        self.view.set_song_pitch(mf.pitch)
        self.view.set_song_tempo(mf.tempo)
        self.view.set_song_volume(mf.volume)
        self.player.play(mf)
        position,  duration = self.player.query_position()
        self.multiplier = sys.maxint/duration
        self.logger.debug("duration : " + str(duration))
        self.logger.debug("multiplier : " + str(self.multiplier))
        self.mf.duration = duration
        self.view.set_seek_values(0,  duration/self.multiplier)
        
        
    def start_stop(self):
        self.logger.debug("start/stop")
        state = self.player.start_stop() 
    
    # update start/pause button text
    def update_start_button(self):
        self.logger.debug("update buttons")
        if self.player.is_playing():
            self.view.startPauseButton.setText(QtGui.QApplication.translate("MusicFileListWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
            self.view.stopButton.setEnabled(True)
        else:
            self.view.startPauseButton.setText(QtGui.QApplication.translate("MusicFileListWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
            self.view.stopButton.setEnabled(False)

    # handle master volume change request
    # expected values 0 - 100
    def set_master_volume(self,  value):
        self.logger.debug("set master volume " + str(value))
        self.player.set_master_volume(value)
        
    # handle song volume change request
    # expected values 0 - 150
    def set_song_volume(self,  value):
        self.logger.debug("set song volume " + str(value))
        self.player.set_song_volume(value)

    # handle song pitch change request 
    # expected values -1000 - 1000
    def set_song_pitch(self,  value):
        self.logger.debug("set song pitch " + str(value))
        self.player.set_song_pitch(value)
        
    # handle song tempo change request
    # expected values -100 - 100
    def set_song_tempo(self,  value):
        self.logger.debug("set song tempo " + str(value))
        self.player.set_song_tempo(value)
    
    #
    # Handle GStreamer messages fom the player
    #
    def handle_gst_message(self, bus, message):
        if message.type == gst.MESSAGE_STATE_CHANGED:
            self.update_start_button()
        elif message.type == gst.MESSAGE_EOS:
            self.update_start_button()
        elif message.type == gst.MESSAGE_TAG:
            """message tag"""
        else :
            self.logger.debug(message)
            
    def seek(self,  value):
        
        self.player.seek(value*self.multiplier*gst.SECOND)
