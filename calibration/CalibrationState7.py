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
