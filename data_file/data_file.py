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
    
    def getStationInput(self):
        stations = {}
        if self.inputType == "DD":
            key1 = 'lat'
            key2 = 'lng'
        elif self.inputType == "UTM":
            key1 = 'easting'
            key2 = 'northing'
        for i in range(len(self.inputStations)):
            stations[self.inputStations[i]] = {key1: self.inputCoordinates[i][0], key2: self.inputCoordinates[i][1]}
        return stations

        
class CoordinateFileError(Exception):
    pass
    
class CreateDataFile:
        
    def __init__ (self):
        self.inputHeader = {
            "frequency": "FREQS",
            "zxx": {"re": "Zxx Re (Rot)", "im": "Zxx Im (Rot)", "var": "Zxx VAR (Rot)"},
            "zxy": {"re": "Zxy Re (Rot)", "im": "Zxy Im (Rot)", "var": "Zxy VAR (Rot)"},
            "zyx": {"re": "Zyx Re (Rot)", "im": "Zyx Im (Rot)", "var": "Zyx VAR (Rot)"},
            "zyy": {"re": "Zyy Re (Rot)", "im": "Zyy Im (Rot)", "var": "Zyy VAR (Rot)"} }
        
        self.outputStr = ''
        self.basePath = os.getcwd()
    
    def __vartoerr(self, data):
        return data ** 0.5
    
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
            
            self.impedanceTensorHeaders = [self.inputHeader["zxy"]["re"], self.inputHeader["zxy"]["im"], 
                                           self.inputHeader["zyx"]["re"], self.inputHeader["zyx"]["im"]]
            
            self.impedanceTensorErrorHeaders = [self.inputHeader["zxy"]["var"], '-', self.inputHeader["zyx"]["var"], '-']
                                           
                                           
        elif self.nResponses == 8:
                                           
            self.impedanceTensorHeaders = [self.inputHeader["zxx"]["re"], self.inputHeader["zxx"]["im"], 
                                           self.inputHeader["zxy"]["re"], self.inputHeader["zxy"]["im"],
                                           self.inputHeader["zyx"]["re"], self.inputHeader["zyx"]["im"], 
                                           self.inputHeader["zyy"]["re"], self.inputHeader["zyy"]["im"]]
                                           
            self.impedanceTensorErrorHeaders = [self.inputHeader["zxx"]["var"], '-',
                                                self.inputHeader["zxy"]["var"], '-',
                                                self.inputHeader["zyx"]["var"], '-',
                                                self.inputHeader["zyy"]["var"], '-']
        else:
            raise ValueError("Invalid number of responses: {}".format(nResponses))
    
    def setUsedValues(self, mode, usedValues):
        self.usedValuesMode = mode
        if mode=="frequency":
            self.usedFrequencies = np.array(usedValues)
            self.usedPeriods = 1/self.usedFrequencies
        elif mode=="period":
            self.usedPeriods = np.array(usedValues)
            self.usedFrequencies = 1/self.usedPeriods
        else:
            raise ValueError("Invalid mode")
        
    
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
        
    def __getNearestFrequencyIndex(self, usedFrequencies, fileFrequencies):
        nearestFrequenciesIndex = np.zeros(len(usedFrequencies), dtype=int)
        nearestFrequencies = np.zeros(len(usedFrequencies), dtype=float)
        for i in range(len(usedFrequencies)):
            nearestIndex = np.argmin(abs(fileFrequencies-usedFrequencies[i]))
            nearestFrequenciesIndex[i] = nearestIndex
            nearestFrequencies[i] = fileFrequencies[nearestIndex]
        return nearestFrequencies, nearestFrequenciesIndex
    
    def __getDataOnFrequencies(self, searchHeader, fileHeaders, fileData, frequenciesIndex):
        headerIndex = self.__getHeaderIndex(searchHeader, fileHeaders)
        headerData = fileData[headerIndex]
        usedHeaderData = np.zeros(len(frequenciesIndex), dtype=float)
        for i in range (len(frequenciesIndex)):
            usedHeaderData[i] = headerData[frequenciesIndex[i]]
        return usedHeaderData
    
    def setImpedanceTensorErrorImag(self, errorValue):
        self.impedanceTensorErrorImag = errorValue
    
    def __getAllData(self):
        self.impedanceTensorHeaderDatasAll = []
        self.impedanceTensorHeaderErrorDatasAll = []
        self.nearestFrequenciesAll = np.zeros([len(self.inputFiles),len(self.usedFrequencies)], dtype=float)
        
        for fIndex, f in enumerate (self.inputFiles):
            pt1FilePath = os.path.join(self.pt1FolderPath, f)
            fileHeaders, fileData = self.__parse(pt1FilePath)
            
            # get nearest frequency
            fileFrequencyIndex = self.__getHeaderIndex(self.inputHeader["frequency"], fileHeaders)
            fileFrequencies = np.array(fileData[fileFrequencyIndex])            
            self.nearestFrequenciesAll[fIndex], nearestFrequenciesIndex = self.__getNearestFrequencyIndex(self.usedFrequencies, fileFrequencies)
            
            # get impedance tensor for each header
            impedanceTensorHeaderDatas = np.zeros([len(self.impedanceTensorHeaders), len(self.usedFrequencies)], dtype=float)
            for i in range (len(self.impedanceTensorHeaders)):
                impedanceTensorHeaderDatas[i] = self.__getDataOnFrequencies(self.impedanceTensorHeaders[i], fileHeaders, fileData, nearestFrequenciesIndex)
            self.impedanceTensorHeaderDatasAll.append(impedanceTensorHeaderDatas)

            # get impedance tensor error for each header
            impedanceTensorHeaderErrorDatas = np.zeros([len(self.impedanceTensorErrorHeaders), len(self.usedFrequencies)], dtype=float)
            lastImpedanceTensorError = np.zeros(len(self.usedFrequencies), dtype=float)
            for i in range (len(self.impedanceTensorErrorHeaders)):
                if self.impedanceTensorErrorHeaders[i] == '-' :
                    impedanceTensorErrorValue = np.zeros(len(self.usedFrequencies), dtype=float)
                    try:
                        impedanceTensorErrorValue[:] = float (self.impedanceTensorErrorImag)
                    except:
                        if self.impedanceTensorErrorImag.lower() == "=real":
                            impedanceTensorErrorValue = lastImpedanceTensorError
                        else:
                            impedanceTensorErrorValue[:] = np.nan
                else:
                    impedanceTensorErrorValue = self.__getDataOnFrequencies(self.impedanceTensorErrorHeaders[i], fileHeaders, fileData, nearestFrequenciesIndex)
                    impedanceTensorErrorValue = self.__vartoerr(impedanceTensorErrorValue)
                    lastImpedanceTensorError = impedanceTensorErrorValue
                impedanceTensorHeaderErrorDatas[i] = impedanceTensorErrorValue
            self.impedanceTensorHeaderErrorDatasAll.append(impedanceTensorHeaderErrorDatas)
    
    def __createDataOnF(self, data, headers):
        dataOnFrequencies =  np.zeros([len(self.usedFrequencies), len(self.inputFiles), len(headers)])
        for i in range (len(self.usedFrequencies)):
            for j in range (len(self.inputFiles)):
                for k in range (len(headers)):
                    dataOnFrequencies[i][j][k] = data[j][k][i]
        return dataOnFrequencies
        
    def initErrMapVal(self):
        nFrequency= len(self.usedFrequencies)
        nFile =  len(self.inputFiles)
        nITHeader = len(self.impedanceTensorHeaders)
        self.errMapVal = np.ones([nFrequency, nFile, nITHeader])
    
    def changeErrMapVal(self, changeDict):
        frequency_period_range = np.arange(1, len(self.usedFrequencies)+1)
        file_range = np.arange(1, len(self.inputFiles)+1)
        response_range = np.arange(1, len(self.impedanceTensorHeaders)+1)
        
        for ID in changeDict:
            frequency_period_id = changeDict[ID]["frequency_period"]
            files_id = changeDict[ID]["file"]
            responses_id = changeDict[ID]["response"]
            final_value = changeDict[ID]["final_value"]
            
            if isinstance(frequency_period_id, int) and frequency_period_id in frequency_period_range:
                pass
            else:
                raise ValueError("Invalid frequency/period id")
            
            if isinstance(files_id, str):
                if files_id=="all":
                    pass
                else:
                    raise ValueError("Invalid file id")
            elif isinstance(files_id, list):
                for file_id in files_id:
                    if isinstance(file_id, int) and file_id in file_range:
                        pass
                    else:
                        raise ValueError("Invalid file id")
            else:
                raise ValueError("Invalid file id")
                
            if isinstance(responses_id, str):
                if responses_id=="all":
                    pass
                else:
                    raise ValueError("Invalid response id")
            elif isinstance(responses_id, list):
                for response_id in responses_id:
                    if isinstance(response_id, int) and response_id in response_range:
                        pass
                    else:
                        raise ValueError("Invalid response id")
            else:
                raise ValueError("Invalid response id")

            if isinstance(final_value, int):
                pass
            else:
                raise ValueError("Invalid value")
            
            if (files_id=="all"):
                files_id = np.arange(len(self.errMapVal[0]))
            if (responses_id=="all"):
                responses_id = np.arange(len(self.errMapVal[0][0]))
            for file_id in files_id:
                for response_id in responses_id:
                    self.errMapVal[frequency_period_id-1][file_id-1][response_id-1] = final_value
        
    def __addFirstLinestr(self):
        self.outputStr += ' {} {} {}'.format(len(self.inputFiles), len(self.usedFrequencies),
                                             len(self.impedanceTensorHeaders))
    
    def __addDataOnFstr(self, headerOut, data):
        # get maximum character
        nCharData = 0
        negativeVal = False
        for i in range (len(self.usedFrequencies)):
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
        for i in range(len(self.usedFrequencies)):
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
        impedanceTensorOnF = self.__createDataOnF(self.impedanceTensorHeaderDatasAll, self.impedanceTensorHeaders)
        impedanceTensorErrorOnF = self.__createDataOnF(self.impedanceTensorHeaderErrorDatasAll, self.impedanceTensorErrorHeaders)
        
        self.__addFirstLinestr()
        self.__addCoordinatestr("Station_Location: N-S", self.northing)
        self.__addCoordinatestr("Station_Location: E-W", self.easting)
        self.__addDataOnFstr("DATA_Period:", impedanceTensorOnF)
        self.__addDataOnFstr("ERROR_Period:", impedanceTensorErrorOnF)
        self.__addDataOnFstr("ERMAP_Period:", self.errMapVal)
        
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

    def getSelectedValues(self):
        print()
        print("Select values: <\"frequency\"/\"period\"> <list of values>")
        selectedValues = []
        mode = ''
        while True:
            inputValues = self.getInput().split()
            for value in inputValues:
                value = value.lower()
                if value=="end":
                    if mode and len(selectedValues)>0:
                        self.newFile.setUsedValues(mode, selectedValues)
                        return True
                    else:
                        print("Invalid input")
                        if self.getSelectedValues():
                            return True

                elif value=="reset":
                    print("Input periods cleared")
                    if self.getSelectedValues():
                        return True
                else:
                    if mode:
                        try:
                            value = float(value)
                        except:
                            print("TypeError: value must be int/float")
                            if self.getSelectedValues():
                                return True
                        else:
                            selectedValues.append(value)
                    else:
                        if value=="frequency" or value=="period":
                            mode = value
                        else:
                            print("Invalid mode")
                            if self.getSelectedValues():
                                return True
    
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
        tableID = []
        for i in range(len(datas)):
            tableID.append(i+1)
        tableData = []
        for data in datas:
            try:
                float(data)
            except:
                data = data.replace(" (Rot)", "")
                data = data.replace(".pt1", "")
            tableData.append(data)        
        print(tabulate({"ID": tableID, name: tableData}, headers="keys", tablefmt="pretty", numalign="right"))        
        
    def breakErrMapStr(self, input_str): #(break "1_1-2_All_999")
        change_list = input_str.lower().split("_")

        if len(change_list)!=4:
            raise ValueError("Invalid input")

        try:
            change_list[0] = int(change_list[0])
        except:
            raise ValueError("Invalid frequency/period id")

        if change_list[1]=="all":
            pass
        else:
            change_list[1] = change_list[1].split("-")
            for i in range(len(change_list[1])):
                try:
                    change_list[1][i] = int(change_list[1][i])
                except:
                    raise ValueError("Invalid file id")

        if change_list[2]=="all":
            pass
        else:
            change_list[2] = change_list[2].split("-")
            for i in range(len(change_list[2])):
                try:
                    change_list[2][i] = int(change_list[2][i])
                except:
                    raise ValueError("Invalid response id")
        try:
            change_list[3] = int(change_list[3])
        except:
            raise ValueError("Invalid value id")

        changeErrMap = {
            "frequency_period": change_list[0], "file": change_list[1],
            "response": change_list[2], "final_value": change_list[3]
        }
        return changeErrMap
        
        
    
    def getErrorMap(self):
        self.newFile.initErrMapVal()
        print()
        print("Change Error Map Period? (y/n)")
        while(True):
            changeStatus = self.getInput().lower()
            if changeStatus=="n":
                return
            elif changeStatus=="y":
                print()
                if self.newFile.usedValuesMode == "frequency":
                    self.showErrMapParamTable(self.newFile.usedFrequencies, "Frequency")
                elif self.newFile.usedValuesMode == "period":
                    self.showErrMapParamTable(self.newFile.usedPeriods, "Period")
                print()
                self.showErrMapParamTable(self.newFile.getInputFiles(), "File")
                print()
                self.showErrMapParamTable(self.newFile.impedanceTensorHeaders, "Response")
                print()
                print("Input format: <{} id>_<files id>_<responses id>_<final value>".format(self.newFile.usedValuesMode))
                break
            else:
                print("Invalid input")

        changeParam = {}
        changeId = 0
        while(True):
            userInputs = self.getInput().lower().split()
            for userInput in userInputs:
                if userInput=="end":
                    if len(changeParam)>0:
                        try:
                            self.newFile.changeErrMapVal(changeParam)
                        except Exception as e:
                            print(e)
                            changeParam = {}
                            changeId = 0
                            print("Changes cleared")
                        else:
                            return
                    else:
                        print("Invalid input")

                elif userInput=="reset":
                    changeParam = {}
                    changeId = 0
                    print("Changes cleared")

                else:
                    try:
                        changeParam[changeId] = self.breakErrMapStr(userInput)
                    except Exception as e:
                        print(e)
                    else:
                        changeId+=1                
    
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
        print("\nSelected values:")
        
        print("Frequency:")
        for frequency in self.newFile.usedFrequencies:
            print("{:.4E}".format(frequency), end=' ')
        print("\nPeriod:")
        for period in self.newFile.usedPeriods:
            print("{:.4E}".format(period), end=' ')
        print()
        print("\nNearest values:")
        print("Frequency:")
        for i in range (len(self.newFile.inputFiles)):
            for frequency in self.newFile.nearestFrequenciesAll[i]:
                print("{:.4E}".format(frequency), end=' ')
            print("({})".format(self.newFile.inputFiles[i]))
        print("Period:")
        for i in range (len(self.newFile.inputFiles)):
            for frequency in self.newFile.nearestFrequenciesAll[i]:
                print("{:.4E}".format(1/frequency), end=' ')
            print("({})".format(self.newFile.inputFiles[i]))

        print("\nCoordinate header: {}".format(self.coordinateHeader))
        print("\nStation coordinate (UTM):")
        staCoordTableList = []
        for i in range(len(self.newFile.inputFiles)):
            staCoordTableList.append([self.newFile.inputFiles[i], self.staCoordinates[0][i], self.staCoordinates[1][i]])
        print(tabulate(staCoordTableList, headers=['Name', 'Easting', 'Northing'], floatfmt=".2f", tablefmt="pretty"))
        print("\nCenter of model:")
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
    userCLI.getSelectedValues()
    userCLI.getITImaginaryError()
    userCLI.getErrorMap()
    userCLI.getCoordinate()
    userCLI.fileProcess()
    userCLI.getFileSave()
    userCLI.displayResult()

if __name__ == "__main__":
    main()
