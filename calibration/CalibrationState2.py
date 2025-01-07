from math import *

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationState3 import *
from calibration.CalibrationStateAbort import *

"""
    State 2:
      - Sends the unitary calibration factor to MCU, and 
      - Requests the correct positioning of the load cell.
"""
class CalibrationState2(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.calibrationFactor = 0.0
        self.parent.sendCalibrationFactor(1.0)
        self.parent.requestCalibrationFactor()
        self.setFrameAppearance()

    def isReady(self):
        return ( fabs(self.calibrationFactor-1.0) < 1E-3 ) 

    def nextStep(self):
        if self.isReady():
            self.parent.setState(CalibrationState3(self.parent,self.frame))
        else:
            self.parent.sendCalibrationFactor(1.0)
            self.parent.requestCalibrationFactor()

    def close(self):
        self.parent.setState(CalibrationStateAbort(self.parent,self.frame))

    def updateCalibrationFactor(self, msgs: list[float]):
        self.calibrationFactor = msgs[-1]

    def updateTimeAndForce(self, time:np.array, force:np.array):
        # Nothing to do
        pass

    def setFrameAppearance(self):
        self.frame.sTxtStep1.Enable()
        self.frame.txtCtrlMass.Disable()
        self.frame.sTxtStep2.Enable()
        self.frame.sTxtStep3.Disable()
        self.frame.gaugeStep3.Disable()
        self.frame.sTxtStep4.Disable()
        self.frame.sTxtStep5.Disable()
        self.frame.gaugeStep5.Disable()
        self.frame.sTxtStep6.Disable()
        self.frame.btnNext.Enable()
