import wx
import GUITemplate
import numpy as np

class CalibrationWizardFrame(GUITemplate.CalibrationFrame):
  def __init__(self, parent, ser):
    GUITemplate.CalibrationFrame.__init__(self, parent=parent)

    self.parent = parent

    self.Bind( wx.EVT_CLOSE, self.onClose )

    self.ser = ser
    self.ser.addObserver(self)

    self.step = 1
    self.maxSamples = 200
    self.time  = np.array([])
    self.force = np.array([])
    self.avg1 = 0.0
    self.avg2 = 0.0
    self.mass = 1.0
    self.calibrationFactor = 1.0
    msg = "s"+"%.2f"%(self.calibrationFactor)
    self.ser.sendMessage(msg)

    self.setAppearance()

  def setAppearance(self):
    if self.step == 1:
      self.sTxtStep1.Enable()
      self.txtCtrlMass.Enable()
      self.sTxtStep2.Disable()
      self.sTxtStep3.Disable()
      self.gaugeStep3.Disable()
      self.sTxtStep4.Disable()
      self.sTxtStep5.Disable()
      self.gaugeStep5.Disable()
    elif self.step == 2:
      self.sTxtStep1.Enable()
      self.txtCtrlMass.Disable()
      self.sTxtStep2.Enable()
      self.sTxtStep3.Disable()
      self.gaugeStep3.Disable()
      self.sTxtStep4.Disable()
      self.sTxtStep5.Disable()
      self.gaugeStep5.Disable()
    elif self.step == 3:
      self.sTxtStep1.Enable()
      self.txtCtrlMass.Disable()
      self.sTxtStep2.Enable()
      self.sTxtStep3.Enable()
      self.gaugeStep3.Enable()
      self.sTxtStep4.Disable()
      self.sTxtStep5.Disable()
      self.gaugeStep5.Disable()
    elif self.step == 4:
      self.sTxtStep1.Enable()
      self.txtCtrlMass.Disable()
      self.sTxtStep2.Enable()
      self.sTxtStep3.Enable()
      self.gaugeStep3.Enable()
      self.sTxtStep4.Enable()
      self.sTxtStep5.Disable()
      self.gaugeStep5.Disable()
    elif self.step == 5:
      self.sTxtStep1.Enable()
      self.txtCtrlMass.Disable()
      self.sTxtStep2.Enable()
      self.sTxtStep3.Enable()
      self.gaugeStep3.Enable()
      self.sTxtStep4.Enable()
      self.sTxtStep5.Enable()
      self.gaugeStep5.Enable()
    return

  def onBtnCancelClick( self, event ):
    event.Skip()

  def onBtnNextClick( self, event ):
    if self.step == 1:
      smass = self.txtCtrlMass.GetValue()
      try:
        self.mass = float(smass)
        if self.mass > 0:
          self.step += 1
        else:
          wx.MessageBox('A massa deve ser positiva', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)
      except:
        wx.MessageBox('Insira um número válido (use ponto como separador decimal)', 'Alerta', wx.OK | wx.ICON_EXCLAMATION)
    elif self.step == 2:
      self.step += 1
    elif self.step == 3:
      self.btnNext.Disable()
    elif self.step == 4:
      self.step += 1
    elif self.step == 5:
      self.btnNext.Disable()
    elif self.step == 6:
      self.close(True)
    else:
      pass
    self.setAppearance()
    event.Skip()

  def close(self, status):
    self.parent.calibrationFinished(status)
    self.ser.removeObserver(self)
    self.Destroy()

  # Closes this window
  def onClose(self, event):
    dial = wx.MessageDialog(None, 'Tem certeza que deseja parar?', 'Fechar',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    dial.SetYesNoLabels("Sim", "Não")
        
    if dial.ShowModal() == wx.ID_YES:
      self.close(False)
    event.Skip()

  def wxPSerialUpdate(self, msgs):
    if ( self.step == 3 or self.step == 5):
      atime  = np.array([])
      aforce = np.array([])
      for msg in msgs:
        data = msg.split(",")
        if data[0] == "1":
          atime  = np.append(atime,  float(data[1]))
          aforce = np.append(aforce, float(data[2]))
      
      if ( atime.size > 0 ):
        self.time  = np.append(self.time, atime)
        self.force = np.append(self.force, aforce)

      if ( self.step == 3 ):
        if ( self.force.size > self.maxSamples ):
          self.avg1 = np.average(self.force)
          self.btnNext.Enable()
          self.gaugeStep3.SetValue(100.0)
          self.time = np.array([])
          self.force = np.array([])
          self.step += 1
          self.setAppearance()
        else:
          self.gaugeStep3.SetValue(100.0*self.force.size / self.maxSamples)

      if ( self.step == 5 ):
        if ( self.force.size > self.maxSamples ):
          self.avg2 = np.average(self.force)
          self.calibrationFactor = (self.avg2-self.avg1)/self.mass
          txt = "s%.2f"%(self.calibrationFactor)
          self.ser.sendMessage(txt)    
          self.gaugeStep5.SetValue(100.0)
          self.time = np.array([])
          self.force = np.array([])
          self.step += 1
          self.btnNext.Enable()
          self.setAppearance()
          self.close(True)
        else:
          self.gaugeStep5.SetValue(100.0*self.force.size / self.maxSamples)
