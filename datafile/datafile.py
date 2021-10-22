from sys import platform
import readline
import os
import errno
import glob
import utm
import numpy as np


class Coordinate:
    
    def __init__(self, file):
        self.inputType, self.inputStations, self.inputDatas = self.__parse(file)
        self.usedCoordinates = self.inputDatas

    def getInputType(self):
        return self.inputType

    def getInputStations(self):
        return self.inputStations

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
    
    def __createUTM(self):
        if self.inputType == "DD":
            convertedUTM = self.__toUTM()
            return convertedUTM
        elif self.inputType == "UTM":
            return self.usedCoordinates
    
    def __toUTM(self):    
        nCoordinate = len(self.usedCoordinates)
        utmCoordinate = np.zeros([nCoordinate, 2], dtype=float)
        for i in range (nCoordinate):
            easting, northing, zone_num, zone_c =  utm.from_latlon(self.usedCoordinates[i][0], self.usedCoordinates[i][1])
            utmCoordinate[i][0] = easting
            utmCoordinate[i][1] = northing
        return utmCoordinate
    
    def getStationCoordinate(self, station):
        found=False
        for index, inputStation in enumerate (self.inputStations):
            if inputStation==station:
                found=True
                return self.inputDatas[index]
        if not found:
            raise CoordinateFileError ("[Error] station coordinate not found: \'{}\'".format(station))
                
    def setUsed(self, usedStations):
        usedCoordinates = np.zeros([len(usedStations),2], dtype=float)
        for index, station in enumerate (usedStations):
            usedCoordinates[index] = self.getStationCoordinate(station)
        self.usedCoordinates = usedCoordinates
    
    def process(self):
        self.utm = self.__createUTM()
        
    def getUTM(self):
        return self.utm
    
    def getEasting(self):
        return self.utm[:,0]
    
    def getNorthing(self):
        return self.utm[:,1]

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
    
    def setErrorMap(self, errorMapValue):
        self.errorMapValue = errorMapValue
    
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
    
    def __createErrorMapOnP(self):
        if self.errorMapValue == 1:
            return np.ones([len(self.usedPeriods), len(self.inputFiles), len(self.impedanceTensorHeaders)])
    
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
        impedanceTensorErrorMapOnP = self.__createErrorMapOnP()
        
        self.__addFirstLinestr()
        self.__addCoordinatestr("Station_Location: N-S", self.northing)
        self.__addCoordinatestr("Station_Location: E-W", self.easting)
        self.__addDataOnPstr("DATA_Period:", impedanceTensorOnP)
        self.__addDataOnPstr("ERROR_Period:", impedanceTensorErrorOnP)
        self.__addDataOnPstr("ERMAP_Period:", impedanceTensorErrorMapOnP)
        
    def save(self, outputFile):
        self.outName = outputFile
        with open (outputFile, 'w') as f:
            f.write(self.outputStr)
        f.close()
    
    def getOutName(self):
        return self.outName

class CommandLine:

    def __init__(self):
        self.newFile = CreateDataFile()
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")    
        self.basePath = os.getcwd()
        readline.parse_and_bind("tab:complete")

    def displayHeader(self):
        print ("####################################################################")
        print ("                       MT DATA PREPROCESSING                        ")
        print ("                             DATA FILE                              ")
        print ("####################################################################")
        print ("{0:17s}: {1}".format("TAB", "autocomplete file or folder name"))
        print ("{0:17s}: {1}".format("DOUBLE TAB", "list of all file and folder in the directory"))
        print ("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print ("{0:17s}: {1}".format("BASE PATH", self.basePath))
        print ("####################################################################")

    
    def getInput(self):
        userInput = input (">> ")
        if userInput=="exit":
            exit()
        return userInput
    
    def chdir(self, directory):
        os.chdir(directory)
    
    def getpt1Directory(self):
        print ()
        print (".pt1 directory")
        while True:
            self.pt1directory = self.getInput()
            try:
                self.newFile.setInputDirectory(self.pt1directory)
            except OSError as err:
                print (err)
                continue
            else:
                break

    def getInputFiles(self):
        print ()
        print ("Input files (./*.pt1)")
        while True:
            inputFile = self.getInput()
            try:
                self.newFile.setInputFiles(inputFile)
            except FileNotFoundError as err:
                print (err)
                continue
            else:
                break

    def getNumberResponses(self):
        print ()
        print ("Number of responses (4/8)")
        while True:
            nResponses = self.getInput()
            try:
                nResponses = int (nResponses)
                assert nResponses==4 or nResponses==8
            except:
                print ("Invalid number of responses")
                continue
            else:
                break
        self.newFile.setResponses(nResponses)
    
    def getSelectedPeriods(self):
        print ()
        print ("Select periods")
        while True:
            selectedPeriods = self.getInput().split()
            try:
                selectedPeriods = [float (period) for period in selectedPeriods]
            except ValueError:
                print ("Invalid input")
                continue
            else:
                break
        self.newFile.setUsedPeriods(selectedPeriods)
    
    def getITImaginaryError(self):
        print ()
        print ("Imaginary impedance tensor error (=real/0/nan)")
        while True:
            impedanceTensorErrorImag = self.getInput()
            try:
                self.newFile.setImpedanceTensorErrorImag(impedanceTensorErrorImag)
            except:
                print ("Invalid input")
                continue
            else:
                break
    
    def getErrorMap(self):
        self.newFile.setErrorMap(1)
    
    def getCoordinate(self):
        print ()
        print ("Coordinate file (.txt)")
        while True:
            coordinateFile = self.getInput()
            try:
                staCoordinate = Coordinate(coordinateFile)
                staCoordinate.setUsed(self.newFile.getInputFiles())
                staCoordinate.process()
                self.newFile.setCoordinate(staCoordinate.getEasting(), staCoordinate.getNorthing())
            except OSError as err:
                print (err)
                continue
            except CoordinateFileError as err:
                print (err)
                continue
            else:
                break
        self.coordinateHeader = staCoordinate.getInputType()

    def fileProcess(self):
        self.newFile.process()
    
    def getFileSave(self):
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
                    self.newFile.save(outputFile)
                    print ("success..")
                except OSError as err:
                    print (err)
                    continue
                else:
                    break
    
    def displayResult(self):
        print ()
        print ("####################################################################")
        print ("                             RESULT                                 ")
        print ("\nSelected periods:")
        for period in self.newFile.usedPeriods:
            print ("{:.4E}".format(period), end=' ')
        print ()
        print ("\nNearest periods:")
        for i in range (len(self.newFile.inputFiles)):
            for period in self.newFile.nearestPeriodsAll[i]:
                print ("{:.4E}".format(period), end=' ')
            print ("({})".format(self.newFile.inputFiles[i]))
        print ("\nCoordinate header: {}".format(self.coordinateHeader))
        print ("\nOutput file: {}".format(self.newFile.getOutName()))
        print ("####################################################################")

def main():
    userCLI = CommandLine()
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