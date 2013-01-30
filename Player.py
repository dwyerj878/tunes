#!/usr/bin/python

import pygst
pygst.require("0.10")
import gst
import gtk
from data.MusicFile import MusicFile
import logging

#
# Music file Player
#
class Player():
    
    # new player
    def __init__(self):
        self.logger = logging.getLogger('tunes.player')
        self.logger.debug("Creating Player")
        self.pipeline = gst.Pipeline("pipeline")
        self.volume = 50
        self.mf = None
        
        source = gst.element_factory_make("filesrc", "filesrc")
        decoder = gst.element_factory_make("decodebin", "decodebin")
        conv = gst.element_factory_make("audioconvert", "audioconvert")
        pitch = gst.element_factory_make("pitch", "pitch")
        volume = gst.element_factory_make("volume",  "volume")
        resample = gst.element_factory_make("audioresample", "audioresample")
        sink = gst.element_factory_make("autoaudiosink", "autoaudiosink")
        
        
        self.pipeline.add(source, decoder, conv, volume,  pitch,  resample,  sink)
        gst.element_link_many(source, decoder);
        gst.element_link_many(conv, pitch,  volume, resample,  sink)
        decoder.connect("new-decoded-pad", self.on_new_decoded_pad)
        self.pipeline.set_state(gst.STATE_PAUSED)
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)
        self.logger.debug("Player created")
        
    # set controller
    def set_controller(self,  controller):
        self.controller = controller
        
    # on pad change re-link
    def on_new_decoded_pad(self,  dbin, pad, islast):
        decoder = pad.get_parent()
        pipeline = decoder.get_parent()
        convert = pipeline.get_by_name('audioconvert')
        decoder.link(convert)
        
        #message = 
        #self.bus.post()
        pipeline.set_state(gst.STATE_PLAYING)
        self.logger.debug("linked!")
        
    # start playing a music file object
    def play(self,  mf):
        #file_name = "'"+self.path+"/"+self.name+"'"
        file_name = mf.path+"/"+mf.name
        self.logger.info("Playing : " + file_name)
        self.pipeline.set_state(gst.STATE_NULL)
        self.mf = mf
        
        #gst_command = ('filesrc location="%s" !decodebin ! audioconvert ! pitch pitch=0.8 tempo=2.0 !    audioconvert ! audioresample ! autoaudiosink') % file_name
        #pipeline = gst.parse_launch(gst_command)
        self.pipeline.get_by_name("filesrc").set_property("location", file_name)
        self.set_song_pitch(mf.pitch)
        self.set_song_tempo(mf.tempo)
        self.set_song_volume(mf.volume)
        self.pipeline.set_state(gst.STATE_PLAYING)
        # self.pipeline.get_state()
        
      
    # start/stop toggle
    def start_stop(self):
        if self.is_playing():
            self.pipeline.set_state(gst.STATE_PAUSED)
        else:
            self.pipeline.set_state(gst.STATE_PLAYING)
        return self.pipeline.get_state()
        
    # handle bus messages
    def on_message(self, bus, message):
        if self.controller:
            self.controller.handle_gst_message(bus,  message)
        
    # set master volume
    def set_master_volume(self,  value):
        self.volume = value;
        self.set_volume()
        
    # actual volume is the product of the master and the song volume
    def set_volume(self):
        level = float(self.volume)/100
        if self.mf is not None:
            songLevel = float(self.volume)/100 * float(self.mf.volume)/100
        else :
            songLevel = level
        self.logger.debug("Setting Volume " + str(self.volume) + " " + str(level) )
        
        if self.pipeline is not None:
           self.pipeline.get_by_name("volume").set_property("volume", songLevel)
           

    # check if the pipeline status includes playing
    def is_playing(self): 
        for st in self.pipeline.get_state():
            if st == gst.STATE_PLAYING:
                return True
        return False
        
    # set the song volume. 0 - 150     
    def set_song_volume(self,  value):
        if self.mf :
            self.mf.volume = value        
            self.set_volume();

    
    # set the pitch between -1000 -and 1000
    def set_song_pitch(self,  value):
        if self.mf:
            self.mf.pitch = value;
            pitch = 1+ float(value) / 2000;
            if self.pipeline :
               self.pipeline.get_by_name("pitch").set_property("pitch", pitch)
        
    # set the tempo between -100 -and 100
    def set_song_tempo(self,  value):
        if self.mf :
            self.mf.tempo = value;
            tempo = 1+ float(value) / 200;
            if self.pipeline :
               self.pipeline.get_by_name("pitch").set_property("tempo", tempo)
               
    def query_position(self):
        "Returns a (position, duration) tuple"

        try:
            position, format = self.pipeline.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self.pipeline.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position/ gst.SECOND, duration/ gst.SECOND)

    def seek(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        self.logger.debug("seeking to %r" % location)
        gst.debug("seeking to %r" % location)
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, location,
            gst.SEEK_TYPE_NONE, 0)

        res = self.pipeline.send_event(event)
        if res:
            gst.info("setting new stream time to 0")
            self.pipeline.set_new_stream_time(0L)
        else:
            gst.error("seek to %r failed" % location)
