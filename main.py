import wx
import MainFrame

app = wx.App()
mainFrame = MainFrame.MainFrame(parent=None)
#mainFrame.SetIcon(wx.Icon(MainFrame.resource_path("./fig/icon.png")))
mainFrame.Show()

app.MainLoop()