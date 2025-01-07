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
import wx

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationState1 import *

class CalibrationController(CalibrationControllerInterface):
    def __init__(self, parentController: CalibrationParentControllerInterface, parentFrame:wx.Frame):
        self.parentController = parentController
        self.parentFrame = parentFrame
        self.state = None
        self.calibrationMass = 1.0
        self.calibrationFactorBkp = 0.0
        self.N = 1000 # Number of measurements required for calibration
        self.force1 = np.array([]) 
        self.force2 = np.array([]) 

    def start(self, calibrationMass: float = 1.0):
        self.calibrationMass = calibrationMass
        self.calibrationFactorBkp = 0.0
        self.force1 = np.array([]) 
        self.force2 = np.array([]) 
        self.calibrationWizardFrame = CalibrationWizardFrame(self.parentFrame, controller=self, m=calibrationMass)
        self.calibrationWizardFrame.Show()
        self.setState(CalibrationState1(self, self.calibrationWizardFrame))

    def setState(self, state:CalibrationStateInterface):
        self.state = state
    
    def isReady(self):
        return self.state.isReady()
    
    def nextStep(self):
        self.state.nextStep()
    
    def close(self):
        self.state.close()
    
    def finishCalibration(self):
        self.calibrationWizardFrame.Destroy()
        self.parentController.finishCalibration()
    
    def updateCalibrationFactor(self, msgs: np.array):
        self.state.updateCalibrationFactor(msgs)

    def updateTimeAndForce(self, time:np.array, force:np.array):
        self.state.updateTimeAndForce(time, force)

    def sendCalibrationFactor(self, factor: float):
        self.parentController.sendCalibrationFactor(factor)
    
    def requestCalibrationFactor(self):
        self.parentController.requestCalibrationFactor()
    
    def setBackupCalibrationFactor(self, factor: float):
        self.calibrationFactorBkp = factor
    
    def getBackupCalibrationFactor(self) -> float:
        return self.calibrationFactorBkp
    
    def setCalibrationMass(self, mass: float):
        self.calibrationMass = mass
    
    def getCalibrationMass(self) -> float:
        return self.calibrationMass
    
    def getNumberOfSamples(self) -> int:
        return self.N
    
    def setForce1Vec(self, f1: np.array):
        self.force1 = f1
    
    def getForce1Vec(self) -> np.array:
        return self.force1
    
    def setForce2Vec(self, f2: np.array):
        self.force2 = f2
    
    def getForce2Vec(self) -> np.array:
        return self.force2
