from abc import abstractmethod

import numpy as np

class CalibrationParentControllerInterface:
    @abstractmethod
    def sendCalibrationFactor(self, factor: float):
        pass
    @abstractmethod
    def requestCalibrationFactor(self):
        pass
    @abstractmethod
    def finishCalibration(self):
        pass
    
class CalibrationStateInterface:
    @abstractmethod
    def isReady(self):
        pass
    @abstractmethod
    def nextStep(self):
        pass
    @abstractmethod
    def close(self):
        pass
    @abstractmethod
    def updateCalibrationFactor(self, msgs: list[float]):
        pass
    @abstractmethod
    def updateTimeAndForce(self, time:np.array, force:np.array):
        pass

class CalibrationControllerInterface:
    @abstractmethod
    def setState(self, state:CalibrationStateInterface):
        pass
    @abstractmethod
    def isReady(self):
        pass
    @abstractmethod
    def nextStep(self):
        pass
    @abstractmethod
    def close(self):
        pass
    @abstractmethod
    def finishCalibration(self):
        pass
    @abstractmethod
    def updateCalibrationFactor(self, msgs: np.array):
        pass
    @abstractmethod
    def updateTimeAndForce(self, time:np.array, force:np.array):
        pass
    @abstractmethod
    def sendCalibrationFactor(self, factor: float):
        pass
    @abstractmethod
    def requestCalibrationFactor(self):
        pass
    @abstractmethod
    def setBackupCalibrationFactor(self, factor: float):
        pass
    @abstractmethod
    def getBackupCalibrationFactor(self) -> float:
        pass
    @abstractmethod
    def setCalibrationMass(self, mass: float):
        pass
    @abstractmethod
    def getCalibrationMass(self) -> float:
        pass
    @abstractmethod
    def getNumberOfSamples(self) -> int:
        pass
    @abstractmethod
    def setForce1Vec(self, f1: np.array):
        pass
    @abstractmethod
    def getForce1Vec(self) -> np.array:
        pass
    @abstractmethod
    def setForce2Vec(self, f2: np.array):
        pass
    @abstractmethod
    def getForce2Vec(self) -> np.array:
        pass
