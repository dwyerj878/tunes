
from PyQt4 import QtCore,QtGui
import sys
import pygst
pygst.require("0.10")
import gst
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMainWindow
from UIFileListWindow import Ui_MusicFileListWindow

class MusicFileListWindow(QMainWindow,  Ui_MusicFileListWindow):

    def __init__(self,  data,  parent=None):
        print "Creating Window"        
        super(MusicFileListWindow, self).__init__(parent)

        # Set up the user interface from Designer.
        print "Setup UI"
        self.setupUi(self)
        print "Window Created"
        
        self.populate(data)
        
    
    def populate(self,  data):
        self.model = data
        self.populateTable()

    def populateTable(self):
        row = 0
        self.tableWidget.setRowCount(len(self.model.music_files))
        
        for mf in self.model.music_files.values():        
            print mf.name+"("+mf.path+", "+str(mf.pitch)+", "+str(mf.tempo)+")"
            nameItem = QtGui.QTableWidgetItem(mf.name)
            nameItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            
            pathItem = QtGui.QTableWidgetItem(mf.path)
            pathItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            
            pitchItem = QtGui.QTableWidgetItem(mf.pitch)
            speedItem = QtGui.QTableWidgetItem(mf.tempo)
            
            self.tableWidget.setItem(  row, 0,  nameItem)  
            self.tableWidget.setItem(  row, 1,  pathItem)  
            self.tableWidget.setItem(  row, 3,  pitchItem)  
            self.tableWidget.setItem(  row, 4,  speedItem)  

            row += 1
    
    def rowDoubleClicked(self,  modelIndex):
        mf = self.model.music_files.values()[ modelIndex.row()]
        self.controller.set_song(mf)
        
    def startPausedClicked(self):
        self.controller.start_stop();
        
            
    def nextSong(self):
        """next"""
        print "next"
        
    def previousSong(self):
        """previous"""
        print "prev"
    
    # master volume
    def volumeSliderMoved(self,  value):  
        self.controller.set_master_volume(value)
        
        
    # update song volume
    def songVolumeSliderMoved(self,  value):
        self.controller.set_song_volume(value)
        
        
    # update pitch
    def songPitchSliderMoved(self,  value):
        self.controller.set_song_pitch(value)
     
    # update speed
    def songTempoSliderMoved(self,  value):
        self.controller.set_song_tempo(value)
    
    # set controller
    def set_controller(self,  controller):
        self.controller = controller
    
    # set song name
    def set_song_name(self,  name):
        self.songNameLabel.setText(name)
        
    # -1000 - 1000
    def set_song_pitch(self,  value):
        self.songPitchSlider.setValue(value)

    # 0 - 150
    def set_song_volume(self,  value):
        self.songVolumeSlider.setValue(value)

    # 100 - 100
    def set_song_tempo(self,  value):
        self.songTempoSlider.setValue(value)

    def set_seek_values(self,  position,  duration): 
        self.songPositionSlider.value = position
        self.songPositionSlider.maximum = duration
        
    def songPositionSliderMoved(self,  value):
        self.controller.seek(value)

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    hwl1 = MusicFileListWindow()
    hwl1.show()
    sys.exit(app.exec_())