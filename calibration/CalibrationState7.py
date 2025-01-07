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
from math import *
import numpy as np

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationStateAbort import *

"""
    State 7:
        - Calculates the calibration factor 
 """
class CalibrationState7(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        f1=np.average(self.parent.getForce1Vec())
        f2=np.average(self.parent.getForce2Vec())
        self.calibrationFactor = (f2-f1)/self.parent.getCalibrationMass()
        self.parent.sendCalibrationFactor(self.calibrationFactor)
        self.parent.requestCalibrationFactor()
        self.calibrationFactorVerificator = 0.0
        self.setFrameAppearance()
        
    def isReady(self):
        if fabs(self.calibrationFactorVerificator) > 0.0:
            return fabs(self.calibrationFactor/self.calibrationFactorVerificator-1) < 0.01
        else:
            return False
    def nextStep(self):
        if self.isReady():
            self.parent.finishCalibration()
        else:
            self.parent.sendCalibrationFactor(self.calibrationFactor)
            self.parent.requestCalibrationFactor()

    def close(self):
        self.parent.setState(CalibrationStateAbort(self.parent, self.frame))

    def updateCalibrationFactor(self, msgs: list[float]):
        self.calibrationFactorVerificator = msgs[-1]
        self.nextStep()

    def updateTimeAndForce(self, time:np.array, force:np.array):
        self.nextStep()

    def setFrameAppearance(self):
        self.frame.sTxtStep1.Enable()
        self.frame.txtCtrlMass.Disable()
        self.frame.sTxtStep2.Enable()
        self.frame.sTxtStep3.Enable()
        self.frame.gaugeStep3.Enable()
        self.frame.sTxtStep4.Enable()
        self.frame.sTxtStep5.Enable()
        self.frame.gaugeStep5.Enable()
        self.frame.sTxtStep6.Enable()
        self.frame.btnNext.SetLabel("Concluir")
        self.frame.btnNext.Enable()
