import wx
from sqtray.models import Observable, squeezeConMdle, squeezePlayerMdl
from sqtray.JrpcServer import squeezeConCtrl
from sqtray.wxEvents import *

from sqtray.wxTaskBarIcon import TaskBarIcon
from sqtray.wxFrmSettings import Example


class myapp(wx.App):
    def __init__(self):
        super(myapp, self).__init__()
        
        self.model = squeezeConMdle()
        self.SqueezeServerPort = Observable(9000)
        self.SqueezeServerPort.addCallback(self.OnSqueezeServerPort)
        self.cfg = wx.FileConfig(appName="ApplicationName", 
                                    vendorName="VendorName", 
                                    localFilename=".squeezetray.cfg", 
                                    style=wx.CONFIG_USE_LOCAL_FILE)
        self.squeezeConCtrl = squeezeConCtrl(self.model)
        
        self.configRead()
        self.tb = TaskBarIcon()
        #print "tb=%s" %self.tb
        self.tb.app = self
        self.tb.cfg = self.cfg
        self.squeezeConCtrl.CbConnectionAdd(self.handleConnectionChange,self.tb)
        self.model.CbPlayersAvailableAdd(self.handlePlayersChange,self.tb)
        self.model.CbChurrentTrackAdd(self.handleTrackChange)
        

    def configRead(self):
        squeezeServerHost = 'localhost'
        if self.cfg.Exists('squeezeServerHost'):
            squeezeServerHost = self.cfg.Read('squeezeServerHost')
            
        self.SetSqueezeServerHost(squeezeServerHost)
        squeezeServerPort = 9000
        if self.cfg.Exists('squeezeServerPort'):
            try:
                squeezeServerPortTmp = int(self.cfg.ReadInt('squeezeServerPort'))
            except ValueError:
                squeezeServerPort = 9000
        self.SqueezeServerPort.set(squeezeServerPort)
        self.squeezeConCtrl.ConectionStringSet("%s:%s" % (self.GetSqueezeServerHost(),self.SqueezeServerPort.get()))
        
        SqueezeServerPlayer = None
        if self.cfg.Exists('SqueezeServerPlayer'):
            SqueezeServerPlayer = self.cfg.Read('SqueezeServerPlayer')
            
        self.SetSqueezeServerPlayer(SqueezeServerPlayer)
        self.squeezeConCtrl.RecConnectionOnline()
        
    def configSave(self):
        self.cfg.Write("squeezeServerHost", self.GetSqueezeServerHost())
        self.cfg.WriteInt("squeezeServerPort", self.GetSqueezeServerPort())
        self.cfg.Write("SqueezeServerPlayer", self.GetSqueezeServerPlayer())
        self.cfg.Flush()
        
    def handleConnectionChange(self,value,window):
        #self.squeezeConCtrl.RecConnectionOnline()
        #print "value=%s" % value
        #print self.GetSqueezeServerHost()
        #print dir(self)
        if not hasattr(self,'tb'):
            print "no tb"
            return
        
        wx.PostEvent(self.tb, ResultEvent2(EVT_RESULT_CONNECTED_ID,value))
        
    
    def handlePlayersChange(self,value,window,asda):
        #print "value=%s,%s,%s,%s" % (value,window,asda)
        #print self.GetSqueezeServerHost()
        #print dir(self)
        if not hasattr(self,'tb'):
            print "no tb"
            return
        value = 0
        wx.PostEvent(self.tb, ResultEvent2(EVT_RESULT_PLAYERS_ID,value))
        
    def handleTrackChange(self,value):
        #print "value=%s,%s,%s,%s" % (value,window,asda,asdfg)
        #print self.GetSqueezeServerHost()
        #print dir(self)
        if not hasattr(self,'tb'):
            print "no tb"
            return
        value = 0
        wx.PostEvent(self.tb, ResultEvent2(EVT_RESULT_CURRENT_TRACK_ID,value))    


    def SetSqueezeServerHost(self,host):
        Changed = False
        if not hasattr(self,'SqueezeServerHost'):
            Changed = True
            self.SqueezeServerHost = 'localhost'
        if self.SqueezeServerHost != host:
            Changed = True
        try:
            self.SqueezeServerHost = unicode(host)
        except TypeError:
            self.SqueezeServerHost = 'localhost'
        if Changed:
            #print " host has changed to %s"  % (self.SqueezeServerHost)
            self.squeezeConCtrl.ServerHostSet(self.SqueezeServerHost)
            self.squeezeConCtrl.RecConnectionOnline()
            
        
    def GetSqueezeServerHost(self):
        if hasattr(self,'SqueezeServerHost'):
            return self.SqueezeServerHost
        return 'localhost'
        
    def OnSqueezeServerPort(self,value):
        self.squeezeConCtrl.ServerPortSet(self.SqueezeServerPort)
        self.squeezeConCtrl.RecConnectionOnline()

    def GetSqueezeServerPort(self):
        if hasattr(self,'SqueezeServerHost'):
            return self.SqueezeServerPort.get()
        return 9000
    def SetSqueezeServerPlayer(self,player):
        self.SqueezeServerPlayer = player
        #print "player=%s" % player
        self.squeezeConCtrl.RecPlayerStatus(player)
        
    def GetSqueezeServerPlayer(self):        
        if hasattr(self,'SqueezeServerPlayer'):
            return self.SqueezeServerPlayer
        if self.model.playersCount.get() > 0:
            return unicode(self.model.playerList[0].name.get())
        return None
    
        
    