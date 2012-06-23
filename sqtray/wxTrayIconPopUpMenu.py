import wx
from sqtray.models import Observable

import functools

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item



def CreatePopupMenu(model,interactor):
    toolsMENU = wx.Menu()
    ConnectionStatus = model.connected.get()
    if ConnectionStatus:
        create_menu_item(toolsMENU, 'Play', interactor.onScPlay)
        create_menu_item(toolsMENU, 'Pause', interactor.onScPause)
        create_menu_item(toolsMENU, 'Next', interactor.onScNext)
        create_menu_item(toolsMENU, 'Previous', interactor.onScPrevious)
        create_menu_item(toolsMENU, 'Rnd', interactor.onScRandom)
        toolsMENU.AppendSeparator()
    playersLen = len(model.Players)
    #print "Players=\n%s\n%s" % (model.Players,model.playerList)
    if playersLen >1:
        playersMENU = wx.Menu()
        toolsMENU.AppendMenu(-1, "Change Player", playersMENU) 
        player = model.GuiPlayer.get()
        if player != None:
            MenuItem = wx.MenuItem(playersMENU, -1, player)
            # Bind event to self.ChangePlayer but add the parameter "player" to the call back, with the value "player"
            playersMENU.Bind(wx.EVT_MENU, functools.partial(interactor.ChangePlayer,player = player), id=MenuItem.GetId())
            playersMENU.AppendItem(MenuItem)
            playersMENU.AppendSeparator()
        for playerName in  model.Players:
            if playerName != player:
                MenuItem = wx.MenuItem(playersMENU, -1, playerName)
                playersMENU.Bind(wx.EVT_MENU, functools.partial(interactor.ChangePlayer,player = playerName), id=MenuItem.GetId())
                playersMENU.AppendItem(MenuItem)

        toolsMENU.AppendSeparator()
    create_menu_item(toolsMENU, 'Settings', interactor.on_settings)
    toolsMENU.AppendSeparator()
    create_menu_item(toolsMENU, 'Exit', interactor.on_exit)
    #print toolsMENU
    return toolsMENU




class PopUpMenuInteractor(object):
    """ http://wiki.wxpython.org/ModelViewPresenter inspired """
    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
    def onScPlay(self,event):
        self.presenter.onScPlay()
    def onScPause(self,event):
        self.presenter.onScPause()
    def onScNext(self,event):
        self.presenter.onScNext()
    def onScPrevious(self,event):
        self.presenter.onScPrevious()
    def onScRandom(self,event):
        self.presenter.onScRandom()
    def ChangePlayer(self,event,player):
        playerStr = unicode(player)
        self.presenter.ChangePlayer(playerStr)
    def on_settings(self,event):
        self.presenter.on_settings()
    def on_exit(self,event):
        self.presenter.on_exit()




class PopupMenuPresentor(object):
    def __init__(self, Model, View,squeezecmd, interactor):
        self.Model = Model
        self.View = View
        self.squeezeConCtrl = squeezecmd
        interactor.install(self,self.View)
        self.player = Observable(None)
        self._cb_settings = []
    def AddCallbackSettings(self,func):
        self._cb_settings.append(func)
    def GetSqueezeServerPlayer(self):
        return self.player.get()
    def onScPause(self):
        player = self.GetSqueezeServerPlayer()
        #print "player",player
        if player != None:
            self.squeezeConCtrl.Pause(player)
        else:
            self.on_settings()    
    def onScPlay(self):
        player = self.GetSqueezeServerPlayer()
        if player != None:
            self.squeezeConCtrl.Play(player)
        else:
            self.on_settings()
    

    def onScNext(self):
        player = self.GetSqueezeServerPlayer()
        if player != None:
            #self.squeezecmd.squeezecmd_Index(player,1)
            
            self.squeezeConCtrl.Index(player,1)
        else:
            self.on_settings()
    def onScPrevious(self):
        player = self.GetSqueezeServerPlayer()
        if player != None:
            #self.squeezecmd.squeezecmd_Index(player,-1)
            self.squeezeConCtrl.Index(player,-1)
        else:
            self.on_settings()
    def onScRandom(self):
        player = self.GetSqueezeServerPlayer()
        if player != None:
            #self.squeezecmd.squeezecmd_randomplay(player)
            self.squeezeConCtrl.PlayRandomSong(player)
        else:
            self.on_settings()


    def on_settings(self):
        for item in self._cb_settings:
            item()
    def ChangePlayer(self,player):
        oldPlayer = self.player.get()
        if oldPlayer != player:
            self.player.set(player)
    def on_exit(self):
        #self.on_settings_close(event)
        #wx.CallAfter(self.View.Destroy)
        
        pass