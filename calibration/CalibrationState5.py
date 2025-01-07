from math import *

from calibration.CalibrationAbstraction import *
from calibration.CalibrationWizardFrame import *
from calibration.CalibrationStateAbort import *
from calibration.CalibrationState6 import *

"""
    State 5:
        - Measures calibration mass
 """
class CalibrationState5(CalibrationStateInterface):
    def __init__(self, parent: CalibrationControllerInterface, frame: CalibrationWizardFrame):
        self.parent = parent
        self.frame = frame
        self.force = np.array([])
        self.setFrameAppearance()
        
    def isReady(self):
        return self.force.size >= self.parent.getNumberOfSamples()

    def nextStep(self):
        if self.isReady():
            self.parent.setForce2Vec(self.force)
            self.parent.setState(CalibrationState6(self.parent,self.frame))

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
        self.frame.gaugeStep5.SetValue(p)
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
        self.frame.sTxtStep6.Disable()
        self.frame.btnNext.Disable()