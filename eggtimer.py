#!/usr/bin/env python
import wx

class test(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1,
        "Test",
        pos=(50,50),
        size=(200,180), style=wx.DEFAULT_FRAME_STYLE)
        button0 = wx.Button(frame, -1, "Hello World!", (20, 20))
        button1 = wx.Button(frame, -1, "Goodbye World!", (20, 60))
        self.frame = frame
        self.frame.Show()

        frame2 = editor(None, "Small Editor")

        return True

class editor(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        self.Show(True)

if __name__ == '__main__':
    app = test()
    app.MainLoop()