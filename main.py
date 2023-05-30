import wx
import MainFrame

print(wx.version())

app = wx.App()
mainFrame = MainFrame.MainFrame(parent=None)
mainFrame.Show()

app.MainLoop()