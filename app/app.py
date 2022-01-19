import os
import shutil
import webbrowser
from threading import Timer
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from module.data_file import StationCoordinate, CreateDataFile
from module.initial_model import CreateInitialModel
from module.prior_control_model import CreateControlModelIndex


class Parameter:
    def __init__(self):
        self.basePath = os.getcwd()
        self.createFolder()
        self.stationCoord = {}
        self.coordName = ""
        self.coordPath = ""
        self.staName = []
        self.staPath = ""
    def createFolder(self):
        self.uploadFolder = "uploads"
        if (os.path.isdir(self.uploadFolder)):
            try:
                shutil.rmtree(self.uploadFolder)
            except OSError as e:
                print ("Error: %s - %s." % (e.filename, e.strerror))
        os.makedirs(self.uploadFolder, exist_ok=True)
        self.uploadPath = os.path.join(self.basePath, self.uploadFolder)

        self.outputFolder = "outputs"
        os.makedirs(self.outputFolder, exist_ok=True)
        self.outputPath = os.path.join(self.basePath, self.outputFolder)

myParam = Parameter()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/uploadcoordinates', methods=['POST'])
def uploadCoordinates():
    file = request.files['myfile']
    myParam.coordName = secure_filename(file.filename)
    myParam.coordPath = os.path.join(myParam.uploadPath, myParam.coordName)
    file.save(myParam.coordPath)
    mySta = StationCoordinate(myParam.coordPath)
    stationCoord = mySta.getStationInput()
    return jsonify(stationCoord)

@app.route('/uploadstations', methods=['POST'])
def uploadStations():
    files = request.files.getlist("file[]")
    myParam.staName = []
    for file in files:
        myParam.staName.append(file.filename)
        myParam.staPath = os.path.join(myParam.uploadPath, file.filename)
        file.save(myParam.staPath)
    return jsonify(myParam.staName)

@app.route('/dfsave', methods=['POST'])
def dfsave():
    return dfProcess("save")

@app.route('/dfpreview', methods=['POST'])
def dfpreview():
    return dfProcess("preview")

def dfProcess(mode):
    input_json = request.get_json(force=True)
    mCenter = input_json["mCenterLatLng"]
    usedValues = input_json["usedValues"]
    nResponse = input_json["nResponse"]
    errPeriod = input_json["errPeriod"]
    errMapChange = input_json["errMap"]
    saveName = input_json["saveName"]

    # create data file obj
    newFile = CreateDataFile()
    newFile.setInputDirectory(myParam.uploadFolder)
    os.chdir(myParam.uploadPath)
    newFile.setInputFiles(myParam.staName)
    newFile.setResponses(nResponse)
    newFile.setUsedValues(usedValues["mode"], usedValues["value"])
    newFile.setImpedanceTensorErrorImag(errPeriod)
    newFile.initErrMapVal()
    if errMapChange:
        newFile.changeErrMapVal(errMapChange)
    os.chdir(newFile.basePath)
    coordFPath = os.path.join(myParam.uploadFolder, myParam.coordName)
    staCoordinate = StationCoordinate(coordFPath)
    staCoordinate.setUsedStation(newFile.getInputFiles())
    staCoordinate.createCoordinateUTM()
    staCenterEasting, staCenterNorthing = staCoordinate.latLngToUTM(mCenter["lat"], mCenter["lng"])
    staCoordinate.recenterCoordinate(staCenterEasting, staCenterNorthing)
    newFile.setCoordinate(staCoordinate.easting0, staCoordinate.northing0)

    newFile.process()

    if mode=="save":
        saveFPath = os.path.join(myParam.outputFolder, saveName)
        newFile.save(saveFPath)
        return ""
    elif mode=="preview":
        return newFile.outputStr

@app.route('/imsave', methods=['POST'])
def imsave():
    return imProcess("save")
@app.route('/impreview', methods=['POST'])
def impreview():
    return imProcess("preview")

def imProcess(mode):
    input_json = request.get_json(force=True)
    blockRI = input_json["blockRI"]
    blockXY = input_json["blockXY"]
    blockZ = input_json["blockZ"]
    mTitle = input_json["title"]
    resistivity = input_json["resistivity"]
    nr = input_json["nr"]
    saveName = input_json["saveName"]

    myIM = CreateInitialModel()
    myIM.title = mTitle
    blockWE = myIM.createBlockXY(mode="manual", side1=blockXY["CW"], side2=blockXY["CE"])
    blockSN = myIM.createBlockXY(mode="manual", side1=blockXY["CS"], side2=blockXY["CN"])

    myIM.blockSizeX = blockSN
    myIM.blockSizeY = blockWE
    myIM.blockSizeZ = blockZ
    myIM.nr = nr
    myIM.resistivityValue = resistivity
    myIM.resistivityIndexLayer = blockRI["id"]
    myIM.lriLValues = blockRI["value"]

    myIM.blockColX = 8
    myIM.blockColY = 8
    myIM.blockColZ = 8

    myIM.createOutput()

    if mode=="save":
        saveFPath = os.path.join(myParam.outputFolder, saveName)
        myIM.save(saveFPath)
        return ""
    elif mode=="preview":
        return myIM.strOutput
    

@app.route('/cmsave', methods=['POST'])
def pmsave():
    return pmProcess("save")

@app.route('/cmpreview', methods=['POST'])
def pmpreview():
    return pmProcess("preview")

def pmProcess(mode):
    input_json = request.get_json(force=True)
    nx = input_json["nx"]
    ny = input_json["ny"]
    nz = input_json["nz"]
    blockCMI = input_json["layerCMI"]
    saveName = input_json["saveName"]

    myCMI = CreateControlModelIndex()
    myCMI.nx = nx
    myCMI.ny = ny
    myCMI.nz = nz
    myCMI.layerRangeList = blockCMI["id"]
    myCMI.IFLValues = blockCMI["value"]
    myCMI.createOutputStr()

    if mode=="save":
        saveFPath = os.path.join(myParam.outputFolder, saveName)
        myCMI.save(saveFPath)
        return ""

    elif mode=="preview":
        return myCMI.strOutput

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new("http://127.0.0.1:2000/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=2000)

# debug: export FLASK_ENV=development
