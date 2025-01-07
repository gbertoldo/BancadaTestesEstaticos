from math import *

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationStateAbort import *
from calibration.CalibrationState7 import *

"""
    State 6:
        - Request calibration mass remotion
 """
class CalibrationState6(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.f1avg = np.average(self.parent.getForce1Vec())
        self.f1std = np.std(self.parent.getForce1Vec())
        self.force = np.array([])
        self.setFrameAppearance()

    def isReady(self):
        return fabs(np.average(self.force)-self.f1avg) < 3.0 * self.f1std

    def nextStep(self):
        if self.isReady():
            self.parent.setState(CalibrationState7(self.parent, self.frame))

    def close(self):
        self.parent.setState(CalibrationStateAbort(self.parent, self.frame))

    def updateCalibrationFactor(self, msgs: list[float]):
        # Nothing to do
        pass

    def updateTimeAndForce(self, time:np.array, force:np.array):
        self.force = force
        if self.isReady():
            self.frame.btnNext.Enable()

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
        self.frame.btnNext.Disable()