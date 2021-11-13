import os
from sys import platform
import numpy as np
import readline

class CreateControlModelIndex:
    
    def __init__(self):
        self.strOutput = ''
    
    @property
    def nx(self):
        return self._nx
    
    @nx.setter
    def nx(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
        else:
            self._nx = value

    @property
    def ny(self):
        return self._ny
    
    @ny.setter
    def ny(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
        else:
            self._ny = value
    
    @property
    def nz(self):
        return self._nz
    
    @nz.setter
    def nz(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
        else:
            self._nz = value
    
    @property
    def layerRangeList(self):
        return self._layerRangeList
    
    @layerRangeList.setter
    def layerRangeList(self, value):
        self._layerRangeList = value
    
    @property
    def indexFormatList(self):
        return self._indexFormatList
    
    @indexFormatList.setter
    def indexFormatList(self, value):
        self._indexFormatList = value
    
    def createIndexFormatLayerStr(self):
        outStr = ''
        for iLayerRange, layerRange in enumerate (self.layerRangeList):
            for iValLayer, valLayer in  enumerate (layerRange):
                trueiLayerRange = iLayerRange+1
                trueiValLayer = iValLayer+1
                outStr += str(valLayer)
                if trueiValLayer == len(layerRange):
                    outStr += '\n'
                else:
                    outStr += ' '
            indexFormatArr = np.zeros([self.nx, self.ny], dtype=int)
            indexFormatArr[:] = self.indexFormatList[iLayerRange]
            for iRowArr, rowArr in enumerate(indexFormatArr):
                for iValArr, valArr in enumerate (rowArr):
                    strValArr = str(valArr)
                    outStr += strValArr
                    trueiRowArr = iRowArr+1
                    trueiValArr = iValArr+1
                    
                    if trueiLayerRange==len(self.layerRangeList) and \
                       trueiRowArr==len(indexFormatArr) and \
                       trueiValArr == len(rowArr):
                        pass
                    elif trueiValArr == len(rowArr):
                        outStr += '\n'
                    else:
                        outStr += ' '
        return outStr
    
    def createOutputStr(self):
        self.strOutput += "{} {} {}\n".format(self.nx, self.ny, self.nz)
        self.strOutput += self.createIndexFormatLayerStr()
        
    def save(self, outputFile):
        self.outFileName = outputFile
        with open(outputFile, 'w') as f:
            f.write(self.strOutput)
        f.close()

# Class for CLI
class controlModelIndexCLI():
    
    def __init__(self):
        self.myCMI = CreateControlModelIndex()
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")    
        self.basePath = os.getcwd()
        readline.parse_and_bind("tab:complete")

    def displayHeader(self):
        print("####################################################################")
        print("                       MT DATA PREPROCESSING                        ")
        print("                        CONTROL MODEL INDEX                         ")
        print("####################################################################")
        print("{0:17s}: {1}".format("BASE PATH", self.basePath))
        print("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print("####################################################################")
    
    def getInput(self):
        userInput = input(">> ")
        userInputLower = userInput.lower()
        if userInputLower == "exit":
            print("Program closed")
            exit()
        else:
            return userInput
    
    def getInputBlockNumber(self):
        while(True):
            inputBlockNumber = self.getInput()
            try:
                blockNumber = int(inputBlockNumber)
            except:
                print("invalid input")
            else:
                return blockNumber
            
    def getBlockNumber(self):
        print()
        print("Number of block x")
        self.myCMI.nx = self.getInputBlockNumber()
        
        print("Number of block y")
        self.myCMI.ny = self.getInputBlockNumber()
        
        print("Number of block z")
        self.myCMI.nz = self.getInputBlockNumber()
        
    def getIndexFormat(self):
        print()
        print("Index format (layer 1 - {})".format(self.myCMI.nz))
        layerStart = 1
        layerEndFlag = True
        layerRange = []
        indexFormatList = []
          
        while(True):
            layerRangeTemp = [layerStart]
            if layerStart == self.myCMI.nz:
                print("Layer range: {}".format(layerStart))
                layerEndFlag = False
            else:
                print("Layer range: {}".format(layerStart), end=' ')
            if layerEndFlag:
                print("to layer:")
                while(True):
                    inputLayerEnd = self.getInput()
                    inputLayerEndLower = inputLayerEnd.lower()
                    if inputLayerEndLower == "last":
                        inputLayerEnd = self.myCMI.nz
                    elif inputLayerEndLower == '':
                        inputLayerEnd = layerStart
                    try:
                        layerEnd = int(inputLayerEnd)
                    except:
                        print("invalid input")
                    else:
                        if layerEnd > self.myCMI.nz:
                            print("invalid input: layer cannot greater than {}".format(self.myCMI.nz))
                        elif layerEnd < layerStart:
                            print("invalid input: layer cannot less than {}".format(layerStart))
                        else:       
                            if layerEnd == self.myCMI.nz:
                                layerRangeTemp.append(layerEnd)
                                layerEndFlag = False
                            elif layerEnd == layerStart:
                                layerStart = layerEnd + 1
                            else:
                                layerRangeTemp.append(layerEnd)
                                layerStart = layerEnd + 1
                            break
            print("Index format ('0':free to change/'1':fixed)")
            while(True):
                try:
                    inputIndexFormat = int(self.getInput())
                except:
                    print("invalid input")
                else:
                    indexFormatList.append(inputIndexFormat)
                    break
            layerRange.append(layerRangeTemp)
            if not layerEndFlag:
                break
        self.myCMI.layerRangeList = layerRange
        self.myCMI.indexFormatList = indexFormatList
    
    def fileProcess(self):
        self.myCMI.createOutputStr()
    
    def fileSave(self):
        print ()
        while True:
            print ("Output file")
            outputFile = self.getInput()
            forceSave = False
            if os.path.isfile(outputFile) and not forceSave:
                validChoice = False
                while not validChoice:
                    print ("File already exist. Replace file? (y/n)")
                    replaceChosen = self.getInput()
                    replaceChosenLower = replaceChosen.lower()
                    if replaceChosenLower == 'y':
                        validChoice = True
                        forceSave = True
                    elif replaceChosenLower == 'n':
                        validChoice = True
                    else:
                        print ("Invalid input")
                        continue
            if not os.path.isfile(outputFile) or forceSave:
                try:
                    self.myCMI.save(outputFile)
                    print ("success..")
                except OSError as err:
                    print (err)
                    continue
                else:
                    break
                    
    def displayResult(self):
        print()
        print("####################################################################")
        print("                             RESULT                                 ")
        print("####################################################################")
        print()
        print("Number of block x: {}".format(self.myCMI.nx))
        print("Number of block y: {}".format(self.myCMI.ny))
        print("Number of block z: {}".format(self.myCMI.nz))
        print()
        maxCharL = 0
        for layerRange in self.myCMI.layerRangeList:
            maxCharLayerRange = 0
            for layer in layerRange:
                nStrLayer = len(str(layer))
                maxCharLayerRange += nStrLayer
            if maxCharLayerRange > maxCharL:
                maxCharL = maxCharLayerRange
        maxCharL += 3
        maxCharI = 0
        for indexVal in self.myCMI.indexFormatList:
            nStrIndex = len(str(indexVal))
            if nStrIndex > maxCharI:
                maxCharI = nStrIndex
        strHeaderLayer = "Layer"
        strHeaderIndex = "Index format"
        if maxCharL < len(strHeaderLayer)+1:
            maxCharL = len(strHeaderLayer)+1
        print("{:{}s}".format(strHeaderLayer, maxCharL), end=' ')
        print("{:{}s}".format(strHeaderIndex, maxCharI))
        for iLayerRange, layerRange in enumerate(self.myCMI.layerRangeList):
            if len(layerRange)==1:
                strLayerRange = "{}".format(layerRange[0])
            elif len(layerRange)==2:
                strLayerRange = "{}-{}".format(layerRange[0], layerRange[1])
            strIndexVal = str(self.myCMI.indexFormatList[iLayerRange])
            print("{:{}s}".format(strLayerRange, maxCharL), end=' ')
            print("{:{}s}".format(strIndexVal, maxCharI))
        print()
        print("Output filename: {}".format(self.myCMI.outFileName))
        print("####################################################################")

def main():
    myCMIUI = controlModelIndexCLI()
    myCMIUI.displayHeader()
    myCMIUI.getBlockNumber()
    myCMIUI.getIndexFormat()
    myCMIUI.fileProcess()
    myCMIUI.fileSave()
    myCMIUI.displayResult()

if __name__ == "__main__":
    main()
