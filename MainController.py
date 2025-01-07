import wx
import serial
import numpy as np
import time
from datetime import datetime
import pickle
import os.path

import pserial
import MainFrame
import datalogger
import ChangeGDialog
from calibration import CalibrationController
from calibration import CalibrationAbstraction

# Possible states
READY=1
DISCONNECTED=2
CALIBRATING=3
RECORDING=4
CONNECTING=5

class MainControllerParameters:
    def __init__(self):
        self.m = 1.0      # standard calibration mass [kg]
        self.mainFrameParameters = MainFrame.MainFrameParameters()
        self.dataloggerParameters = datalogger.DataloggerParameters()

class MainController(MainFrame.MainFrameControllerInterface, 
                     pserial.wxPSerialObserverInterface, 
                     ChangeGDialog.ChangeGControllerInterface, 
                     CalibrationAbstraction.CalibrationParentControllerInterface):
    def __init__(self):
        # Serial connection
        self.ser = None
        self.configFilename = "config.cfg"
        self.state = DISCONNECTED
        self.maxPlotPoints = 500
        self.outputFileName = ""
        self.notificationPeriod = 200 # ms
        self.isBusy = False
        self.listOfMsgs = []
        self.finishCalibrationFlag = False
        self.finishCalibrationCounter = 0
        self.parameters = self.loadParameters()
        self.datalogger = datalogger.Datalogger(self.parameters.dataloggerParameters)
        self.parameters.mainFrameParameters.par["listofports"] = self.getAvailableSerialPorts()
        self.parameters.mainFrameParameters.par["selectedUnit"] = self.parameters.mainFrameParameters.par["listOfUnits"][self.parameters.dataloggerParameters.selectedUnit]
        self.parameters.mainFrameParameters.par["g"] = self.parameters.dataloggerParameters.localG
        print(self.parameters.mainFrameParameters.par["selectedUnit"])
        print(self.parameters.mainFrameParameters.par["g"])
 
    def saveParameters(self, p: MainControllerParameters):
        with open(self.configFilename, 'wb') as handle:
           pickle.dump(p, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadParameters(self):
        p = MainControllerParameters()
        if ( os.path.isfile(self.configFilename) ):
            with open(self.configFilename, 'rb') as handle:
                p = pickle.load(handle)
        else:
            self.saveParameters(p)
        return p

    def setState(self, st):
        if st != self.state:
            self.state = st
            if st == READY:
                self.mainFrame.setConnectedAppearance()
            elif st == DISCONNECTED:
                self.mainFrame.setDisconnectedAppearance()
            elif st == CALIBRATING:
                self.mainFrame.setCalibratingAppearance()
            elif st == RECORDING:
                self.mainFrame.setRecordingAppearance(self.outputFileName)
            elif st == CONNECTING:
                self.mainFrame.setConnectingAppearance()

    def startApplication(self):
        self.app = wx.App()
        self.mainFrame = MainFrame.MainFrame(None, self, self.parameters.mainFrameParameters)
        #self.mainFrame.SetIcon(wx.Icon(MainFrame.resource_path("./fig/icon.png")))
        self.mainFrame.Maximize(True)
        self.mainFrame.Show()
        self.app.MainLoop()

    def getAvailableSerialPorts(self):
        # Getting the available ports
        commList = serial.tools.list_ports.comports()
        portList = []
        for item in commList:
            portList.append(item.device)
        return portList
    
    def connectToSerial(self, port: str):
        self.ser = pserial.wxPSerial(self.mainFrame, notificationPeriod=self.notificationPeriod, port=port, baudrate=115200)
        self.ser.addObserver(self)
        self.ser.start()
        if self.ser.is_open():
            self.setState(CONNECTING)
        else:
            self.ser = None
            self.setState(DISCONNECTED)

    def startCalibration(self):
        self.calibrationController = CalibrationController.CalibrationController(self, self.mainFrame)
        self.calibrationController.start(self.parameters.m)
        self.setState(CALIBRATING)

    def finishCalibration(self):
        self.parameters.m = self.calibrationController.getCalibrationMass()
        self.saveParameters(self.parameters)
        self.finishCalibrationFlag = True
        self.finishCalibrationCounter = 0
        self.setState(READY)

    def sendCalibrationFactor(self, factor: float):
        self.ser.sendMessage("s%.2f"%(factor))
    
    def requestCalibrationFactor(self):
        self.ser.sendMessage("g") # Asking Arduino for the current calibration factor

    def changeG(self):
        dlg = ChangeGDialog.ChangeGDialog(self.mainFrame, self, self.parameters.mainFrameParameters.par["g"])
        dlg.ShowModal()
        
    def setLocalG(self, g: float):
        self.parameters.mainFrameParameters.par["g"] = g
        self.datalogger.setLocalG(g)
        self.parameters.dataloggerParameters = self.datalogger.getParameters()
        self.saveParameters(self.parameters)
        self.mainFrame.setLocalG(g)

    def clearData(self):
        self.listOfMsgs.clear()
        self.datalogger.clear()
        
    def startRecording(self):
        now = datetime.now()
        self.outputFileName = now.strftime("log_%Y_%m_%d__%Hh_%Mmin_%Ss.txt")
        self.setState(RECORDING)

    def stopRecording(self):
        self.datalogger.writeData(self.outputFileName)
        self.setState(READY)
    
    def tare(self):
        self.datalogger.tare()

    def setForceUnit(self, opt: int):
        self.parameters.mainFrameParameters.par["selectedUnit"] = opt
        if opt == 1:
            self.datalogger.setUnitkgf()
            self.mainFrame.setSelectedUnit("kgf")
        elif opt == 2:
            self.datalogger.setUnitgf()        
            self.mainFrame.setSelectedUnit("gf")
        else:
            self.datalogger.setUnitN()
            self.mainFrame.setSelectedUnit("newton")
        self.parameters.dataloggerParameters = self.datalogger.getParameters()
        self.saveParameters(self.parameters)

    def setGraphOption(self, opt: int):
        self.parameters.mainFrameParameters.par["selectedGraphOpt"] = self.parameters.mainFrameParameters.par["listOfGraphOpt"][opt]
        self.saveParameters(self.parameters)

    def parseMessages(self, msgs: list):
        atime  = np.array([])
        aforce = np.array([])
        afactor = np.array([])
        N = len(msgs)
        for i in range(0,N):
          msg = msgs.pop(0)
          data = msg.split(",")
          if data[0] == "1":
            atime  = np.append(atime,  float(data[1]))
            aforce = np.append(aforce, float(data[2]))
          if data[0] == "2":
            afactor = np.append(afactor, float(data[1]))
        return [atime, aforce, afactor]
    
    def processMessages(self, msgs):
        if self.state == CONNECTING:
            self.setState(READY)

        [t,f,factor] = self.parseMessages(msgs)

        if self.state == CALIBRATING:
            if t.size > 0:
                self.calibrationController.updateTimeAndForce(t, f)
            if factor.size > 0:
                self.calibrationController.updateCalibrationFactor(factor)

        elif self.state == READY or self.state == RECORDING:
            if ( t.size > 0 ):
                self.datalogger.append(t, f)

            if self.state == RECORDING:
                self.datalogger.writeData(self.outputFileName)

            [t,f] = self.datalogger.getData()
            self.mainFrame.setForceInfo(f[-1],np.max(f),len(t))

            if self.finishCalibrationFlag:
                self.tare()
                self.clearData()
                self.finishCalibrationCounter = self.finishCalibrationCounter + 1
                if self.finishCalibrationCounter > 1:
                    self.finishCalibrationFlag = False
            
            if self.parameters.mainFrameParameters.par["selectedGraphOpt"] == "complete":
                [t,f] = datalogger.filterUniformlyDistributedPoints(self.maxPlotPoints,[t,f])
                self.mainFrame.replot(t,f)
            if self.parameters.mainFrameParameters.par["selectedGraphOpt"] == "slide":
                [t,f] = datalogger.filterLastNPoints(self.maxPlotPoints,[t,f])
                self.mainFrame.replot(t,f)

    def wxPSerialUpdate(self, msgs: list):
        if len(msgs) > 0: 
            self.listOfMsgs = self.listOfMsgs + msgs
            if not self.isBusy:
                self.isBusy = True
                #t1 = datetime.now()
                self.processMessages(self.listOfMsgs)
                #t2 = datetime.now()
                #print((t2-t1).microseconds*0.001)
                self.isBusy = False
