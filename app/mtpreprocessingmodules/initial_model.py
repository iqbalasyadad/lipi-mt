import os
from sys import platform
import numpy as np
import readline

class CreateInitialModel:
    
    def __init__(self):
        self.lriLValues = []
        self.blockColX = 8 #"src-x"
        self.blockColY = 8 #"src-y"
        self.blockColZ = 8 #"src-z"
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
    def nr(self):
        return self._nr
    
    @nr.setter
    def nr(self, value):
        if value != int(value):
            raise TypeError("value must be integer")
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
        for i in range(nBlockVal):
            if not isinstance(blockVal[i], int):
                blockVal[i] = int(blockVal[i])
        strBlock = ''
        if col == "inf":
            for iVal,val in enumerate(blockVal):
                strBlock += ("{}".format(val))
                if iVal < nBlockVal-1:
                    strBlock += ' '
        else:
            # calc max char in blockVal
            maxChar = 0
            for val in blockVal:
                strVal = str(val)
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
                    strVal = "{:{}d}".format(val, valSpacing)
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
                        strVal = "{:{}d}".format(val, valSpacing)
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
                    strVal = "{:{}d}".format(val, valSpacing)
                    strBlock += strVal

                    if trueIndexVal%col==0 and trueIndexVal != nBlockVal:
                        strBlock += '\n'
                    else:
                        strBlock += ' '
        return strBlock

    def createResistivityValStr(self):
        strOut = ''
        for iVal, val in enumerate(self.resistivityValue):
            strOut += str(val)
            if iVal < len(self.resistivityValue)-1:
                strOut += " "
        return strOut

    def createLRILVal(self, lRanges, lValue, nEW, nSE):
        nLR = len(lRanges) 
        nLV = len(lValue)
        if nLR != nLV:
            raise ValueError("nz != vals")
        lriArr = np.zeros([nLR, nSE*nEW], dtype=int)
        for i in range(nLV):
            lriArr[i] = lValue[i]
        return lriArr
    
    def createLRIStr(self, lRanges, lValues, nWE, nSE):
        outStr = ''
        nLR = len(lRanges)
        nLV = len(lValues)
        for i in range(nLR):
            nLRi = len(lRanges[i])
            if nLRi == 1:
                outStr += "{} {}".format(lRanges[i][0], lRanges[i][0])
            elif nLRi == 2:
                outStr += "{} {}".format(lRanges[i][0], lRanges[i][1])
            outStr += '\n'

            # add layer value
            nLVi = len(lValues[i])
            for iVal in range(nLVi):
                outStr += "{}".format(lValues[i][iVal])
                if (i+1)==nLR and (iVal+1)==nSE*nWE:
                    continue
                if (iVal+1)%nWE == 0:
                    outStr += "\n"
                else:
                    outStr += " "
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
        self.strOutput += self.createLRIStr(self.resistivityIndexLayer, self.lriLValues, 
                                            self.ny, self.nx)

    def save(self, outputFile):
        self.outFileName = outputFile
        with open(outputFile, 'w') as f:
            f.write(self.strOutput)

class InitialModelCLI():
    
    def __init__(self):
        self.myIM = CreateInitialModel()
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")    
        self.basePath = os.getcwd()
        readline.parse_and_bind("tab:complete")
    
    def displayHeader(self):
        print("####################################################################")
        print("                       MT DATA PREPROCESSING                        ")
        print("                           INITIAL MODEL                            ")
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
    
    def getTitle(self):
        print()
        print("Model title")
        self.myIM.title = self.getInput()
        
    def getBlockSide(self):
        blockSide = []
        while(True):
            inputBlockSize = self.getInput().lower()
            inputBlockSize = inputBlockSize.split()
            
            for blockSize in inputBlockSize:
                if blockSize=="end":
                    return blockSide
                elif blockSize=="reset":
                    blockSide = []
                    print("block size deleted")
                else:
                    try:
                        blockSize = int(blockSize)
                    except:
                        print("invalid input")
                    else:
                        blockSide.append(blockSize)
        
    def getBlockX(self):
        print()
        print("Block in x direction")
        print("Block size from center to south")
        blockSide1 = self.getBlockSide()
        print("Do you want to use the same block size for center to north? (y/n)")
        while(True):
            mirrorBlockMode = self.getInput().lower()
            if mirrorBlockMode=='y' or mirrorBlockMode=='n':
                break
            else:
                print("invalid input")
        
        if mirrorBlockMode == 'n':
            print("Block size from center to north")
            blockSide2 = self.getBlockSide()
            self.myIM.blockSizeX = self.myIM.createBlockXY('manual', blockSide1, blockSide2)
        elif mirrorBlockMode == 'y':
            self.myIM.blockSizeX = self.myIM.createBlockXY(mode='auto', side1=blockSide1)
    
    def getBlockY(self):
        print()
        print("Block in y direction")
        print("Block size from center to west")
        blockSide1 = self.getBlockSide()
        print("Do you want to use the same block size for center to east? (y/n)")
        while(True):
            mirrorBlockMode = self.getInput().lower()
            if mirrorBlockMode=='y' or mirrorBlockMode=='n':
                break
            else:
                print("invalid input")
        
        if mirrorBlockMode == 'n':
            print("Block size from center to east")
            blockSide2 = self.getBlockSide()
            self.myIM.blockSizeY = self.myIM.createBlockXY('manual', blockSide1, blockSide2)
        elif mirrorBlockMode == 'y':
            self.myIM.blockSizeY = self.myIM.createBlockXY(mode='auto', side1=blockSide1)
    
    def getBlockZ(self):
        print()
        print("Block in z direction")
        print("Block size from surface to bottom")
        blockSide = self.getBlockSide()
        self.myIM.blockSizeZ = blockSide
    
    def getRVal(self):
        print()
        print("Number of resistivity index")
        
        while(True):
            try:
                self.myIM.nr = int(self.getInput())
            except:
                print ("invalid input")
            else:
                if self.myIM.nr == 0:
                    print("input resistivity model is in real format")
                elif self.myIM.nr == 1:
                    print("input resistivity is in half-space format")
                elif self.myIM.nr > 1:
                    print("input resistivity is in index format")
                break
        
        print()
        print("Resistivity value")
        resistivityValueTemp = []
        
        while(True):
            inputResistivityValue = self.getInput().lower().split()
            for resistivity in inputResistivityValue:
                if resistivity == "end":
                    self.myIM.resistivityValue = resistivityValueTemp
                    return
                elif resistivity == "reset":
                    resistivityValueTemp = []
                else:
                    try:
                        resistivity = float(resistivity)
                    except:
                        print("invalid input")
                    else:
                        resistivityValueTemp.append(resistivity)
        
    def getRIndex(self):
        print()
        print("Resistivity index (layer 1 - {})".format(self.myIM.nz))
        layerStart = 1
        layerEndFlag = True
        layerRange = []
        resistivityIndex = []
        
        while(True):
            layerRangeTemp = [layerStart]
            if layerStart == self.myIM.nz:
                print("Layer range: {}".format(layerStart))
                layerEndFlag = False
            else:
                print("Layer range: {}".format(layerStart), end=' ')
            
            if layerEndFlag:
                print("to layer:")
                while(True):
                    inputLayerEnd = self.getInput().lower()
                    if inputLayerEnd == "last":
                        inputLayerEnd = self.myIM.nz
                    elif inputLayerEnd == '':
                        inputLayerEnd = layerStart
                    try:
                        layerEnd = int(inputLayerEnd)
                    except:
                        print("invalid input")
                    else:
                        if layerEnd > self.myIM.nz:
                            print("invalid input: layer cannot greater than {}".format(self.myIM.nz))
                        elif layerEnd < layerStart:
                            print("invalid input: layer cannot less than {}".format(layerStart))
                        else:       
                            if layerEnd == self.myIM.nz:
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
                    print("invalid input")
                else:
                    resistivityIndex.append(inputResistivityIndex)
                    break
            layerRange.append(layerRangeTemp)
            
            if not layerEndFlag:
                break
                
        self.myIM.resistivityIndexLayer = layerRange
        self.myIM.resistivityIndex = resistivityIndex
        
        self.myIM.lriLValues = self.myIM.createLRILVal(self.myIM.resistivityIndexLayer, 
                                                       self.myIM.resistivityIndex,
                                                       self.myIM.ny, self.myIM.nx)
                
    
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
        print("Column format ('src-x'/'src-y'/'src-z'/'inf'/integer)")
        print("Block X column")
        self.myIM.blockColX = self.getFormatBlock()
        print("Block Y column")
        self.myIM.blockColY = self.getFormatBlock()
        print("Block Z column")
        self.myIM.blockColZ = self.getFormatBlock()
    
    def fileProcess(self):
        self.myIM.createOutput()
    
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
                    self.myIM.save(outputFile)
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
        print("Block x ({}) south-north:".format(self.myIM.nx))
        print(self.myIM.blockSizeX)
        print()
        print("Block y ({}) west-east:".format(self.myIM.ny))
        print(self.myIM.blockSizeY)
        print()
        print("Block z ({}) surface-bottom:".format(self.myIM.nz))
        print(self.myIM.blockSizeZ)
        print()
        print("Number of resistivity index: {}".format(self.myIM.nr))
        print()
        print("Resistivity value: {}".format(self.myIM.resistivityValue))
        print()
        maxCharL = 0
        for layerRange in self.myIM.resistivityIndexLayer:
            maxCharLayerRange = 0
            for layer in layerRange:
                nStrLayer = len(str(layer))
                maxCharLayerRange += nStrLayer
            if maxCharLayerRange > maxCharL:
                maxCharL = maxCharLayerRange
        maxCharL += 3
        maxCharI = 0
        for indexVal in self.myIM.resistivityIndex:
            nStrIndex = len(str(indexVal))
            if nStrIndex > maxCharI:
                maxCharI = nStrIndex
        strHeaderLayer = "Layer"
        strRI = "Resistivity index"
        if maxCharL < len(strHeaderLayer)+1:
            maxCharL = len(strHeaderLayer)+1
        print("{:{}s}".format(strHeaderLayer, maxCharL), end=' ')
        print("{:{}s}".format(strRI, maxCharI))
        for iLayerRange, layerRange in enumerate(self.myIM.resistivityIndexLayer):
            if len(layerRange)==1:
                strLayerRange = "{}".format(layerRange[0])
            elif len(layerRange)==2:
                strLayerRange = "{}-{}".format(layerRange[0], layerRange[1])
            strIndexVal = str(self.myIM.resistivityIndex[iLayerRange])
            print("{:{}s}".format(strLayerRange, maxCharL), end=' ')
            print("{:{}s}".format(strIndexVal, maxCharI))
        print()
        print("Output file: {}".format(self.myIM.outFileName))
        print("####################################################################")  

def main():
    myIMCLI = InitialModelCLI()
    myIMCLI.displayHeader()
    myIMCLI.getTitle()
    myIMCLI.getBlockX()
    myIMCLI.getBlockY()
    myIMCLI.getBlockZ()
    myIMCLI.getRVal()
    myIMCLI.getRIndex()
    myIMCLI.formatBlock()
    myIMCLI.fileProcess()
    myIMCLI.fileSave()
    myIMCLI.displayResult()

if __name__ == "__main__":
    main()
