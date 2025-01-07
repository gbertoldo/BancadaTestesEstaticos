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
from calibration.CalibrationState4 import *

"""
    State 3:
        - Measures empty load cell
 
 """
class CalibrationState3(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.force = np.array([])
        self.setFrameAppearance()
        
    def isReady(self):
        return self.force.size >= self.parent.getNumberOfSamples()

    def nextStep(self):
        if self.isReady():
            self.parent.setForce1Vec(self.force)
            self.parent.setState(CalibrationState4(self.parent,self.frame))

    def close(self):
        self.parent.setState(CalibrationStateAbort(self.parent,self.frame))

    def updateCalibrationFactor(self, msgs: list[float]):
        # Nothing to do
        pass

    def updateTimeAndForce(self, time:np.array, force:np.array):
        self.force = np.append(self.force, force)
        p = int(100.0 * self.force.size / self.parent.getNumberOfSamples())
        if p > 100:
            p = 100
        self.frame.gaugeStep3.SetValue(p)
        self.nextStep()

    def setFrameAppearance(self):
        self.frame.sTxtStep1.Enable()
        self.frame.txtCtrlMass.Disable()
        self.frame.sTxtStep2.Enable()
        self.frame.sTxtStep3.Enable()
        self.frame.gaugeStep3.Enable()
        self.frame.sTxtStep4.Disable()
        self.frame.sTxtStep5.Disable()
        self.frame.gaugeStep5.Disable()
        self.frame.sTxtStep6.Disable()
        self.frame.btnNext.Disable()