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
import numpy as np

import wx

import GUITemplate

class CalibrationWizardControllerInterface:
  @abstractmethod
  def nextStep(self):
    pass

  @abstractmethod
  def close(self):
    pass


class CalibrationWizardFrame(GUITemplate.CalibrationFrame):
  def __init__(self, parent: wx.Frame, controller: CalibrationWizardControllerInterface, m: float):
    GUITemplate.CalibrationFrame.__init__(self, parent=parent)
    self.parent = parent
    self.controller = controller
    self.Bind( wx.EVT_CLOSE, self.onClose )
    self.gaugeStep3.SetRange(100)
    self.gaugeStep5.SetRange(100)
    self.txtCtrlMass.SetValue(m)

  def getCalibrationMass(self):
    return self.txtCtrlMass.GetValue()

  def onBtnCancelClick( self, event ):
    self.close()
    event.Skip()

  def onBtnNextClick( self, event ):
    self.controller.nextStep()

  def close(self):
    self.controller.close()

  # Closes this window
  def onClose(self, event):
    #dial = wx.MessageDialog(None, 'Tem certeza que deseja parar?', 'Fechar',
    #        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    #dial.SetYesNoLabels("Sim", "Não")
        
    #if dial.ShowModal() == wx.ID_YES:
    #  self.close()
    self.close()
    event.Skip()

  def setForce1Percentage(self, p: int):
    self.gaugeStep3.SetValue(p)
    
  def setForce2Percentage(self, p: int):
    self.gaugeStep5.SetValue(p)