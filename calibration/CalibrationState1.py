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
from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationState2 import *

"""
    State 1:
      - Gets the current calibration factor from MCU, and 
      - Requests the calibration mass value from the user interface.
"""
class CalibrationState1(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.calibrationMass = 0.0
        self.calibrationFactor = 0.0
        self.parent.requestCalibrationFactor()
        self.setFrameAppearance()

    def isReady(self):
        return ( self.calibrationMass > 0.0 ) and ( self.calibrationFactor > 0.0 ) 

    def nextStep(self):
        self.calibrationMass = self.frame.txtCtrlMass.GetValue()
        if self.isReady():
            self.parent.setBackupCalibrationFactor(self.calibrationFactor)
            self.parent.setCalibrationMass(self.calibrationMass)
            self.parent.setState(CalibrationState2(self.parent,self.frame))
        else:
            self.parent.requestCalibrationFactor()

    def close(self):
        self.parent.setState(CalibrationStateAbort(self.parent,self.frame))

    def updateCalibrationFactor(self, msgs: list[float]):
        self.calibrationFactor = msgs[-1]
        self.parent.setBackupCalibrationFactor(self.calibrationFactor)

    def updateTimeAndForce(self, time:np.array, force:np.array):
        # Nothing to do
        pass

    def setFrameAppearance(self):
        self.frame.sTxtStep1.Enable()
        self.frame.txtCtrlMass.Enable()
        self.frame.txtCtrlMass.SetFocus()
        self.frame.sTxtStep2.Disable()
        self.frame.sTxtStep3.Disable()
        self.frame.gaugeStep3.Disable()
        self.frame.sTxtStep4.Disable()
        self.frame.sTxtStep5.Disable()
        self.frame.gaugeStep5.Disable()
        self.frame.sTxtStep6.Disable()
        self.frame.btnNext.Enable()