from abc import abstractmethod
import numpy as np
from math import *

import wx

import CalibrationWizardFrame
import pserial

class CalibrationControllerInterface:
    @abstractmethod
    def finishCalibration(self):
        pass

# Steps of calibration
STEP_REQUEST_CALIBRATION_MASS_VALUE = 1
STEP_REQUEST_LOADCELL_POSITIONING = 2
STEP_MEASURE_EMPTY_LOADCELL = 3
STEP_REQUEST_CALIBRATION_MASS_INSERTION = 4
STEP_MEASURE_CALIBRATION_MASS = 5
STEP_REQUEST_CALIBRATION_MASS_REMOTION = 6
STEP_CALCULATE_CALIBRATION_FACTOR = 7
STEP_FINISH_CALIBRATION = 8

class CalibrationWizardController(CalibrationWizardFrame.CalibrationWizardControllerInterface, pserial.wxPSerialObserverInterface):
    def __init__(self, parentController: CalibrationControllerInterface, parentFrame, serial: pserial.wxPSerial):
        self.parentController = parentController
        self.parentFrame = parentFrame
        self.calibrationWizardFrame = None
        self.serial = serial

    def start(self, calibrationMass: float = 1.0):
        self.step = STEP_REQUEST_CALIBRATION_MASS_VALUE
        self.calibrationMass = calibrationMass
        self.calibrationFactor = 0.0
        self.calibrationFactorVer = 0.0
        self.verCounter = 0
        self.calibrationFactorBkp = 0.0
        self.N = 100 # Number of measurements required for calibration
        self.forceSTD = 0.0
        self.force1 = np.array([]) 
        self.force2 = np.array([]) 
        self.tmpForce = np.array([])
        self.serial.addObserver(self)
        self.serial.sendMessage("g") # Asking Arduino for the current calibration factor
        self.calibrationWizardFrame = CalibrationWizardFrame.CalibrationWizardFrame(self.parentFrame, controller=self, m=calibrationMass)
        self.calibrationWizardFrame.Show()

    def isReady(self):
        if self.step == STEP_REQUEST_CALIBRATION_MASS_VALUE:
            # calibrationFactorBkp is initialized as 0. It is necessary
            # to get the calibrationFactor from Arduino before proceeding.
            return fabs(self.calibrationFactorBkp) > 0.0
        elif self.step == STEP_REQUEST_LOADCELL_POSITIONING:
            # During calibration, the calibrationFactor is set to 1.
            # It is necessary to ensure that before proceeding.
            return fabs(self.calibrationFactor) > 0.0
        elif self.step == STEP_MEASURE_EMPTY_LOADCELL:
            return len(self.force1) >= self.N
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_INSERTION:
            # If the current deviation is greater than 3 times the standard deviation, 
            # then the calibration mass is present
            return fabs(np.average(self.tmpForce)) > 3.0 * self.forceSTD + fabs(np.average(self.force1))
        elif self.step ==STEP_MEASURE_CALIBRATION_MASS:
            return len(self.force2) >= self.N
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_REMOTION:
            # If the current force deviation is less than 3 times the standard deviation, 
            # then the calibration mass is absent
            return fabs(np.average(self.tmpForce)) < 3.0 * self.forceSTD + fabs(np.average(self.force1))
        elif self.step == STEP_CALCULATE_CALIBRATION_FACTOR:
            return fabs(self.calibrationFactor-self.calibrationFactorVer) > 0.1
        else:
            return True

    def nextStep(self):
        if self.step == STEP_REQUEST_CALIBRATION_MASS_VALUE:
            if self.isReady():
                self.sendCalibrationFactor(1.0)
                self.calibrationMass = self.calibrationWizardFrame.getCalibrationMass()
                self.step = STEP_REQUEST_LOADCELL_POSITIONING
                self.calibrationWizardFrame.setStep2Appearance()
        elif self.step == STEP_REQUEST_LOADCELL_POSITIONING:
            if self.isReady():
                self.serial.sendMessage("g")
                self.step = STEP_MEASURE_EMPTY_LOADCELL
                self.calibrationWizardFrame.setStep3Appearance()
        elif self.step == STEP_MEASURE_EMPTY_LOADCELL:
            if self.isReady():
                self.step = STEP_REQUEST_CALIBRATION_MASS_INSERTION
                self.calibrationWizardFrame.setStep4Appearance(False)
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_INSERTION:
            if self.isReady():
                self.step = STEP_MEASURE_CALIBRATION_MASS
                self.calibrationWizardFrame.setStep5Appearance()
        elif self.step == STEP_MEASURE_CALIBRATION_MASS:
            if self.isReady():
                self.step = STEP_REQUEST_CALIBRATION_MASS_REMOTION
                self.calibrationWizardFrame.setStep6Appearance(False)
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_REMOTION:
            if self.isReady():
                self.step = STEP_CALCULATE_CALIBRATION_FACTOR
                dF = (np.average(self.force2)-np.average(self.force1))
                self.calibrationFactor = dF/self.calibrationMass
                self.sendCalibrationFactor(self.calibrationFactor)
                self.serial.sendMessage("g")
        elif self.step == STEP_CALCULATE_CALIBRATION_FACTOR:
            if self.isReady():
                self.step = STEP_FINISH_CALIBRATION
        elif self.step == STEP_FINISH_CALIBRATION:
            if self.isReady():
                self.close()
                dlg = wx.MessageDialog(self.parentFrame, "Calibração concluída com sucesso!", "Calibração")
                dlg.ShowModal()
        print(self.step)

    def close(self):
        if self.step != STEP_FINISH_CALIBRATION:
            self.sendCalibrationFactor(self.calibrationFactorBkp)
            dlg = wx.MessageDialog(self.parentFrame, "A calibração prévia foi reestabelecida.", "Calibração cancelada")
            dlg.ShowModal()
        self.serial.removeObserver(self)
        self.calibrationWizardFrame.Destroy()
        self.parentController.finishCalibration()

    def parseMessages(self, msgs: list):
        cfactor = []
        force = np.array([])
        for msg in msgs:
            data = msg.split(",")
            if data[0] == "1":
                force = np.append(force, float(data[2]))
            elif data[0] == "2":
                cfactor.append(float(data[1]))
        return [cfactor, force]

    def sendCalibrationFactor(self, factor):
        self.serial.sendMessage("s%.2f"%(factor))

    def wxPSerialUpdate(self, msgs: list):
        cfactor, force = self.parseMessages(msgs)
        if self.step == STEP_REQUEST_CALIBRATION_MASS_VALUE:
            if len(cfactor) == 0 and ( not self.isReady() ): 
                self.serial.sendMessage("g") # Asking Arduino for the current calibration factor
            else:
                self.calibrationFactorBkp = cfactor[-1]
        elif self.step == STEP_REQUEST_LOADCELL_POSITIONING:
            if len(cfactor) == 0 and ( not self.isReady() ): 
                self.serial.sendMessage("g") # Asking Arduino for the current calibration factor
            else:
                self.calibrationFactor = cfactor[-1]
        elif self.step == STEP_MEASURE_EMPTY_LOADCELL:
            self.force1 = np.append(self.force1,force)
            if len(self.force1) < self.N:
                p = int(float(len(self.force1))/self.N * 100.0)
                self.calibrationWizardFrame.setForce1Percentage(p)
            else:
                self.calibrationWizardFrame.setForce1Percentage(100)
                self.forceSTD = np.std(self.force1)
                self.nextStep()
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_INSERTION:
            self.tmpForce = np.append(self.tmpForce, force) 
            if self.isReady():
                self.calibrationWizardFrame.setStep4Appearance(True)
            else:
                self.calibrationWizardFrame.setStep4Appearance(False)
        elif self.step == STEP_MEASURE_CALIBRATION_MASS:
            self.force2 = np.append(self.force2,force)
            if len(self.force2) < self.N:
                p = int(float(len(self.force2))/self.N * 100.0)
                self.calibrationWizardFrame.setForce2Percentage(p)
            else:
                self.calibrationWizardFrame.setForce2Percentage(100)
                self.nextStep()
        elif self.step == STEP_REQUEST_CALIBRATION_MASS_REMOTION:
            self.tmpForce = force
            if self.isReady():
                self.calibrationWizardFrame.setStep6Appearance(True)
                self.nextStep()
            else:
                self.calibrationWizardFrame.setStep6Appearance(False)
        elif self.step == STEP_CALCULATE_CALIBRATION_FACTOR:
            if self.isReady():
                self.nextStep()
            else:
                if len(cfactor) == 0:
                    self.sendCalibrationFactor(self.calibrationFactor)
                else:
                    self.calibrationFactorVer = cfactor[-1]
                self.verCounter = self.verCounter + 1
                if self.verCounter > 5:
                    self.close()
                    dlg = wx.MessageDialog(self.parentFrame, "Falha na calibração!", "Calibração")
                    dlg.ShowModal()
