class Parameter {
    constructor() {
        this.imCellsVal = null;
        this.imCellsValDesign = null;
        this.pmCellsVal = null;
        this.pmCellsValDesign = null;
        this.lastCellsVal = null;
        //init im cell val
    }
    // DATAFILE //
    getErrMapParam() {
        var errmapPeriodSelects = document.getElementsByClassName("errmap-period-select");
        var errmapStaInputs = document.getElementsByClassName("errmap-station-input");
        var errmapRespInputs = document.getElementsByClassName("errmap-response-input");
        var errmapValInputs = document.getElementsByClassName("errmap-value-input");
        var dfErrmapModeSelect = document.getElementById("df-errmap-period-mode-select");
        
        if (dfErrmapModeSelect.value==="none") {
            return false
        } else if (dfErrmapModeSelect.value==="change") {
            var errMapChange = {}
            for (var i=0; i<errmapPeriodSelects.length; i++) {
                var cPeriod = this.parseInput(errmapPeriodSelects[i].value, "int")[0];
                if (errmapStaInputs[i].value.replace(" ", "").toLowerCase()==="all") {
                    var cStation = "all";
                } else {
                    var cStation = this.parseInput(errmapStaInputs[i].value, "int");
                }
                if (errmapRespInputs[i].value.replace(" ", "").toLowerCase()==="all") {
                    var cResponse = "all";
                } else {
                    var cResponse = this.parseInput(errmapRespInputs[i].value, "int");
                }
                var cValue = this.parseInput(errmapValInputs[i].value, "int")[0];
    
                errMapChange[i] = { "period": cPeriod, "station": cStation,
                                    "response": cResponse, "value": cValue };
            }
            return errMapChange;
        }
        

    }
    // END DATAFILE //
    
    // PRIOR MODEL //
    getpmIndexColor() {
        this.pmIndexColors = [];
        var pmitColorEls = document.getElementsByClassName("pmit-color-input");
        for (var i=0; i<pmitColorEls.length; i++) {
            this.pmIndexColors.push(pmitColorEls[i].value);
        }
    }
    getpmShowLayer() {
        var imShowLayerValStr = document.getElementById("pm-show-layer-select").value;
        if (imShowLayerValStr === "design") {
            return imShowLayerValStr;
        } else {
            return parseInt(imShowLayerValStr);
        }
    }
    getpmChangeL() {
        var pmcmiClMode = document.getElementById("pm-cmi-al-mode-select");
        if (pmcmiClMode.value === "single") {
            var singleLayerSelected = parseInt(document.getElementById("pm-cmi-cl-layer-single-select").value);
            var layerSelected = [singleLayerSelected]
        } else if (pmcmiClMode.value === "multiple") {
            var msLayerSelected = parseInt(document.getElementById("pm-cmi-al-layer-ms-select").value);
            var meLayerSelected = parseInt(document.getElementById("pm-cmi-al-layer-me-select").value);
            var layerSelectedFL = [msLayerSelected, meLayerSelected];
            layerSelectedFL.sort((a, b) => a - b);
            var layerSelected = [];
            for (var i=layerSelectedFL[0]; i<=layerSelectedFL[1]; i++) {
                layerSelected.push(i);
            }
        }
        return layerSelected;
    }
    getpmInitialCells() {
        var pmSILayerSelect = document.getElementById("pm-cmi-si-layer-select").value;
        if (pmSILayerSelect != "all" && pmSILayerSelect != "design") {
            pmSILayerSelect = parseInt(pmSILayerSelect);
        }
        var pmSI = {
            layer: pmSILayerSelect,
            value: parseInt(document.getElementById("pm-cmi-si-value-select").value)
        };
        return pmSI;
    }
    getpmSaveName() {
        var fname = document.getElementById("pm-output-fname-textarea").value;
        return fname

    }
    // END PRIOR MODEL //

    // START INITIAL MODEL //
    getimTitle() {
        var title = document.getElementById("im-title-textarea").value;
        return title;
    }
    getimSaveName() {
        var fname = document.getElementById("im-output-fname-textarea").value;
        return fname;
    }
    getIMRes() {
        var nr = parseInt (document.getElementById("im-r-number-text").value);
        var resistivity = {ids:[], values:[], colors: [], number: nr};
        var imResTextEls = document.getElementsByClassName("im-r-val-text");
        for (var i=0; i<imResTextEls.length; i++) {
            var iValStr = imResTextEls[i].value.replace(/\s/g,'');
            if (iValStr != '') {
                resistivity.values.push(parseFloat(iValStr));
            }
        }
        var imResColorEls = document.getElementsByClassName("imrt-color-input");
        for (var i=0; i<imResColorEls.length; i++) {
            resistivity.colors.push(imResColorEls[i].value);
        }
        var imResNoEls = document.getElementsByClassName("imrt-no");
        for (var i=0; i<imResNoEls.length; i++) {
            resistivity.ids.push(i+1);
        }
        return resistivity;
    }
    getimShowLayer() {
        var imShowLayerValStr = document.getElementById("im-show-layer-select").value;
        if (imShowLayerValStr === "design") {
            return imShowLayerValStr;
        } else {
            return parseInt(imShowLayerValStr);
        }
    }
    setCellVal(layers, imCellsVal, cellsValOut) {
        if (cellsValOut==null) {
            alert("Initial value is null");
            return null;
        }
        for (var i=0; i<layers.length; i++) {
            cellsValOut[layers[i]-1] = imCellsVal;
        }
        return cellsValOut;
    }
    getimChangeL() {
        var imlriClMode = document.getElementById("im-lri-al-mode-select");
        if (imlriClMode.value === "single") {
            var singleLayerSelected = parseInt(document.getElementById("im-lri-al-layer-single-select").value);
            var layerSelected = [singleLayerSelected]
        } else if (imlriClMode.value === "multiple") {
            var msLayerSelected = parseInt(document.getElementById("im-lri-al-layer-ms-select").value);
            var meLayerSelected = parseInt(document.getElementById("im-lri-al-layer-me-select").value);
            var layerSelectedFL = [msLayerSelected, meLayerSelected];
            layerSelectedFL.sort((a, b) => a - b);
            var layerSelected = [];
            for (var i=layerSelectedFL[0]; i<=layerSelectedFL[1]; i++) {
                layerSelected.push(i);
            }
        }
        return layerSelected;
    }
    setInitialCellsVal(layer, val, nLayer, nCell, cellsValOut) {
        if (Number.isNaN(val)) {
            alert("value is NaN");
            return null;
        }
        if (cellsValOut === null) {
            cellsValOut = new Array(nLayer);
        }
        if (layer==="all") {
            for (var i=0; i<nLayer; i++) {
                cellsValOut[i] = Array.apply(null, Array(nCell)).map(Number.prototype.valueOf, val);
            }
        } else if (layer==="design") {
            var cellsValDesign = Array.apply(null, Array(nCell)).map(Number.prototype.valueOf, val);
            return cellsValDesign;
        } 
        else {
            cellsValOut[layer-1] = Array.apply(null, Array(nCell)).map(Number.prototype.valueOf, val);
        }
        return cellsValOut;
    }
    getimInitialCells() {
        var imSILayerSelect = document.getElementById("im-lri-si-layer-select").value;
        if (imSILayerSelect != "all" && imSILayerSelect != "design") {
            imSILayerSelect = parseInt(imSILayerSelect);
        }
        var imSILayer = {
            layer: imSILayerSelect,
            value: parseInt(document.getElementById("im-lri-si-value-select").value)
        };
        return imSILayer;
    }
    getimCLCellVal() {
        var cellVal = parseInt(document.getElementById("im-lri-cl-value-select").value);
        return cellVal;
    }
    getimCellColor(idx) {
        var imResColorEls = document.getElementsByClassName("imrt-color-input");
        var colorVal = imResColorEls[idx-1].value;
        return colorVal;
    }
    // END INITIAL MODEL //

    getdfSaveName() {
        var fname = document.getElementById("df-output-fname-textarea").value;
        return fname;
    }
    getdfErrorPeriod() {
        var dfErrorPeriod = null;
        var selectErrPeriod = document.getElementById("errperiod-select");
        if (selectErrPeriod.value==="=real") {
            dfErrorPeriod = "=real"
        } else if (selectErrPeriod.value==="manual"){
            dfErrorPeriod = document.getElementById("manual-errperiod-text").value;
        }
        return dfErrorPeriod;

    }
    getdfPeriod() {
        var dfPeriods = [];
        var table = document.getElementById("df-period-table");
        var dfPeriodValInputs = document.getElementsByClassName("df-period-inputs");
        for (var i=0; i<dfPeriodValInputs.length; i++) {
            var cellValueStr = dfPeriodValInputs[i].value.replace(/\s/g,'')
            if (cellValueStr != '') {
                dfPeriods.push(parseFloat(cellValueStr));
            }
        }
        return dfPeriods;
    }
    getBundaries() {
        let latSW = document.getElementById("textBoundSWlat").value;
        let lngSW = document.getElementById("textBoundSWlng").value;
        let latNE = document.getElementById("textBoundNElat").value;
        let lngNE = document.getElementById("textBoundNElng").value;
        this.boundaries = {
            point1: [latSW, lngSW],
            point2: [latNE, lngNE]
        };
    }
    getModelCenter() {
        this.modelCenter = {
            mode: document.getElementById("selectModelCenterMode").value,
            latManual: document.getElementById("textModelCenterLat").value,
            lngManual: document.getElementById("textModelCenterLng").value
        };
    }
    parseInputToStr(dataStr) {
        return dataStr.replace(" ", '');
    }
    parseInput(dataStr, outType) {
        let dataList = [];
        let inputDataListStr = dataStr.split(/\s+/g);
        for (var i=0; i<inputDataListStr.length; i++) {
            if (inputDataListStr[i] != '') {
                if (outType==="float") {
                    dataList.push(parseFloat(inputDataListStr[i]));
                } else if (outType==="int") {
                    dataList.push(parseInt(inputDataListStr[i]));
                }
            }
        }
        return (dataList);
    }
    sumBlock(blockList) {
        let lastSize = 0;
        let blockSum = [];
        for (var i=0; i<blockList.length; i++) {
            lastSize += blockList[i];
            blockSum.push(lastSize);
        }
        return (blockSum);
    }
    breakSumBlock(blockList) {
        let blockBreak = [blockList[0]];
        for (var i=1; i<blockList.length; i++) {
            blockBreak.push(blockList[i]-blockList[i-1])
        }
        return (blockBreak);
    }
    getBlockXY() {
        let textInput = {
            CN: document.getElementById("CN-textarea"),
            CS: document.getElementById("CS-textarea"),
            CE: document.getElementById("CE-textarea"),
            CW: document.getElementById("CW-textarea")
        }
        let inputBlock = {
            CN: this.parseInput(textInput.CN.value, "float"),
            CS: this.parseInput(textInput.CS.value, "float"),
            CE: this.parseInput(textInput.CE.value, "float"),
            CW: this.parseInput(textInput.CW.value, "float")
        }
        let inputBlockMode = {
            CN: document.getElementById("CN-mode-select").value,
            CS: document.getElementById("CS-mode-select").value,
            CE: document.getElementById("CE-mode-select").value,
            CW: document.getElementById("CW-mode-select").value
        };
        if (inputBlockMode.CN != "manual") {
            inputBlock.CN = inputBlock[inputBlockMode.CN];
            textInput.CN.value = "";
        }
        if (inputBlockMode.CS != "manual") {
            inputBlock.CS = inputBlock[inputBlockMode.CS];
            textInput.CS.value = "";
        }
        if (inputBlockMode.CE != "manual") {
            inputBlock.CE = inputBlock[inputBlockMode.CE];
            textInput.CE.value = "";
        }
        if (inputBlockMode.CW != "manual") {
            inputBlock.CW = inputBlock[inputBlockMode.CW];
            textInput.CW.value = "";
        }
        let mode = document.getElementById("block-xy-mode-select").value;
        this.blockXY = {
            size: {CN: null, CS: null, CE: null, CW: null},
            distance: {CN: null, CS: null, CE: null, CW: null}
        };
        if (mode==="size") {
            this.blockXY.size = {
                CN: inputBlock.CN,
                CS: inputBlock.CS,
                CE: inputBlock.CE,
                CW: inputBlock.CW
            };
            this.blockXY.distance = {
                CN: this.sumBlock(inputBlock.CN),
                CS: this.sumBlock(inputBlock.CS),
                CE: this.sumBlock(inputBlock.CE),
                CW: this.sumBlock(inputBlock.CW)
            };
        } else if (mode==="distance"){
            this.blockXY.size = {
                CN: this.breakSumBlock(inputBlock.CN),
                CS: this.breakSumBlock(inputBlock.CS),
                CE: this.breakSumBlock(inputBlock.CE),
                CW: this.breakSumBlock(inputBlock.CW)
            };
            this.blockXY.distance = {
                CN: inputBlock.CN,
                CS: inputBlock.CS,
                CE: inputBlock.CE,
                CW: inputBlock.CW
            };
        }
    }
    getBlockXYLatLng(distanceObj, modelBoundary, modelCenter) {
        let centerE = L.latLng(modelCenter.lat, modelBoundary.east);
        let centerW = L.latLng(modelCenter.lat, modelBoundary.west);
        let centerN = L.latLng(modelBoundary.north, modelCenter.lng);
        let centerS = L.latLng(modelBoundary.south, modelCenter.lng);

        var blockLinePoint = [];

        this.blockCells = {
            lat: [modelCenter.lat],
            lng: [modelCenter.lng]
        };

        // Center-North
        for (var i=0; i<distanceObj.CN.length; i++) {
            var distance = distanceObj.CN[i];
            var destinationPointW = L.GeometryUtil.destination(centerW, 0, distance);
            var destinationPointE = L.GeometryUtil.destination(centerE, 0, distance);
            blockLinePoint.push([destinationPointW, destinationPointE]);

            this.blockCells.lat.push(destinationPointW.lat);
        }
        // Center-South
        for (var i=0; i<distanceObj.CS.length; i++) {
            var distance = distanceObj.CS[i];
            var destinationPointW = L.GeometryUtil.destination(centerW, 180, distance);
            var destinationPointE = L.GeometryUtil.destination(centerE, 180, distance);
            blockLinePoint.push([destinationPointW, destinationPointE]);

            this.blockCells.lat.push(destinationPointW.lat);

        }
        // Center-East
        for (var i=0; i<distanceObj.CE.length; i++) {
            var distance = distanceObj.CE[i];
            var destinationPointN = L.GeometryUtil.destination(centerN, 90, distance);
            var destinationPointS = L.GeometryUtil.destination(centerS, 90, distance);
            blockLinePoint.push([destinationPointN, destinationPointS]);

            this.blockCells.lng.push(destinationPointN.lng)
        }
        // Center-West
        for (var i=0; i<distanceObj.CW.length; i++) {
            var distance = distanceObj.CW[i];
            var destinationPointN = L.GeometryUtil.destination(centerN, 270, distance);
            var destinationPointS = L.GeometryUtil.destination(centerS, 270, distance);
            blockLinePoint.push([destinationPointN, destinationPointS]);

            this.blockCells.lng.push(destinationPointN.lng)
        }

        this.blockCells.lng.sort((a, b) => a - b);
        this.blockCells.lat.sort((a, b) => a - b).reverse();

        return (blockLinePoint);
    }
    getCenterGrid() {
        //pass
    }
    getBlockZ() {
        let textInput = document.getElementById("block-z-textarea");
        let inputBlock = this.parseInput(textInput.value, "float");
        let mode = document.getElementById("block-z-mode-select").value;
        this.blockZ = {id:null, size: null, distance: null};
        if (mode==="size") {
            this.blockZ.size = inputBlock;
            this.blockZ.distance = this.sumBlock(inputBlock);
        } else if (mode==="distance"){
            this.blockZ.size = this.breakSumBlock(inputBlock)
            this.blockZ.distance = inputBlock;
        }
        this.blockZ.id = Array.from({length: this.blockZ.size.length}, (_, i) => i + 1);
    }

}

function numberRange(start, end) {
    return new Array(end - start).fill().map((d, i) => i + start);
}

function compareArr(arr1, arr2) {
    if (arr1.length != arr2.length) {
        return false;
    }
    for (var i=0; i<arr1.length; i++) {
        if (arr1[i] != arr2[i]) {
            return false;
        }
    }
    return true;
}

function compressLayer(id, val) {
    var result = {id: [], value: []};
    var lastCellVal = [null];
    var sameIDTemp = [];

    for (var i=0; i<val.length; i++) {
        if (!compareArr(lastCellVal, val[i])) {
            //cell
            result.value.push(val[i]);
            lastCellVal = val[i];
            //layer
            result.id.push([id[i]]);
        } else {
            var lastIDidx = result.id.length-1;
            if (result.id[lastIDidx].length==1) {
                result.id[lastIDidx].push(id[i]);
            } else {
                result.id[lastIDidx][1] = id[i];
            }
        }
    }
    return result;
}