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
import GUITemplate

class ChangeGControllerInterface:
    @abstractmethod
    def setLocalG(self, g: float):
        pass

class ChangeGDialog(GUITemplate.ChangeGDialog):
  def __init__(self, parent, controller: ChangeGControllerInterface, g: float):
    GUITemplate.ChangeGDialog.__init__(self, parent)
    self.parent = parent
    self.controller = controller
    self.setG(g)

  def setG(self, g):
    self.spinCtrlDoubleG.SetValue(g)
  
  def onBtnStdGClick( self, event ):
    self.setG(9.80665)
  
  def onBtnApplyClick( self, event ):
    value=float(self.spinCtrlDoubleG.GetValue())
    self.controller.setLocalG(value)
    self.Destroy()
