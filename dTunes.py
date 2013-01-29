#!/usr/bin/python

import os
import dbm
import pickle
import shelve
import sys

import pygtk
import gtk

import logging

from data.MusicFile import MusicFile
from data.MusicFileList import MusicFileList

from MusicFileListWindow import MusicFileListWindow
from PyQt4 import QtCore, QtGui
from Player import Player
from Controller import Controller


def create_log():
        # create logger with 'spam_application'    
    logger = logging.getLogger('tunes')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('tunes.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)    
    


if __name__ == "__main__":
    create_log()
    logger = logging.getLogger('tunes.main')
    gtk.gdk.threads_init()
    app = QtGui.QApplication(sys.argv)

    logger.debug("Start")
    mfl = MusicFileList("/home/jcdwyer/Music/flac")
    mfl.load()
    mfl.save()

    player = Player()
    player.set_master_volume(50);

    logger.debug("Creating ui")
    ui = MusicFileListWindow(mfl)
    ui.show()
    controller = Controller(ui,  player)
    ui.set_controller(controller)
    player.set_controller(controller)
    logger.debug("ui Created")

    sys.exit(app.exec_())


