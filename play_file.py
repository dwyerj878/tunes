#!/usr/bin/python

import pygst
pygst.require("0.10")
import gst
import gtk

file_name = "/home/jcdwyer/Music/flac/Cult/Electric/bad_fun.flac"
        
#gst_command = ('filesrc location=%s ! decodebin2 ! pitch pitch=0.06 tempo=1.0 ! autoaudiosink') % '/home/jcdwyer/Music/flac/Cult/Electric/bad_fun.flac'

gst_command = ('filesrc location=%s !decodebin ! audioconvert ! pitch pitch=0.8 tempo=2.0 !    audioconvert ! audioresample ! autoaudiosink') % '/home/jcdwyer/Music/flac/Cult/Electric/bad_fun.flac'
pipeline = gst.parse_launch(gst_command)
pipeline.set_state(gst.STATE_PLAYING)
pipeline.get_state()



#position = 10 * gst.SECOND
#rate = 0.5
#pipeline.seek(rate, gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE, gst.SEEK_TYPE_SET, position, gst.SEEK_TYPE_NONE, -1)

gtk.main()
