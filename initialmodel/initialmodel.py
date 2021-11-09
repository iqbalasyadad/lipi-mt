import os
from sys import platform
import numpy as np
import readline

class CreateInitialModel:
    
    def __init__(self):
        self.blockColX = "src-x"
        self.blockColY = "src-y"
        self.blockColZ = "src-z"
        self.strOutput = ''
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = "# {}".format(value)
    
    @property
    def nx(self):
        return self._nx
    
    @nx.setter
    def nx(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
        elif value%2 != 0:
            raise ValueError("value is not an even number")
        else:
            self._nx = value
    
    @property
    def ny(self):
        return self._ny
    
    @ny.setter
    def ny(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
        elif value%2 !=0:
            raise ValueError("value is not an even number")
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
    def nr(self):
        return self._nr
    
    @nr.setter
    def nr(self, value):
        if value > 9:
            raise ValueError("nr cannot greater than 9")
        else:
            self._nr = value
    
    @property
    def blockSizeX(self):
        return self._blockSizeX
    
    @blockSizeX.setter
    def blockSizeX(self, value):
        self._blockSizeX = np.array(value)
        self.nx = len(value)
    
    @property
    def blockSizeY(self):
        return self._blockSizeY
    
    @blockSizeY.setter
    def blockSizeY(self, value):
        self._blockSizeY = np.array(value)
        self.ny = len(value)

    @property
    def blockSizeZ(self):
        return self._blockSizeZ
    
    @blockSizeZ.setter
    def blockSizeZ(self, value):
        self._blockSizeZ = np.array(value)
        self.nz = len(value)
    
    def mirrorBlock(self, value):
        return value[::-1]  # block with reversed value
    
    def createBlockXY(self, mode='auto', side1=None, side2=None):
        if mode == "auto":
            side2 = side1
            side1 = self.mirrorBlock(side1)
        elif mode == "manual":
            side1 = self.mirrorBlock(side1)
        else:
            raise ValueError("invalid mode")
        return side1 + side2
            
    @property
    def resistivityValue(self):
        return self._resistivityValue
    
    @resistivityValue.setter
    def resistivityValue(self, value):
        if len(value) != self._nr:
            raise ValueError ("invalid number of resistivity")
        else:
            self._resistivityValue = np.array(value)
            
    @property
    def resistivityIndex(self):
        return self._resistivityIndex 
    
    @resistivityIndex.setter
    def resistivityIndex(self, value):
        self._resistivityIndex = np.array(value)
                    
    @property
    def resistivityIndexLayer(self):
        return self._resistivityIndexLayer
    
    @resistivityIndexLayer.setter
    def resistivityIndexLayer(self, value):
        self._resistivityIndexLayer = value
    
    def createOutputBlock(self, blockVal, col="inf"):
        nBlockVal = len(blockVal)
        strBlock = ''
        if col == "inf":
            for iVal,val in enumerate(blockVal):
                strBlock += ("{:.0f}".format(val))
                if iVal < nBlockVal-1:
                    strBlock += ' '
                    
        else:
            # calc max char in blockVal
            maxChar = 0
            for val in blockVal:
                strVal = str(val)
                strVal = strVal.split('.')[0]+'.'

                nCharVal = len(strVal)
                if nCharVal > maxChar:
                    maxChar = nCharVal
                    
            valSpacing = maxChar+1
            
            if col=="src-x" or col=="src-y":
                edgeCol = 5
                centerCol = 9
                rangeStart = 0
                rangeEnd = edgeCol

                for iVal, val in enumerate(blockVal):
                    trueIndex = iVal+1
                    strVal = "{:{}.1f}".format(val, valSpacing)
                    strVal = strVal.split('.')[0]+'.'
                    
                    strBlock += strVal

                    if trueIndex == rangeEnd and trueIndex != nBlockVal:
                        strBlock += '\n'
                        rangeEnd += centerCol
                    else:
                        strBlock += ' '
                        
            elif col=="src-z":
                for iEl, el in enumerate(self.resistivityIndexLayer):
                    nEl = len(el)
                    if nEl == 1:
                        trueIndexList = [el[0]]
                    elif nEl == 2:
                        trueIndexList = np.arange(el[0], el[1]+1)

                    for trueIndex in trueIndexList:
                        val = self.blockSizeZ[trueIndex-1]
                        strVal = "{:{}.1f}".format(val, valSpacing)
                        strVal = strVal.split('.')[0]+'.'
                        strBlock += strVal 
                        trueiEl = iEl+1
                        if trueiEl == len(self.resistivityIndexLayer) and trueIndex == el[-1]:
                            pass
                        elif trueIndex == el[-1]:
                            strBlock += '\n'
                        else:
                            strBlock += ' '
                
            else:
                for iVal, val in enumerate(blockVal):
                    trueIndexVal = iVal+1
                    strVal = "{:{}.1f}".format(val, valSpacing)
                    strVal = strVal.split('.')[0]+'.'
                    strBlock += strVal
                    
                    if trueIndexVal%col==0 and trueIndexVal != nBlockVal:
                        strBlock += '\n'
                    else:
                        strBlock += ' '
        return strBlock
    
    def createResistivityValStr(self):
        strOut = ''
        for iVal, val in enumerate (self.resistivityValue):
            strVal = str(val)
            strVal = strVal.split('.')[0]+'.'
            strOut += strVal
            
            trueIndexVal = iVal + 1
            
            if trueIndexVal != len(self.resistivityValue):
                strOut += ' '
            
        return strOut
    
    def createResistivityIndexStr(self):
        outStr = ''
        for iLayerList, layerList in enumerate (self.resistivityIndexLayer):
            for iValLayer, valLayer in  enumerate (layerList):
                
                trueiLayerList = iLayerList+1
                trueiValLayer = iValLayer+1
                
                outStr += str(valLayer)

                if trueiValLayer == len(layerList):
                    outStr += '\n'
                else:
                    outStr += ' '
            
            # data in layer
            resistivityIndexForLayerArr = np.zeros([self.nx, self.ny], dtype=int)
            resistivityIndexForLayerArr[:] = self.resistivityIndex[iLayerList]
                        
            for irow, row in enumerate(resistivityIndexForLayerArr):
                for iVal, val in enumerate (row):
                    strVal = str(val)
                    outStr += strVal
                    
                    trueirow = irow+1
                    trueiVal = iVal+1
                    
                    if trueiLayerList==len(self.resistivityIndexLayer) and \
                       trueirow==len(resistivityIndexForLayerArr) and \
                       trueiVal == len(row):
                        pass
                    elif trueiVal == len(row):
                        outStr += '\n'
                    else:
                        outStr += ' '
        return outStr
    
    def createOutput(self):
        # add title
        self.strOutput += self.title + '\n'
        
        # add block size x, y, and z
        self.strOutput += "{} {} {} {}\n".format(self.nx, self.ny, self.nz, self.nr)
        self.strOutput += self.createOutputBlock(self.blockSizeX, col=self.blockColX) + '\n'
        self.strOutput += self.createOutputBlock(self.blockSizeY, col=self.blockColY) + '\n'
        self.strOutput += self.createOutputBlock(self.blockSizeZ, col=self.blockColZ) + '\n'
        
        # add resistivity value
        self.strOutput += self.createResistivityValStr() + '\n'
        
        # add resistivity index
        self.strOutput += self.createResistivityIndexStr()

    def save(self, outputFile):
        self.outFileName = outputFile
        with open(outputFile, 'w') as f:
            f.write(self.strOutput)
        f.close()

# Class for CLI
class InitialModelCLI():
    
    def __init__(self):
        self.myInitialModel = CreateInitialModel()
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")    
        self.basePath = os.getcwd()
        readline.parse_and_bind("tab:complete")
    
    def displayHeader(self):
        print ("####################################################################")
        print ("                       MT DATA PREPROCESSING                        ")
        print ("                           INITIAL MODEL                            ")
        print ("####################################################################")
        print ("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print ("{0:17s}: {1}".format("BASE PATH", self.basePath))
        print ("####################################################################")
    
    def getInput(self):
        userInput = input (">> ")
        if userInput=="exit":
            exit()
        return userInput
    
    def getTitle(self):
        print()
        print("Model title")
        self.myInitialModel.title = self.getInput()
        
    def getBlockSide(self):
        blockSide = []
        while(True):
            blockSize = self.getInput().lower()
            if blockSize == "end":
                break
            else:
                try:
                    blockSize = float(blockSize)
                    blockSide.append(blockSize)
                except:
                    print("invalid block size")
        return blockSide
        
    def getBlockX(self):
        print()
        print("Block x")
        print("Auto fill block size in opposite direction? (y/n)")
        while(True):
            autoFillMode = self.getInput().lower()
            if autoFillMode=='y' or autoFillMode=='n':
                break
            else:
                print("invalid input")
        if autoFillMode == 'n':
            print("Input block size (center to south)")
            blockSide1 = self.getBlockSide()
            print("Input block size (center to north)")
            blockSide2 = self.getBlockSide()
            self.myInitialModel.blockSizeX = self.myInitialModel.createBlockXY('manual', blockSide1, blockSide2)
        elif autoFillMode == 'y':
            print("Input block size (center to south)")
            blockSide1 = self.getBlockSide()
            self.myInitialModel.blockSizeX = self.myInitialModel.createBlockXY(mode='auto', side1=blockSide1)
    
    def getBlockY(self):
        print()
        print("Block y")
        print("Auto fill block size in opposite direction? (y/n)")
        while(True):
            autoFillMode = self.getInput().lower()
            if autoFillMode=='y' or autoFillMode=='n':
                break
            else:
                print("invalid input")
        if autoFillMode == 'n':
            print("Input block size (center to west)")
            blockSide1 = self.getBlockSide()
            print("Input block size (center to east)")
            blockSide2 = self.getBlockSide()
            self.myInitialModel.blockSizeY = self.myInitialModel.createBlockXY('manual', blockSide1, blockSide2)
        elif autoFillMode == 'y':
            print("Input block size (center to west)")
            blockSide1 = self.getBlockSide()
            self.myInitialModel.blockSizeY = self.myInitialModel.createBlockXY(mode='auto', side1=blockSide1)
    
    def getBlockZ(self):
        print()
        print("Block z")
        print("Input block size (surface to bottom)")
        blockSide = self.getBlockSide()
        self.myInitialModel.blockSizeZ = blockSide
    
    def getRVal(self):
        print()
        print("Number of resistivity index")
        
        while(True):
            
            try:
                self.myInitialModel.nr = int(self.getInput())
            except:
                print ("invalid input")
            else:
                if self.myInitialModel.nr == 0:
                    print("input resistivity model is in real format")
                elif self.myInitialModel.nr == 1:
                    print("input resistivity is in half-space format")
                elif self.myInitialModel.nr > 1:
                    print("input resistivity is in index format")
                break
        
        print()
        print("Resistivity value")
        rvTemp = []
        
        while(True):
            try:
                inputResistivityValue = float(self.getInput())
            except:
                print("invalid value")
            else:
                rvTemp.append(inputResistivityValue)
            if len(rvTemp) == self.myInitialModel.nr:
                break
        self.myInitialModel.resistivityValue = rvTemp
    
    def getRIndex(self):
        print()
        print("Resistivity index (layer 1 - {})".format(self.myInitialModel.nz))
        
        layerStart = 1
        layerEndFlag = True
        layerRange = []
        resistivityIndex = []
          
        while(True):
            print("layer: {}".format(layerStart), end=' ')
            
            layerRangeTemp = [layerStart]
            
            if layerStart == self.myInitialModel.nz:
                layerEndFlag = False
            
            if layerEndFlag:
                print("to layer:")
                while(True):
                    try:
                        layerEnd = int(self.getInput())
                    except:
                        print("invalid value")
                    else:
                        if layerEnd > self.myInitialModel.nz:
                            print("invalid value: layer cannot greater than {}".format(self.myInitialModel.nz))
                        elif layerEnd < layerStart:
                            print("invalid value: layer cannot less than {}".format(layerStart))
                        else:       
                            if layerEnd == self.myInitialModel.nz:
                                layerRangeTemp.append(layerEnd)
                                layerEndFlag = False
                            elif layerEnd == layerStart:
                                layerStart = layerEnd + 1
                            else:
                                layerRangeTemp.append(layerEnd)
                                layerStart = layerEnd + 1
                            break
                        
            print("Resistivity index:")
            while(True):
                try:
                    inputResistivityIndex = int(self.getInput())
                except:
                    print("invalid value")
                else:
                    resistivityIndex.append(inputResistivityIndex)
                    break
            layerRange.append(layerRangeTemp)
            
            if not layerEndFlag:
                break
                
        self.myInitialModel.resistivityIndexLayer = layerRange
        self.myInitialModel.resistivityIndex = resistivityIndex
        
        print(self.myInitialModel.resistivityIndexLayer)
        print(self.myInitialModel.resistivityIndex)
    
    def getFormatBlock(self):
        while(True):
            blockCol = self.getInput().lower()
            validStringFormat = ["src-x", "src-y", "src-z", "inf"]
            if blockCol in validStringFormat:
                break
            else:
                try:
                    blockCol = int(blockCol)
                except:
                    print("invalid input")
                else:
                    break
        return blockCol
    
    def formatBlock(self):
        print()
        print("Output format")
        
        print("Block X column:")
        self.myInitialModel.blockColX = self.getFormatBlock()
        
        print("Block Y column:")
        self.myInitialModel.blockColY = self.getFormatBlock()
        
        print("Block Z column:")
        self.myInitialModel.blockColZ = self.getFormatBlock()
    
    def fileProcess(self):
        self.myInitialModel.createOutput()
    
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
                    replaceChosen = self.getInput().lower()
                    if replaceChosen == 'y':
                        validChoice = True
                        forceSave = True
                    elif replaceChosen == 'n':
                        validChoice = True
                    else:
                        print ("Invalid input")
                        continue
            if not os.path.isfile(outputFile) or forceSave:
                try:
                    self.myInitialModel.save(outputFile)
                    print ("success..")
                except OSError as err:
                    print (err)
                    continue
                else:
                    break
    
def main():
    myInitialModelCLI = InitialModelCLI()
    myInitialModelCLI.displayHeader()
    myInitialModelCLI.getTitle()
    myInitialModelCLI.getBlockX()
    myInitialModelCLI.getBlockY()
    myInitialModelCLI.getBlockZ()
    myInitialModelCLI.getRVal()
    myInitialModelCLI.getRIndex()
    myInitialModelCLI.formatBlock()
    myInitialModelCLI.fileProcess()
    myInitialModelCLI.fileSave()

if __name__ == "__main__":
    main()