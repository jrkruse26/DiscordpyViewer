import wx
import wx.lib.scrolledpanel

class GUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Test app v1.0", style = wx.DEFAULT_FRAME_STYLE )
        self.Center()
        self.CreateStatusBar()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll = wx.ScrolledWindow(self, -1)
        self.scroll.SetScrollbars(1, 1, 600, 400)
        panelA = wx.lib.scrolledpanel.ScrolledPanel(self.scroll, -1, style=wx.SIMPLE_BORDER, size=(300,200))
        panelA.SetupScrolling()
        panelA.SetBackgroundColour('#EEE111')
        panelB = wx.lib.scrolledpanel.ScrolledPanel(self.scroll, -1, style=wx.SIMPLE_BORDER, size=(200,200))
        panelB.SetupScrolling()
        panelB.SetBackgroundColour('#Eaa222')
        mainSizer.Add(panelA, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(panelB, 1, wx.ALL|wx.EXPAND, 5)
        self.scroll.SetSizer(mainSizer)

if __name__=='__main__':
    app = wx.App(0)
    frame = GUI().Show()
    app.MainLoop()