from math import *

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *

"""
    State Abort:
        - Aborts the calibration process
 """
class CalibrationStateAbort(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.calibractionFactorBkpVerificator = 0.0
        self.parent.sendCalibrationFactor(self.parent.getBackupCalibrationFactor())
        self.parent.requestCalibrationFactor()
        
    def isReady(self):
        print(self.calibractionFactorBkpVerificator,self.parent.getBackupCalibrationFactor())
        if fabs(self.calibractionFactorBkpVerificator) > 0.0:
            return fabs(self.calibractionFactorBkpVerificator/self.parent.getBackupCalibrationFactor()-1.0) < 0.01
        else:
            return False
    
    def nextStep(self):
        if self.isReady():
            self.parent.finishCalibration()
        else:
            self.parent.sendCalibrationFactor(self.parent.getBackupCalibrationFactor())
            self.parent.requestCalibrationFactor()

    def close(self):
        pass

    def updateCalibrationFactor(self, msgs: list[float]):
        self.calibractionFactorBkpVerificator = msgs[-1]
        self.nextStep()

    def updateTimeAndForce(self, time:np.array, force:np.array):
        self.nextStep()

    def setFrameAppearance(self):
        self.frame.sTxtStep1.Disable()
        self.frame.txtCtrlMass.Disable()
        self.frame.sTxtStep2.Disable()
        self.frame.sTxtStep3.Disable()
        self.frame.gaugeStep3.Disable()
        self.frame.sTxtStep4.Disable()
        self.frame.sTxtStep5.Disable()
        self.frame.gaugeStep5.Disable()
        self.frame.sTxtStep6.Disable()
        self.frame.btnNext.Enable()
