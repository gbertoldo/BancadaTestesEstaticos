import wx
import GUITemplate
import serial
import pserial
from datetime import datetime

import CalibrationWizardFrame
import wxPlotPanel
import numpy as np
import os
import sys
import pickle

VERSION="v1.1.0"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

# Possible states
READY=1
DISCONNECTED=2
CALIBRATING=3
RECORDING=4
CONNECTING=5


class ChangeGDialog(GUITemplate.ChangeGDialog):
  def __init__(self, parent, g):
    GUITemplate.ChangeGDialog.__init__(self, parent)
    self.parent = parent
    self.setLabel(g)

  def setLabel(self, g):
    self.txtG.SetLabel("%10.7f"%(g))
  
  def onBtnStdGClick( self, event ):
    self.setLabel(9.80665)
  
  def onBtnApplyClick( self, event ):
    try:
      value=float(self.txtG.GetValue())
      if (value >= 8) and (value <= 11):
        self.parent.setLocalG(value)
        self.Destroy()
      else:
        dial = wx.MessageDialog(None, 'Valor fora do intervalo aceitável: 8 a 11 m/s².', 'Erro',
            wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    except:
      dial = wx.MessageDialog(None, 'Número inválido. Obs.: use ponto ao invés de vírgula.', 'Erro',
            wx.OK | wx.ICON_ERROR)
      dial.ShowModal()
    pass

class MainFrame(GUITemplate.MainFrame):
  def __init__(self, parent):
    GUITemplate.MainFrame.__init__(self, parent)

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
    
    # Reading the configuration file
    self.parameters=self.readConfigParameters()

    # Data
    self.time = np.array([])
    self.force = np.array([])
    self.timeFiltered = np.array([])
    self.forceFiltered = np.array([])
    self.maxNumOfPoints = 1000
    self.npArrayMaxSize = 50000
    self.outputFileName = ""
    self.tare = 0.0
    self.lastForce = 0.0
    self.time0 = 0.0
    self.isBusy = False

    # Serial connection
    self.ser = None
    self.onBmpBtnReloadClick(None)

    # Plot panel
    self.plotPanel = wxPlotPanel.wxPlotPanel( self.panelPlotBackground, "-", 40,25, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    self.plotPanel.setXLabel("t (s)")
    self.plotPanel.setYLabel("F")
    self.plotPanel.setGrid()
    self.plotPanel.addToolbar()

    self.plotPanel.draw(np.array([]),np.array([]))


    # Current state
    self.state = DISCONNECTED
    self.setState(self.state)

    # Setting parameters
    self.setLocalG(self.parameters["g"])



  def readConfigParameters(self):
    # default parameters
    par={"version":VERSION, "g":9.80665}

    # trying to read the parameters from file
    if os.path.isfile("config.cfg"):
      with open("config.cfg", 'rb') as file:  
        par = pickle.load(file)
    else: # if the file does not exist, create one
      self.writeConfigParameters(par)
    return par

  def writeConfigParameters(self, par):
    with open("config.cfg", 'wb') as file:  
      pickle.dump(par, file)

  def setLocalG(self,g):
    self.txtG.SetLabel("g =%10.7f m/s²"%(g))
    self.parameters["g"]=g
    self.writeConfigParameters(self.parameters)
    self.updateUnit()

  def onBtnChangeG( self, event ):
    dial=ChangeGDialog(self,self.parameters["g"])
    dial.ShowModal()
    
  def setState(self, state):
    if (state == DISCONNECTED):
      self.state = state
      self.setDisconnectedAppearance()
    elif (state == READY ):
      self.state = state
      self.setConnectedAppearance()
    elif state == CALIBRATING:
      self.state = state
      self.setCalibratingAppearance()
    elif state == RECORDING:
      self.state = state
      self.setRecordingAppearance()
    elif state == CONNECTING:
      self.state = state
      self.setConnectingAppearance()
    else:
      print("Unknown state...")

  def setConnectedAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Enable()
    self.updateForceDisplay()
    self.btnClearPlot.Enable()
    self.btnTare.Enable()
    self.btnStartRec.Enable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("PRONTO P. GRAVAR")
    self.sTxtOFileName.SetLabel("")
    self.updateUnit()
    self.radioBoxUnits.Enable()
    return

  def setDisconnectedAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figDisconnected)
    self.btnConnect.Enable()
    self.btnCalibrate.Disable()
    self.updateForceDisplay()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("DESCONECTADO")
    self.sTxtOFileName.SetLabel("")
    self.updateUnit()
    self.radioBoxUnits.Disable()
    return

  def setRecordingAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Disable()
    self.updateForceDisplay()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Enable()
    self.sTxtStatus.SetBackgroundColour(wx.Colour(wx.RED))
    self.sTxtStatus.SetLabel("GRAVANDO...")
    self.sTxtOFileName.SetLabel(self.outputFileName)
    self.updateUnit()
    self.radioBoxUnits.Disable()
    return

  def setCalibratingAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figConnected)
    self.btnConnect.Disable()
    self.btnCalibrate.Disable()
    self.updateForceDisplay()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("CALIBRANDO...")
    self.sTxtOFileName.SetLabel("")
    self.updateUnit()
    self.radioBoxUnits.Disable()
    return

  def setConnectingAppearance(self):
    self.bmpConnStatus.SetBitmap(self.figDisconnected)
    self.btnConnect.Enable()
    self.btnCalibrate.Disable()
    self.updateForceDisplay()
    self.btnClearPlot.Disable()
    self.btnTare.Disable()
    self.btnStartRec.Disable()
    self.btnStopRecClick.Disable()
    self.sTxtStatus.SetBackgroundColour(self.sTxtStatusbgColor)
    self.sTxtStatus.SetLabel("CONECTANDO...")
    self.sTxtOFileName.SetLabel("")
    self.updateUnit()
    self.radioBoxUnits.Disable()
    return

  def onBmpBtnReloadClick( self, event ):
    # Getting the available ports
    commList = serial.tools.list_ports.comports()
    self.choiceSerial.Clear()
    for item in commList:
      self.choiceSerial.Append(item.device)

    if len(commList) > 0:
      self.choiceSerial.SetSelection(0)
    

  def onBtnConnectClick( self, event ):
    idx = self.choiceSerial.GetSelection()
    if ( idx == wx.NOT_FOUND ):
      wx.MessageBox('Selecione um dispositivo', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)
      return
    else:
      devser = self.choiceSerial.GetString(idx)
    self.ser = pserial.wxPSerial(self, notificationPeriod=200, port=devser, baudrate=115200)

    if self.ser.is_open():
      self.setState(CONNECTING)
    else:
      self.ser = None
      self.setState(DISCONNECTED)
      wx.MessageBox('Erro ao conectar ao dispositivo', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)

    event.Skip()

  def onBtnCalibrateClick( self, event ):
    self.setState(CALIBRATING)
    frm = CalibrationWizardFrame.CalibrationWizardFrame(self, self.ser)
    frm.Show()
    event.Skip()

  def calibrationFinished(self, status=False):
    self.setState(READY)

    if status:
      wx.MessageBox('Calibração concluída com sucesso', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)

    self.clearPlot()

  def clearPlot(self):
    self.time = np.array([])
    self.force = np.array([])
    self.timeFiltered = np.array([])
    self.forceFiltered = np.array([])
    self.updateForceDisplay()
    self.replot()
    

  def onBtnClearPlotClick( self, event ):
    if self.time.size > 0:
      self.time0 = self.time[-1]
    else:
      self.time0 = 0
    self.clearPlot()
    event.Skip()

  def onBtnStartRecClick( self, event ):
    now = datetime.now()
    self.outputFileName = now.strftime("log_%Y_%m_%d__%Hh_%Mmin_%Ss.txt")
    self.updateForceDisplay()
    self.replot()
    with open(self.outputFileName, 'w') as file:
      file.write("# tempo (s)  força "+self.unitLabel+"\n")
    self.setState(RECORDING)
    event.Skip()

  def onBtnStopRecClick( self, event ):
    self.outputFileName = ""
    self.setState(READY)
    event.Skip()

  def onBtnTareClick( self, event ):
    if self.force.size > 0:
      self.tare = self.lastForce 
    self.updateForceDisplay()
    self.replot()

    event.Skip()

  def onRadioBoxUnitsClick( self, event ):
    self.updateUnit()
    event.Skip()

  def onRadioBoxGraphOptionClick( self, event ):
    event.Skip()

  def updateUnit(self):
    unit = self.radioBoxUnits.GetSelection()
    if unit == 0:
      self.unitFactor = self.parameters["g"]
      self.unitLabel = "(N)"
      self.plotPanel.setYLabel("F (N)")
    elif unit == 1:
      self.unitFactor = 1.0
      self.unitLabel = "(kgf)"
      self.plotPanel.setYLabel("F (kgf)")
    elif unit == 2:
      self.unitFactor = 1E3
      self.unitLabel = "(gf)"
      self.plotPanel.setYLabel("F (gf)")

    self.sTxtForceLabel.SetLabel("Força "+self.unitLabel+":")
    self.sTxtMaxForceLabel.SetLabel("Força máxima "+self.unitLabel+":")

    self.replot()

  def updateForceDisplay(self):
    if ( self.force.size > 0 ):
      self.sTxtForce.SetLabel("%15.4f\n"%((self.force[-1]-self.tare)*self.unitFactor))
      self.sTxtMaxForce.SetLabel("%15.4f\n"%((max(self.force)-self.tare)*self.unitFactor))
    else:
      self.sTxtForce.SetLabel("---")
      self.sTxtMaxForce.SetLabel("---")

  def wxPSerialUpdate(self, msgs):
    if not self.isBusy:
      self.isBusy=True
      if (self.state == CONNECTING ):
        self.setState(READY)
      else:
        atime  = np.array([])
        aforce = np.array([])
        for msg in msgs:
          data = msg.split(",")
          if data[0] == "1":
            atime  = np.append(atime,  float(data[1]))
            aforce = np.append(aforce, float(data[2]))
        
        if ( atime.size > 0 ):
          self.lastForce = aforce[-1]
          self.time  = np.append(self.time, atime)
          self.force = np.append(self.force, aforce)
          self.replot()
          if (self.state == RECORDING):
            self.save(atime-self.time0, aforce-self.tare)
          self.updateForceDisplay()
          if self.time.size > self.npArrayMaxSize:
            self.time = self.time[-self.npArrayMaxSize:-1]
            self.force = self.force[-self.npArrayMaxSize:-1]
      self.isBusy=False

  def save(self, atime, aforce):
    with open(self.outputFileName, 'a') as file:
      for i in range(0,atime.size):
        file.write("%15.3f %15.4f\n"%(atime[i],aforce[i]*self.unitFactor))
      
  def replot(self):
    if (self.state == READY or self.state == RECORDING):
      plotOption = self.radioBoxGraphOption.GetSelection()
      if plotOption != 2: # if not paused
        # filtering
        if len(self.time) > self.maxNumOfPoints:
          if ( plotOption == 0 ): # all
            rfactor = int(len(self.time) / self.maxNumOfPoints)
            self.timeFiltered = self.time[::rfactor]-self.time0
            self.forceFiltered = (self.force[::rfactor]-self.tare)*self.unitFactor
          elif ( plotOption == 1 ): # slide
            self.timeFiltered = self.time[-self.maxNumOfPoints:-1]-self.time0
            self.forceFiltered = (self.force[-self.maxNumOfPoints:-1]-self.tare)*self.unitFactor
        else:
          self.timeFiltered = self.time-self.time0
          self.forceFiltered = (self.force-self.tare)*self.unitFactor

        if self.timeFiltered.size > 0:
          self.plotPanel.draw(self.timeFiltered,self.forceFiltered)
        else:
          self.plotPanel.draw(np.array([]),np.array([]))