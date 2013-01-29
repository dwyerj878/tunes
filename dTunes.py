#!/usr/bin/python

import os
import dbm
import pickle
import shelve
import sys

import pygtk
import gtk

from MusicFile import MusicFile
from MusicFileList import MusicFileList

from MusicFileListWindow import MusicFileListWindow
from PyQt4 import QtCore, QtGui
from Player import Player
from Controller import Controller

if __name__ == "__main__":
    gtk.gdk.threads_init()
    app = QtGui.QApplication(sys.argv)

    print "Start"
    mfl = MusicFileList("/home/jcdwyer/Music/flac")
    mfl.load()
    mfl.save()

    player = Player()
    player.set_master_volume(50);

    print "Creating ui"
    ui = MusicFileListWindow(mfl)
    ui.show()
    controller = Controller(ui,  player)
    ui.set_controller(controller)
    player.set_controller(controller)
    print "ui Created"

    sys.exit(app.exec_())


