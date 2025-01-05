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
