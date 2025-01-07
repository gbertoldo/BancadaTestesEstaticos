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

import abstractmethod

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
