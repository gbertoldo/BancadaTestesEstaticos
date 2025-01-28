"""
  The MIT License (MIT)

  Copyright (C) 2024 Guilherme Bertoldo
  (UTFPR) Federal University of Technology - Parana

  Permission is hereby granted, free of charge, to any person obtaining a 
  copy of this software and associated documentation files (the “Software”), 
  to deal in the Software without restriction, including without limitation 
  the rights to use, copy, modify, merge, publish, distribute, sublicense, 
  and/or sell copies of the Software, and to permit persons to whom the Software 
  is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all 
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from abc import abstractmethod
import wx
import numpy as np
import GUITemplate
import wxPlotPanel
from utils import *

VERSION="v1.1.3"

class MainFrameControllerInterface:  
  @abstractmethod
  def getAvailableSerialPorts(self):
    pass
  @abstractmethod
  def connectToSerial(self, port: str):
    pass
  @abstractmethod
  def startCalibration(self):
    pass
  @abstractmethod
  def changeG(self):
    pass
  @abstractmethod
  def clearData(self):
    pass
  @abstractmethod
  def startRecording(self):
    pass
  @abstractmethod
  def stopRecording(self):
    pass
  @abstractmethod
  def tare(self):
    pass
  @abstractmethod
  def setForceUnit(self, opt: int):
    pass
  @abstractmethod
  def setGraphOption(self, opt: int):
    pass

class MainFrameParameters:
  def __init__(self):
    self.par = {}
    self.par["listofports"] = []
    self.par["g"] = 9.80665
    self.par["listOfUnits"] = ["newton","kgf","gf"]
    self.par["selectedUnit"] = self.par["listOfUnits"][0] 
    self.par["listOfGraphOpt"] = ["complete", "slide", "paused"]
    self.par["selectedGraphOpt"] = self.par["listOfGraphOpt"][0] 

class MainFrame(GUITemplate.MainFrame):
  def __init__(self, parent: wx.Frame, controller: MainFrameControllerInterface, parameters: MainFrameParameters):
    GUITemplate.MainFrame.__init__(self, parent)

    self.controller = controller
    self.SetTitle("Bancada de testes estáticos - " + VERSION + " - GFT/GFCS")

    # Adjusting figures
    figReload = wx.Bitmap(resource_path("./fig/reload.png"))
    figReload = scale_bitmap(figReload, 15, 15)
    self.bmpBtnReload.SetBitmap(figReload)
    self.figConnected = wx.Bitmap(resource_path("./fig/connected.png"))
    self.figConnected = scale_bitmap(self.figConnected, 20, 20)
    self.figDisconnected = wx.Bitmap(resource_path("./fig/disconnected.png"))
    self.figDisconnected = scale_bitmap(self.figDisconnected, 20, 20)

    # Original background color
    self.sTxtStatusbgColor = self.sTxtStatus.GetBackgroundColour()
    
    # Plot panel
    self.plotPanel = wxPlotPanel.wxPlotPanel( self.panelPlotBackground, "-", 40,25, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    self.plotPanel.setXLabel("t (s)")
    self.plotPanel.setYLabel("F")
    self.plotPanel.setGrid()
    self.plotPanel.addToolbar()
    self.setParameters(parameters)
    self.replot()

    self.setDisconnectedAppearance()

  def setParameters(self, p: MainFrameParameters):
    self.setListOfPorts(p.par["listofports"])
    self.setLocalG(p.par["g"])
    self.setSelectedUnit(p.par["selectedUnit"])
    self.setSelectedGraphOpt(p.par["selectedGraphOpt"])

  def setListOfPorts(self, listOfPorts: list):
    self.choiceSerial.Clear()
    self.choiceSerial.AppendItems(listOfPorts)
    if (len(listOfPorts)>0):
      self.choiceSerial.SetSelection(0)

  def setLocalG(self, g: float):
    self.txtG.SetLabel("g =%11.8f m/s²"%(g))

  def setSelectedUnit(self, unit):
    if unit == "newton":
      self.plotPanel.setYLabel("F (N)")
      self.radioBoxUnits.SetSelection(0)
      self.sTxtForceLabel.SetLabel("Força (N):")
      self.sTxtMaxForceLabel.SetLabel("Força máxima (N):")
    elif unit == "kgf":
      self.plotPanel.setYLabel("F (kgf)")
      self.radioBoxUnits.SetSelection(1)
      self.sTxtForceLabel.SetLabel("Força (kgf):")
      self.sTxtMaxForceLabel.SetLabel("Força máxima (kgf):")
    else:
      self.plotPanel.setYLabel("F (gf)")
      self.radioBoxUnits.SetSelection(2)
      self.sTxtForceLabel.SetLabel("Força (gf):")
      self.sTxtMaxForceLabel.SetLabel("Força máxima (gf):")

  def setSelectedGraphOpt(self, opt):
    if opt == "complete":
      self.radioBoxGraphOption.SetSelection(0)
    elif opt == "slide":
      self.radioBoxGraphOption.SetSelection(1)
    else:
      self.radioBoxGraphOption.SetSelection(2)

  def setConnectedAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Enable()
    self.btnClearPlot.Enable()
    self.btnTare.Enable()
    self.btnStartRec.Enable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("PRONTO P. GRAVAR")
    self.sTxtOFileName.SetLabel("")
    self.radioBoxUnits.Enable()
    self.btnChangeG.Enable()
    return

  def setDisconnectedAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figDisconnected)
    self.btnConnect.Enable()
    self.btnCalibrate.Disable()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("DESCONECTADO")
    self.sTxtOFileName.SetLabel("")
    self.radioBoxUnits.Disable()
    self.btnChangeG.Enable()
    return

  def setRecordingAppearance(self, outputFileName: str):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Disable()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Enable()
    self.sTxtStatus.SetBackgroundColour(wx.Colour(wx.RED))
    self.sTxtStatus.SetLabel("GRAVANDO...")
    self.sTxtOFileName.SetLabel(outputFileName)
    self.radioBoxUnits.Disable()
    self.btnChangeG.Disable()
    return

  def setCalibratingAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Disable()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("CALIBRANDO...")
    self.sTxtOFileName.SetLabel("")
    self.radioBoxUnits.Disable()
    self.btnChangeG.Disable()
    return

  def setConnectingAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figDisconnected)
    self.btnConnect.Enable()
    self.btnCalibrate.Disable()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("CONECTANDO...")
    self.sTxtOFileName.SetLabel("")
    self.radioBoxUnits.Disable()
    self.btnChangeG.Enable()
    return

  def onBmpBtnReloadClick( self, event ):
    self.setListOfPorts(self.controller.getAvailableSerialPorts())
    event.Skip()

  def onBtnConnectClick( self, event ):
    idx = self.choiceSerial.GetSelection()
    if ( idx == wx.NOT_FOUND ):
      wx.MessageBox('Selecione um dispositivo', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)
      return
    else:
      port = self.choiceSerial.GetString(idx)
      self.controller.connectToSerial(port)
    event.Skip()

  def onBtnCalibrateClick( self, event ):
    self.controller.startCalibration()
    event.Skip()

  def onBtnChangeG( self, event ):
    self.controller.changeG()
    event.Skip()

  def onBtnClearPlotClick( self, event ):
    self.controller.clearData()
    event.Skip()

  def onBtnStartRecClick( self, event ):
    self.controller.startRecording()
    event.Skip()

  def onBtnStopRecClick( self, event ):
    self.controller.stopRecording()
    event.Skip()

  def onBtnTareClick( self, event ):
    self.controller.tare()
    event.Skip()

  def onRadioBoxUnitsClick( self, event ):
    self.controller.setForceUnit(self.radioBoxUnits.GetSelection())
    event.Skip()

  def onRadioBoxGraphOptionClick( self, event ):
    self.controller.setGraphOption(self.radioBoxGraphOption.GetSelection())
    event.Skip()

  def setForceInfo(self, F: float, Fmax: float, size: int):
    if ( size > 0 ):
      self.sTxtForce.SetLabel("%15.4f"%(F))
      self.sTxtMaxForce.SetLabel("%15.4f"%(Fmax))
    else:
      self.sTxtForce.SetLabel("---")
      self.sTxtMaxForce.SetLabel("---")
     
  def replot(self, time: np.array = np.array([]), force: np.array = np.array([])):
      self.plotPanel.draw(time, force)
