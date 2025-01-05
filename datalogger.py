import numpy as np
import os.path

def filterLastNPoints(N, data):
    return [data[0][-N:-1],data[1][-N:-1]]

def filterUniformlyDistributedPoints(N, data):
    sz = len(data[0])
    if sz > N:
        rfactor = int(sz / N)
        return [data[0][::rfactor],data[1][::rfactor]]
    else:
        return data
    
class DataloggerParameters:
    def __init__(self):
        self.localG = 9.80665
        self.listOfUnits = [{"label":"N",   "factor":1.0},
                            {"label":"kgf", "factor":1.0/9.80665},
                            {"label":"gf",  "factor":1000.0/9.80665}]
        self.selectedUnit = 0    

class Datalogger:
    def __init__(self, parameters: DataloggerParameters):
        self.t = np.array([])
        self.f = np.array([])
        self.t0 = 0.0
        self.f0 = 0.0
        self.outputFileName = ""
        self.numberOfLinesWritten = 0
        self.parameters = parameters
        pass

    def setParameters(self, p:DataloggerParameters):
        self.parameters = p

    def getParameters(self):
        return self.parameters

    def append(self, t: np.array, f: np.array):
        self.t = np.append(self.t,t)
        self.f = np.append(self.f,f)

    def setLocalG(self, g: float):
        self.parameters.localG = g

    def setUnitN(self):
        self.parameters.selectedUnit = 0

    def setUnitkgf(self):
        self.parameters.selectedUnit = 1

    def setUnitgf(self):
        self.parameters.selectedUnit = 2

    def shiftT(self, t0):
        self.t0 = t0

    def shiftF(self, f0):
        self.f0 = f0

    def clear(self):
        if len(self.t) > 0:
            self.shiftT(self.t[-1])
        else:
            self.shiftT(0.0)
        self.t = np.array([])
        self.f = np.array([])

    def tare(self):
        if len(self.t) > 0:
            if len(self.t) > 10:
                self.shiftF(np.average(self.f[-10:-1]))
            else:
                self.shiftF(self.f[-1])
    
    def getUnit(self):
        return self.parameters.listOfUnits[self.parameters.selectedUnit]
    
    def getData(self):
        kgToSelectedUnit = self.parameters.localG*self.getUnit()["factor"]
        return [self.t-self.t0,(self.f-self.f0)*kgToSelectedUnit]

    def writeData(self, filename: str):
        if os.path.isfile(filename):
            with open(filename, 'a',encoding='utf-8') as file:
                [t,f] = self.getData()
                for i in range(self.numberOfLinesWritten,len(t)):
                    file.write("%14.7f %14.7f\n"%(t[i],f[i]))
                self.numberOfLinesWritten = len(t)

        else:
            with open(filename, 'w',encoding='utf-8') as file:
                file.write("# g local = %14.7f m/s2\n"%(self.parameters.localG))
                title = "# tempo (s)  força ("+self.getUnit()["label"]+")\n"
                file.write(title)
                [t,f] = self.getData()
                for i in range(0,len(t)):
                    file.write("%14.7f %14.7f\n"%(t[i],f[i]))
                self.numberOfLinesWritten = len(t)
    
if __name__ == "__main__":
    dl = Datalogger()
    N=35
    ofile = "dl.txt"
    if os.path.isfile(ofile):
        os.remove(ofile)
                      
    for i in range(1,N):
        dl.append(np.array([i]),np.array([i]))
        if (i%10==0):
            dl.writeData(ofile)
    dl.writeData(ofile)
    with open(ofile, 'r',encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(1,len(lines)):
        fields = lines[i].split()
        if int(float(fields[0])) - i != 0:
            print("Error t")
        if int(float(fields[1])/9.80665) - i != 0:
            print("Error f")
        