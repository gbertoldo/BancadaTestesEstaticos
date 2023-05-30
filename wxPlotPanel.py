import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np
# https://www.youtube.com/playlist?list=PLecOfLY9Yl9cqDZ1opVnWWfAxqrDgk-MH

class wxPlotPanel(wx.Panel):
  def __init__(self, parent, plotstyle, fontsize, dpi, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.PanelNameStr):
    wx.Panel.__init__(self, parent, id, pos, size, style, name)

    plt.rcParams['font.size'] = str(fontsize)
 
    self.figure = Figure((3, 2), dpi)
    self.axes = self.figure.add_subplot(111)
 
    # FigureCanvas is a kind of wx.Panel for Matplotlib
    self.canvas = FigureCanvas(self, -1, self.figure)

    # Lets add a sizer to contain the canvas (Panel)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
    self.SetSizer(self.sizer)

    # Creating an empty plot
    x = np.array([])
    y = np.array([])
    self.lines = self.axes.plot(x,y,plotstyle)
    
    # Drawing the figure
    self.canvas.draw()

    # Now lets create a sizer on the parent widget to contain the current panel and to expand it
    bSizer = wx.BoxSizer(wx.VERTICAL)
    bSizer.Add(self, wx.ID_ANY, wx.LEFT | wx.TOP | wx.EXPAND | wx.ALL, 10)
    parent.SetSizer(bSizer)

    self.Fit()

  def draw(self, x, y):
    if x.size > 0:
      self.axes.set_xlim(np.min(x),np.max(x))
      self.axes.set_ylim(np.min(y),np.max(y))
    else:
      self.axes.set_xlim(0,1)
      self.axes.set_ylim(0,1)
    self.lines[0].set_data(x, y)
    self.canvas.draw()
    self.canvas.flush_events()

  def setXLabel(self, label):
    self.axes.set_xlabel(label,)

  def setYLabel(self, label):
    self.axes.set_ylabel(label)

  def setGrid(self):
    self.axes.grid()

  def addToolbar(self):
      self.toolbar = NavigationToolbar(self.canvas)
      self.toolbar.Realize()
      # By adding toolbar in sizer, we are able to put it at the bottom
      # of the frame - so appearance is closer to GTK version.
      self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
      # update the axes menu on the toolbar
      self.toolbar.update()