import wx
import glob, os, datetime, shutil
#import os
#import datetime
#import shutil

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 240))

        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Choose source and destination for files modified in the past 24 hours.", (150,10))

        # Create the origin folder label, textbox, and button
        wx.StaticText(panel, -1, "Source:", (34,43))
        self.OriginFilePath = wx.TextCtrl(panel, pos=(120,40), size=(250,25), name="Source", style=wx.TE_READONLY)
        wx.Button(panel, 1, "Source", (375, 40))
        self.Bind(wx.EVT_BUTTON, self.originBrowse, id=1)

        # Create the destination folder label, textbox, and button
        wx.StaticText(panel, -1, "Destination:", (5,73))
        self.DestFilePath = wx.TextCtrl(panel, pos=(120,70), size=(250,25), name="Destination", style=wx.TE_READONLY)
        wx.Button(panel, 2, "Destination", (375, 70))
        self.Bind(wx.EVT_BUTTON, self.destBrowse, id=2)

        # Create the copy files button
        wx.Button(panel, 3, "Copy Files", (190,100))
        self.Bind(wx.EVT_BUTTON, self.copyFiles, id=3)

        self.Show(True)
        
    def originBrowse(self, event):
        '''
        Dialog box for the origin folder
        '''
        
        dlg = wx.DirDialog(self, "Source Folder:")

        if dlg.ShowModal() == wx.ID_OK:
            self.OriginFilePath.WriteText(dlg.GetPath())
            
        dlg.Destroy()

    def destBrowse(self, event):
        '''
        Dialog box for the destination folder
        '''

        dlg = wx.DirDialog(self, "Destination Folder:")

        if dlg.ShowModal() == wx.ID_OK:
            self.DestFilePath.WriteText(dlg.GetPath())
            
        dlg.Destroy()

    def copyFiles(self, event):
        '''
        Copy files modified within 24 hours from origin to destination folder
        '''

        originPath = self.OriginFilePath.GetValue() + "\\"
        print(originPath)
        destPath = self.DestFilePath.GetValue() + "\\"
        print(destPath)
        fileType = ".txt"

        # Create list of text filenames in origin folder
        fileList = glob.glob(originPath + "*" + fileType)

        todaysDate = datetime.datetime.today()

        # Loop through the filenames
        for file in fileList:
            # Get last modified date and today's date
            modifyDate = datetime.datetime.fromtimestamp(os.path.getmtime(file))
            todaysDate = datetime.datetime.today()
    
            filePathList = file.split("\\") # Create a list from the filepath
            filename = filePathList[-1] # The last element is a the filename
    
            # If modified within last 24 hours, then copy to destination folder
            modifyDateLimit = modifyDate + datetime.timedelta(days=1)

            if modifyDateLimit > todaysDate:
                shutil.copy2(file, destPath + filename)
    
app = wx.App(False)
frame = MainWindow(None, "File Copy GUI")
app.MainLoop()
