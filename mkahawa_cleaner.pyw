#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Starlord
#
# Created:     16/03/2016
# Copyright:   (c) Starlord 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/bin/env python
import sqlite3 as sqlite
import time
import wx
import os
import os.path
import getpass
default_path_linux = r"/usr/home/%s/.mkahawa/mkahawa.db"%getpass.getuser()
alternate_path = "."
class MkahawaCleaner(wx.Frame):
    def __init__(self,title="                                       Fhitech Cyber Mkahawa Cleaner Version 1.0", ):
        wx.Frame.__init__(self, None,  -1, title, size=(1000, 550))
        if os.path.exists("cleaner.png"):
            img = '\cleaner.png' if os.name == 'nt' else '/cleaner.png'
            path = os.getcwd()
            newpath = path+img
            icon = wx.Icon(newpath, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        self.mkahawaDExitsb = True
        self.already_displayed = False
        self.main_panel = wx.Panel(self, -1, size=(-1,-1))
        self.main_panel.SetBackgroundColour(wx.BLUE)


        self.toppanel = wx.Panel(self.main_panel, -1, size=(-1, 60))
        self.toppanel.SetBackgroundColour(wx.GREEN)
        self.bttmpanel = wx.Panel(self.main_panel, -1, size=(-1, -1))
        # top cleaning button
        self.cleanbtn = wx.Button(self.toppanel, -1, 'Clear Mkahawa', size= (130, 40))
        self.exitbtn = wx.Button(self.toppanel, -1, 'Exit Cleaner', size= (80, 40))
        self.toppanel.Bind(wx.EVT_BUTTON, self.OnExit, id = self.exitbtn.GetId())
        self.toppanel.Bind(wx.EVT_BUTTON, self.OnClear, id=self.cleanbtn.GetId())
        tophsizer = wx.BoxSizer(wx.HORIZONTAL)
        tophsizer.Add(self.cleanbtn, 0, wx.EXPAND| wx.ALL, 10)
        tophsizer.Add(self.exitbtn, 0, wx.EXPAND| wx.ALL, 10)
        self.toppanel.SetSizer(tophsizer)

        self.txtctrl = wx.TextCtrl(self.bttmpanel, -1, size=(-1, -1), style=wx.TE_MULTILINE|wx.TE_READONLY)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.txtctrl, 1, wx.EXPAND)
        self.bttmpanel.SetSizer(hsizer)
        vsizer= wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toppanel, 0, wx.EXPAND|wx.BOTTOM, 5)
        vsizer.Add(self.bttmpanel, 1, wx.EXPAND)
        self.main_panel.SetSizer(vsizer)
        self.CreateStatusBar()
        self.SetStatusText("\tScript Developed by Samuel Nganj for Lenny N. @ Copyright 2016")
    def OnClear(self, event):
        self.DisplayResults()
    def GetDBConn(self):
        dbconnection = None
        mkahawa_checker = ""
        def timerz(num, srange, erange, location= "default"):
            self.txtctrl.AppendText("\nChecking if database exits in %s directory"%location)
            for i in range(1, 10):
                self.txtctrl.AppendText(".")
                time.sleep(1)
        if os.path.exists("mkahawa.db") == True:
                self.mkahawaDExitsb = True
                try:
                    timerz(1, 0, 5, location="Local")
                    dbconnection = sqlite.connect("mkahawa.db")
                    self.txtctrl.AppendText("\nConnection to mkahawa database established...\nListing Records in ")
                    for i in range (0, 3):
                        i  += 1
                        self.txtctrl.AppendText("%s, "%i)
                        time.sleep(3)
                except Exception:
                    self.txtctrl.AppendText("\nCould not connect to database file on local directory, program will check default directory")
        else:
            if os.path.exists(default_path_linux) == True:
                try:
                    timerz(1, 0, 5, location=".mkahawa")
                    dbconnection = sqlite.connect(default_path_linux)
                    self.txtctrl.AppendText("\nConnection to mkahawa database established...\nListing Records in ")
                    for i in range (0, 3):
                        i  += 1
                        self.txtctrl.AppendText("%s, "%i)
                        time.sleep(3)
                except Exception:
                    self.txtctrl.AppendText("\nCould not connect to database file on default location")
            else:
                self.txtctrl.AppendText("\nFile not found in path: %s"%str(default_path_linux))
##                    wx.MessageBox("Mkahawa database does not exist in local or home directory, check your settings again", "Mkahawa Database check Error", style=wx.OK|wx.ICON_WARNING)
        return dbconnection
    def DisplayResults(self):
        lol_sqlite = self.GetDBConn()
        if self.already_displayed != True:
            newgetter = None
            if lol_sqlite != None: newgetter = lol_sqlite.cursor()
            if  newgetter != None:
                newgetter.execute("select b.name, a.stime, a.etime, a.time, a.price from sessionslog a left join clients b on a.client = b.id")
                i = 1
                self.txtctrl.AppendText("\n"+"_"*110)
                header = "\nRecord\tComputer name\t\tStart Time\t\tEnd Time\t\t\tUsed Time\t\tPrice"
                self.txtctrl.AppendText(header)
                self.txtctrl.AppendText("\n"+"_"*110)
                self.SetStatusText("Displaying Mkahawa Records")
                total_earnings = 0
                for cname, stime, etime, usedtime, price in newgetter.fetchall():

                    txt = "\n"+str(i)+".\t"+str(cname)+"\t\t"+str(time.ctime(stime))+"\t\t"+str(time.ctime(etime))+"\t\t"+str(usedtime)+"\t\t"+str(price)
                    total_earnings += usedtime
                    self.txtctrl.AppendText("\n"+"_"*110)
                    self.txtctrl.AppendText(txt)
                    i += 1
                self.txtctrl.AppendText("\n"+"_"*110)
                if i > 1:
                    self.SetStatusText("Diplaying records from %d cyber sessions"%i)
                    self.already_displayed =True
                    ret = wx.MessageDialog(None, "Are you sure you want to clear the records ?", "Confirm Clearing Records", style=wx.YES_NO|wx.ICON_QUESTION)
                    if ret.ShowModal() == wx.ID_YES:
                        self.CleanDb(lol_sqlite)
                    else:
                        newgetter.close()
                        lol_sqlite.close()
                else:
                    wx.MessageBox("No records to clean", "Message", style=wx.ICON_INFORMATION|wx.OK)
                    self.SetStatusText("No records to clean")
            else:
                self.CleanDb(lol_sqlite)

    def CleanDb(self, db_connect):
        cleaner = None
        if db_connect != None: cleaner = db_connect.cursor()
        if cleaner != None:
            try:
                cleaner.execute("delete from sessionslog")
                db_connect.commit()
                db_connect.close()
                self.txtctrl.Clear()
                self.SetStatusText("")
                wx.MessageBox("Records Cleared successfully", "Successful operation", style=wx.ICON_INFORMATION|wx.OK)
            except Exception:
                wx.MessageBox("Error while trying to clear records", "Error while clearing records", style=wx.ICON_ERROR|wx.OK)
        else:
            self.txtctrl.AppendText("\nEmpty Connection object")
    def OnExit(self, event):
        self.Destroy()
if __name__ == '__main__':
    app = wx.App(False)
    frame = MkahawaCleaner()
    frame.Show()
    app.MainLoop()
