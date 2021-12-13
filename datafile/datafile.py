from sys import platform
import readline
import os
import errno
import glob
import utm
import numpy as np
from tabulate import tabulate

class StationCoordinate:    
    def __init__(self, file):
        self.basePath = os.getcwd()
        coordinateFilePath = os.path.join(self.basePath, file)
        self.inputType, self.inputStations, self.inputCoordinates = self.__parse(coordinateFilePath)
        self.usedCoordinates = self.inputCoordinates
        
    def __parse(self, file):
        with open(file, 'r') as f:
            rows = f.readlines()
            header =''
            stations = []
            data = []
            for row in rows:
                splittedRow = row.split()
                if splittedRow:
                    if len(splittedRow) == 1:
                        header = splittedRow[0]
                        if header not in ["DD", "UTM"]:
                            raise CoordinateFileError("[Error] invalid file header: \'{}\'".format(header))
                    elif len(splittedRow)==3:
                        stations.append(splittedRow[0])
                        try:
                            latitude = float (splittedRow[1])
                            longitude = float (splittedRow[2])
                        except:
                            raise CoordinateFileError ("[Error] invalid data: {}".format(splittedRow))
                        data.append([latitude, longitude])
        return header, np.array(stations), np.array(data)
    
    def getStationCoordinate(self, station):
        found=False
        for index, inputStation in enumerate (self.inputStations):
            if inputStation==station:
                found=True
                return self.inputCoordinates[index]
        if not found:
            raise CoordinateFileError ("[Error] station coordinate not found: \'{}\'".format(station))
                
    def setUsedStation(self, usedStations):
        usedCoordinates = np.zeros([len(usedStations),2], dtype=float)
        for index, station in enumerate (usedStations):
            usedCoordinates[index] = self.getStationCoordinate(station)
        self.usedCoordinates = usedCoordinates    
        
    def createCoordinateUTM(self):
        if self.inputType=="DD":
            self.easting, self.northing, zone_num, zone_c = utm.from_latlon(self.usedCoordinates[:,0], self.usedCoordinates[:,1])
            self.utm = np.array([[el_e, el_n] for el_e, el_n in zip(self.easting, self.northing)])
        elif self.inputType=="UTM":
            self.easting = self.usedCoordinates[:,0]
            self.northing = self.usedCoordinates[:,1]
            self.utm = self.usedCoordinates
    
    def recenterCoordinate(self, eastingCenter=None, northingCenter=None,  mode=None):
        if mode=="auto":
            self.eastingCenter = (max(self.easting) - min(self.easting))/2 + min(self.easting)
            self.northingCenter = (max(self.northing) - min(self.northing))/2 + min(self.northing)
        else:
            self.eastingCenter = eastingCenter
            self.northingCenter = northingCenter
        self.easting0 = self.easting - self.eastingCenter
        self.northing0 = self.northing - self.northingCenter
    
    def latLngToUTM(self, lat, lng):
        easting, northing, zone_num, zone_c = utm.from_latlon(lat, lng)
        return easting, northing
        
class CoordinateFileError(Exception):
    pass
    

class CreateDataFile:
    
    def __vartoerr(self, data):
        return data ** 0.5
        
    def __init__ (self):
        self.headerFreq = "FREQS"
        self.headerZxxRe = "Zxx Re (Rot)"
        self.headerZxxIm = "Zxx Im (Rot)"
        self.headerZxyRe = "Zxy Re (Rot)"
        self.headerZxyIm = "Zxy Im (Rot)"
        self.headerZyxRe = "Zyx Re (Rot)"
        self.headerZyxIm = "Zyx Im (Rot)"
        self.headerZyyRe = "Zyy Re (Rot)"
        self.headerZyyIm = "Zyy Im (Rot)"
        self.headerZxxVar = "Zxx VAR (Rot)"
        self.headerZxyVar = "Zxy VAR (Rot)"
        self.headerZyxVar = "Zyx VAR (Rot)"
        self.headerZyyVar = "Zyy VAR (Rot)"
        self.outputStr = ''
        self.basePath = os.getcwd()
    
    def setInputDirectory(self, directory=None):
        if directory:
            if os.path.isdir(directory):
                self.pt1FolderPath = os.path.join(self.basePath, directory)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), directory)
        else:
            self.pt1FolderPath = self.basePath
                
    def setInputFiles(self, files='*'):
        if not files or files=='.' or files=='*':
            inputFiles = [os.path.basename(x) for x in glob.glob('*.pt1')]
            inputFiles = np.sort(inputFiles)            
        else:
            if isinstance(files, str):
                files = files.split()
            inputFiles = []
            for file in files:
                if os.path.isfile(file):
                    inputFiles.append(file)
                else:
                    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
        self.inputFiles = inputFiles
    
    def getInputFiles(self):
        return self.inputFiles
    
    def setResponses(self, nResponses):
        self.nResponses = nResponses
        if self.nResponses == 4:
            self.impedanceTensorHeaders = [self.headerZxyRe, self.headerZxyIm, self.headerZyxRe, self.headerZyxIm]
            self.impedanceTensorErrorHeaders = [self.headerZxyVar, '-', self.headerZyxVar, '-']
        elif self.nResponses == 8:
            self.impedanceTensorHeaders = [self.headerZxxRe, self.headerZxxIm, self.headerZxyRe, self.headerZxyIm,
                                           self.headerZyxRe, self.headerZyxIm, self.headerZyyRe, self.headerZyyIm]
            self.impedanceTensorErrorHeaders = [self.headerZxxVar, '-', self.headerZxyVar, '-',
                                                self.headerZyxVar, '-', self.headerZyyVar, '-']
        else:
            raise ValueError("Invalid number of responses: {}".format(nResponses))

    def setUsedPeriods(self, usedPeriods):
        usedPeriodsArr = np.array(usedPeriods)
        self.usedPeriods = usedPeriodsArr
        self.usedFrequencies = 1/usedPeriodsArr
    
    def __parse(self, file):
        headers=[]
        data=[]
        header_num = 0
        with open(file) as f:
            for line in f:
                first_str = line.split()[0]
                try:
                    float (first_str)
                    for val in line.split():
                        data[header_num-1].append(float(val))
                except:
                    if first_str == "PARAMETER#":
                        headers.append(' '.join(line.split()[3:]))
                    else:
                        headers.append(line.split()[0].replace(':',''))
                    header_num +=1
                    data.append([])
        return np.array(headers, dtype=object), np.array(data,dtype=object)
    
    def __getHeaderIndex(self, search, headers):
        found=False
        for index, header in enumerate (headers):
            if search == header:
                found = True
                return index
        assert found==True, "Header not found"
        
    def __getNearestPeriodsIndex(self, usedPeriods, filePeriods):
        filePeriods = np.array(filePeriods)
        nearestPeriodsIndex = np.zeros(len(usedPeriods), dtype=int)
        nearestPeriods = np.zeros(len(usedPeriods), dtype=float)
        for i in range (len(usedPeriods)):
            nearestPeriodIndex = np.argmin(abs(filePeriods-usedPeriods[i]))
            nearestPeriodsIndex[i] = nearestPeriodIndex
            nearestPeriods[i] = filePeriods[nearestPeriodIndex]
        return nearestPeriods, nearestPeriodsIndex
    
    def __getDataOnPeriods(self, searchHeader, fileHeaders, fileData, periodsIndex):
        headerIndex = self.__getHeaderIndex(searchHeader, fileHeaders)
        headerData = fileData[headerIndex]
        usedHeaderData = np.zeros(len(periodsIndex), dtype=float)
        for i in range (len(periodsIndex)):
            usedHeaderData[i] = headerData[periodsIndex[i]]
        return usedHeaderData
    
    def setImpedanceTensorErrorImag(self, errorValue):
        self.impedanceTensorErrorImag = errorValue
    
    def __getAllData(self):
        self.impedanceTensorHeaderDatasAll = []
        self.impedanceTensorHeaderErrorDatasAll = []
        self.nearestPeriodsAll = np.zeros([len(self.inputFiles),len(self.usedPeriods)], dtype=float)
        
        for fIndex, f in enumerate (self.inputFiles):
            pt1FilePath = os.path.join(self.pt1FolderPath, f)
            fileHeaders, fileData = self.__parse(pt1FilePath)
            
            # get nearest periods
            fileFrequencyIndex = self.__getHeaderIndex(self.headerFreq, fileHeaders)
            fileFrequencies = fileData[fileFrequencyIndex]
            filePeriods = 1/fileFrequencies
            self.nearestPeriodsAll[fIndex], nearestPeriodsIndex = self.__getNearestPeriodsIndex(self.usedPeriods, filePeriods)
            
            # get impedance tensor for each header
            impedanceTensorHeaderDatas = np.zeros([len(self.impedanceTensorHeaders) ,len(self.usedPeriods)], dtype=float)
            for i in range (len(self.impedanceTensorHeaders)):
                impedanceTensorHeaderDatas[i] = self.__getDataOnPeriods(self.impedanceTensorHeaders[i], fileHeaders, fileData, nearestPeriodsIndex)
            self.impedanceTensorHeaderDatasAll.append(impedanceTensorHeaderDatas)

            # get impedance tensor error for each header
            impedanceTensorHeaderErrorDatas = np.zeros([len(self.impedanceTensorErrorHeaders) ,len(self.usedPeriods)], dtype=float)
            lastImpedanceTensorError = np.zeros(len(self.usedPeriods), dtype=float)
            for i in range (len(self.impedanceTensorErrorHeaders)):
                if self.impedanceTensorErrorHeaders[i] == '-' :
                    impedanceTensorErrorValue = np.zeros(len(self.usedPeriods), dtype=float)
                    try:
                        impedanceTensorErrorValue[:] = float (self.impedanceTensorErrorImag)
                    except:
                        if self.impedanceTensorErrorImag.lower() == "=real":
                            impedanceTensorErrorValue = lastImpedanceTensorError
                        else:
                            impedanceTensorErrorValue[:] = np.nan
                else:
                    impedanceTensorErrorValue = self.__getDataOnPeriods(self.impedanceTensorErrorHeaders[i], fileHeaders, fileData, nearestPeriodsIndex)
                    impedanceTensorErrorValue = self.__vartoerr(impedanceTensorErrorValue)
                    lastImpedanceTensorError = impedanceTensorErrorValue
                impedanceTensorHeaderErrorDatas[i] = impedanceTensorErrorValue
            self.impedanceTensorHeaderErrorDatasAll.append(impedanceTensorHeaderErrorDatas)
    
    def __createDataOnP(self, data, headers):
        dataOnPeriods =  np.zeros([len(self.usedPeriods), len(self.inputFiles), len(headers)])
        for i in range (len(self.usedPeriods)):
            for j in range (len(self.inputFiles)):
                for k in range (len(headers)):
                    dataOnPeriods[i][j][k] = data[j][k][i]
        return dataOnPeriods
        
    def initErrMapVal(self):
        nPeriod = len(self.usedPeriods)
        nFile =  len(self.inputFiles)
        nITHeader = len(self.impedanceTensorHeaders)
        self.errMapVal = np.ones([nPeriod, nFile, nITHeader])
    
    def changeErrMapVal(self, changeLists):
        for changeList in changeLists:
            period = changeList[0]
            stationList = changeList[1]
            responseList = changeList[2]
            value = changeList[3]
            if (stationList=="all"):
                stationList = np.arange(len(self.errMapVal[0]))
            if (responseList=="all"):
                responseList = np.arange(len(self.errMapVal[0][0]))
            for station in stationList:
                for response in responseList:
                    self.errMapVal[period-1][station-1][response-1] = value        
        
    def __addFirstLinestr(self):
        self.outputStr += ' {} {} {}'.format(len(self.inputFiles), len(self.usedPeriods),
                                             len(self.impedanceTensorHeaders))
        
    def __addDataOnPstr(self, headerOut, data):
        # get maximum character
        nCharData = 0
        negativeVal = False
        for i in range (len(self.usedPeriods)):
            for row in data[i]:
                for val in row:
                    nCharDataCurrent = len("{:.4E}".format(val))
                    if nCharDataCurrent > nCharData:
                        nCharData = nCharDataCurrent
                        if val < 0:
                            negativeVal = True
        if negativeVal:
            dataSpacing = nCharData
        else:
            dataSpacing = nCharData + 1
        
        # add header and data to output string
        for i in range(len(self.usedPeriods)):
            self.outputStr += "\n{}  {:.4E}".format(headerOut, self.usedPeriods[i])
            for row in data[i]:
                self.outputStr += '\n'
                for val in row:
                    if np.isnan(val):
                        self.outputStr += "  {}".format(self.impedanceTensorErrorImag)
                    else:
                        self.outputStr += " {:{}.4E}".format(val, dataSpacing)
                    
    def setCoordinate(self, easting, northing): 
        self.easting = easting
        self.northing = northing
        
    def __addCoordinatestr(self, header, data):
        self.outputStr += "\n{}".format(header)
        nCharCoordinate = np.zeros(len(data), dtype=int)
        for i in range(len(data)):
            nCharCoordinate[i] = len("{:.2f}".format(data[i]))
        coordinateSpacing = max(nCharCoordinate) + 1
        self.outputStr += '\n'
        for i in range(len(data)):
            self.outputStr += ' {:{}.2f}'.format(data[i], coordinateSpacing)
            if (i+1)%8==0: self.outputStr += '\n'
            
    def process(self):
        self.__getAllData()
        impedanceTensorOnP = self.__createDataOnP(self.impedanceTensorHeaderDatasAll, self.impedanceTensorHeaders)
        impedanceTensorErrorOnP = self.__createDataOnP(self.impedanceTensorHeaderErrorDatasAll, self.impedanceTensorErrorHeaders)
        
        self.__addFirstLinestr()
        self.__addCoordinatestr("Station_Location: N-S", self.northing)
        self.__addCoordinatestr("Station_Location: E-W", self.easting)
        self.__addDataOnPstr("DATA_Period:", impedanceTensorOnP)
        self.__addDataOnPstr("ERROR_Period:", impedanceTensorErrorOnP)
        self.__addDataOnPstr("ERMAP_Period:", self.errMapVal)
        
    def save(self, outputFile):
        self.outName = outputFile
        with open (outputFile, 'w') as f:
            f.write(self.outputStr)
        f.close()
    
    def getOutName(self):
        return self.outName

class DataFileCLI:

    def __init__(self):
        self.newFile = CreateDataFile()
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")    
        self.basePath = os.getcwd()
        readline.parse_and_bind("tab:complete")

    def displayHeader(self):
        print("####################################################################")
        print("                       MT DATA PREPROCESSING                        ")
        print("                             DATA FILE                              ")
        print("####################################################################")
        print("{0:17s}: {1}".format("TAB", "autocomplete file or folder name"))
        print("{0:17s}: {1}".format("DOUBLE TAB", "list of all file and folder in the directory"))
        print("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print("{0:17s}: {1}".format("BASE PATH", self.basePath))
        print("####################################################################")

    
    def getInput(self):
        userInput = input(">> ")
        userInputLower = userInput.lower()
        if userInputLower == "exit":
            print("Program closed")
            exit()
        else:
            return userInput
    
    def chdir(self, directory):
        os.chdir(directory)
    
    def getpt1Directory(self):
        print()
        print(".pt1 directory")
        while True:
            self.pt1directory = self.getInput()
            try:
                self.newFile.setInputDirectory(self.pt1directory)
            except OSError as err:
                print(err)
                continue
            else:
                break

    def getInputFiles(self):
        print()
        print("Input files (./*.pt1)")
        filesF = []
        while True:
            inputFiles = self.getInput()
            if len(filesF)==0 and inputFiles=="" or inputFiles.lower()=="." or inputFiles.lower()=="*":
                self.newFile.setInputFiles(inputFiles)
                break
            else:
                inputFiles = inputFiles.split()
                for file in inputFiles:
                    if file.lower()=="end":
                        try:
                            self.newFile.setInputFiles(filesF)
                        except FileNotFoundError as err:
                            print(err)
                            filesF = []
                            print("Input files cleared")
                            continue
                        else:
                            return
                    elif file.lower()=="reset":
                        filesF = []
                        print("Input files cleared")
                    else:
                        filesF.append(file)

    def getNumberResponses(self):
        print()
        print("Number of responses (4/8)")
        while True:
            nResponses = self.getInput()
            try:
                nResponses = int (nResponses)
                assert nResponses==4 or nResponses==8
            except:
                print("Invalid number of responses")
                continue
            else:
                break
        self.newFile.setResponses(nResponses)
    
    def getSelectedPeriods(self):
        print()
        print("Select periods")
        selectedPeriods = []
        while True:
            inputPeriods = self.getInput().split()
            for period in inputPeriods:
                if period.lower()=="end":    
                    if len(selectedPeriods)==0:
                        print("period length must be greater than 0")
                        continue
                    else:
                        self.newFile.setUsedPeriods(selectedPeriods)
                        return
                elif period.lower()=="reset":
                    selectedPeriods = []
                    print("Input periods cleared")
                else:
                    try:
                        period = float(period)
                    except:
                        print("Invalid value")
                        selectedPeriods = []
                        print("Input periods cleared")
                    else:
                        selectedPeriods.append(period)
    
    def getITImaginaryError(self):
        print()
        print("Imaginary impedance tensor error (=real/0/nan)")
        while True:
            impedanceTensorErrorImag = self.getInput()
            try:
                self.newFile.setImpedanceTensorErrorImag(impedanceTensorErrorImag)
            except:
                print("Invalid input")
                continue
            else:
                break
    def showErrMapParamTable(self, datas, name):
        tableHeader = ["Id"]
        for i in range(len(datas)):
            tableHeader.append(i+1)
        tableData = [name]
        for data in datas:
            try:
                float(data)
            except:
                data = data.replace(" (Rot)", "")
                data = data.replace(".pt1", "")
            tableData.append(data)
        print(tabulate([tableData], headers=tableHeader))   
        
    def breakErrMapStr(self, inputStr): #(break "1_1-2_All_999")
        inputStr = inputStr.split("_")
        changeLists = []
        for lists in inputStr:
            if lists != '':
                strList = lists.split("-")
                tempList = []
                for el in strList:
                    try:
                        el = int(el)
                    except:
                        tempList.append(el.lower())
                    else:
                        tempList.append(el)
                if len(tempList)==1:
                    changeLists.append(tempList[0])
                else:
                    changeLists.append(tempList)
        return changeLists
    
    def getErrMapChangesVal(self):
        changeListsF = []
        while True:
            rawInputsStr = self.getInput().lower()
            rawInputsStr = rawInputsStr.split()
            for rawInputStr in rawInputsStr:
                if rawInputStr=="end":
                    return changeListsF
                    break
                elif rawInputStr=="reset":
                    changeListsF = []
                else:
                    changeListsF.append(self.breakErrMapStr(rawInputStr))
    
    def getErrorMap(self):
        self.newFile.initErrMapVal()
        print()
        print("Change Error Map Period? (y/n)")
        while True:
            changeErrMap = self.getInput().lower()
            if changeErrMap=="y":
                print()
                self.showErrMapParamTable(self.newFile.usedPeriods, "Period")
                print()
                self.showErrMapParamTable(self.newFile.getInputFiles(), "File")
                print()
                self.showErrMapParamTable(self.newFile.impedanceTensorHeaders, "Response")
                print()
                print("Input format: period_file-list_response-list_value")
                errMapChanges = self.getErrMapChangesVal()
                try:
                    self.newFile.changeErrMapVal(errMapChanges)
                except:
                    print("Invalid input")
                break
            elif changeErrMap=="n":
                break
            else:
                print("Invalid input")
                continue
    
    def getCoordinate(self):
        print()
        print("Coordinate file (.txt)")
        while True:
            coordinateFile = self.getInput()
            try:
                staCoordinate = StationCoordinate(coordinateFile)
                staCoordinate.setUsedStation(self.newFile.getInputFiles())
                staCoordinate.createCoordinateUTM()
            except OSError as err:
                print(err)
                continue
            except CoordinateFileError as err:
                print(err)
                continue
            else:
                break
        
        print()
        print("Automatic model center (using station center)? (y/n)")
        
        while(True):
            autoModelCenter = self.getInput().lower()
            if autoModelCenter=='y':
                staCoordinate.recenterCoordinate(mode='auto')
                break
            elif autoModelCenter=='n':
                print("Input model center coordinate (DD/UTM lat/northing lng/easting)")
                while(True):
                    staCenters = self.getInput().lower().split()
                    try:
                        staCenters1 = float(staCenters[1])
                        staCenters2 = float(staCenters[2])
                    except:
                        print("Invalid input")
                    if staCenters[0]=="utm":
                        staCenterEasting = staCenters2
                        staCenterNorthing = staCenters1
                    elif staCenters[0]=="dd":
                        staCenterEasting, staCenterNorthing = staCoordinate.latLngToUTM(staCenters1, staCenters2)
                    try:
                        staCoordinate.recenterCoordinate(staCenterEasting, staCenterNorthing)
                    except:
                        print("Error")
                    else:
                        break
                break
            else:
                print("Invalid input")
                continue

        self.newFile.setCoordinate(staCoordinate.easting0, staCoordinate.northing0)

        self.staCoordinates = [staCoordinate.easting, staCoordinate.northing]
        self.staCenter = [staCoordinate.eastingCenter, staCoordinate.northingCenter]
        self.coordinateHeader = staCoordinate.inputType

    def fileProcess(self):
        self.newFile.process()
    
    def getFileSave(self):
        print()
        while True:
            print("Output file")
            outputFile = self.getInput()
            forceSave = False
            if os.path.isfile(outputFile) and not forceSave:
                validChoice = False
                while not validChoice:
                    print("File already exist. Replace file? (y/n)")
                    replaceChosen = self.getInput().lower()
                    if replaceChosen == 'y':
                        validChoice = True
                        forceSave = True
                    elif replaceChosen == 'n':
                        validChoice = True
                    else:
                        print("Invalid input")
                        continue
            if not os.path.isfile(outputFile) or forceSave:
                try:
                    self.newFile.save(outputFile)
                    print("success..")
                except OSError as err:
                    print(err)
                    continue
                else:
                    break
    
    def displayResult(self):
        print()
        print("####################################################################")
        print("                             RESULT                                 ")
        print("\nSelected periods:")
        for period in self.newFile.usedPeriods:
            print("{:.4E}".format(period), end=' ')
        print()
        print("\nNearest periods:")
        for i in range (len(self.newFile.inputFiles)):
            for period in self.newFile.nearestPeriodsAll[i]:
                print("{:.4E}".format(period), end=' ')
            print("({})".format(self.newFile.inputFiles[i]))
        print("\nImpedance Tensor Error (Im): {}".format(self.newFile.impedanceTensorErrorImag))
        print("\nCoordinate header: {}".format(self.coordinateHeader))
        print("\nStation coordinate (UTM):")
        staCoordTableList = []
        for i in range(len(self.newFile.inputFiles)):
            staCoordTableList.append([self.newFile.inputFiles[i], self.staCoordinates[0][i], self.staCoordinates[1][i]])
        print(tabulate(staCoordTableList, headers=['Name', 'Easting', 'Northing'], floatfmt=".2f"))
        print("\nCenter of station:")
        print("Easting: {}".format(self.staCenter[0]))
        print("Northing: {}".format(self.staCenter[1]))
        print("\nOutput file: {}".format(self.newFile.getOutName()))
        print("####################################################################")

def main():
    userCLI = DataFileCLI()
    userCLI.displayHeader()
    userCLI.getpt1Directory()
    userCLI.chdir(userCLI.pt1directory)
    userCLI.getInputFiles()
    userCLI.chdir(userCLI.basePath)
    userCLI.getNumberResponses()
    userCLI.getSelectedPeriods()
    userCLI.getITImaginaryError()
    userCLI.getErrorMap()
    userCLI.getCoordinate()
    userCLI.fileProcess()
    userCLI.getFileSave()
    userCLI.displayResult()

if __name__ == "__main__":
    main()
