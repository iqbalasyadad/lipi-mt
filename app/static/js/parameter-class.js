class Parameter {
    constructor() {
        this.imCellsVal = null;
        this.cmCellsVal = null;
        this.lastCellsVal = null;
        //init im cell val
    }
    // DATAFILE //
    getdfErrMapParam() {
        var errmapPeriodSelects = document.getElementsByClassName("errmap-used-value-select");
        var errmapStaInputs = document.getElementsByClassName("errmap-file-input");
        var errmapRespInputs = document.getElementsByClassName("errmap-response-input");
        var errmapValInputs = document.getElementsByClassName("errmap-value-input");
        var dfErrmapModeSelect = document.getElementById("df-errmap-period-mode-select");
        
        if (dfErrmapModeSelect.value==="none") {
            return false
        } else if (dfErrmapModeSelect.value==="change") {
            var errMapChange = {}
            for (var i=0; i<errmapPeriodSelects.length; i++) {
                var cUsedValues = this.parseInput(errmapPeriodSelects[i], "int");
                if (errmapStaInputs[i].value.replace(" ", "").toLowerCase()==="all") {
                    var cFile = "all";
                } else {
                    var cFile = this.parseInputs(errmapStaInputs[i], "int");
                }
                if (errmapRespInputs[i].value.replace(" ", "").toLowerCase()==="all") {
                    var cResponse = "all";
                } else {
                    var cResponse = this.parseInputs(errmapRespInputs[i], "int");
                }
                var cValue = this.parseInput(errmapValInputs[i], "int");
    
                errMapChange[i] = { "frequency_period": cUsedValues, "file": cFile,
                                    "response": cResponse, "final_value": cValue };
            }
            return errMapChange;
        }
    }
    // END DATAFILE //
    
    // START CONTROL MODEL //
    getcmIndexColor() {
        var pmIndexColors = [];
        var pmitColorEls = document.getElementsByClassName("cmit-color-input");
        for (var i=0; i<pmitColorEls.length; i++) {
            pmIndexColors.push(pmitColorEls[i].value);
        }
        return pmIndexColors;
    }
    getcmShowLayer() {
        var imShowLayerValStr = document.getElementById("cm-show-layer-select").value;
        if (imShowLayerValStr === "design") {
            return imShowLayerValStr;
        } else {
            return parseInt(imShowLayerValStr);
        }
    }
    getcmChangeL() {
        var pmcmiClMode = document.getElementById("cm-cmi-al-mode-select");
        if (pmcmiClMode.value === "single") {
            var singleLayerSelected = parseInt(document.getElementById("cm-cmi-al-layer-single-select").value);
            var layerSelected = [singleLayerSelected]
        } else if (pmcmiClMode.value === "multiple") {
            var msLayerSelected = parseInt(document.getElementById("cm-cmi-al-layer-ms-select").value);
            var meLayerSelected = parseInt(document.getElementById("cm-cmi-al-layer-me-select").value);
            var layerSelectedFL = [msLayerSelected, meLayerSelected];
            layerSelectedFL.sort((a, b) => a - b);
            var layerSelected = [];
            for (var i=layerSelectedFL[0]; i<=layerSelectedFL[1]; i++) {
                layerSelected.push(i);
            }
        }
        return layerSelected;
    }
    getcmInitialCells() {
        var pmSILayerSelect = document.getElementById("cm-cmi-si-layer-select").value;
        if (pmSILayerSelect != "all" && pmSILayerSelect != "design") {
            pmSILayerSelect = parseInt(pmSILayerSelect);
        }
        var pmSI = {
            layer: pmSILayerSelect,
            value: parseInt(document.getElementById("cm-cmi-si-value-select").value)
        };
        return pmSI;
    }
    getcmSaveName() {
        var fname = document.getElementById("cm-output-fname-textarea").value;
        return fname

    }
    // END CONTROL MODEL //

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
        var resistivity = {ids:[], values:[], colors: [], number: null};
        var imResTextEls = document.getElementsByClassName("im-r-val-text");
        for (var i=0; i<imResTextEls.length; i++) {
            var imResVal = this.parseInput(imResTextEls[i], "float");
            resistivity.values.push(imResVal);
        }
        resistivity.number = resistivity.values.length;
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
            cellsValOut = new Array(nLayer);
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
        var modeSelect = document.getElementById("df-errperiod-select");

        if (modeSelect.value==="=real") {
            dfErrorPeriod = "=real"
        } else if (modeSelect.value==="manual"){
            dfErrorPeriod = document.getElementById("df-errperiod-text").value;
        }
        return dfErrorPeriod;

    }
    getdfUsedValue() {
        var usedValue = {
            mode: document.getElementById("df-used-value-mode-select").value,
            value: []
        }
        var dfPeriodValInputs = document.getElementsByClassName("df-used-value-inputs");
        for (var i=0; i<dfPeriodValInputs.length; i++) {
            usedValue.value.push(this.parseInput(dfPeriodValInputs[i], "float"));
        }
        return usedValue;
    }
    getModelBoundary() {
        var sw_lat_text = document.getElementById("boundary-sw-lat-text");
        var sw_lng_text = document.getElementById("boundary-sw-lng-text");
        var ne_lat_text = document.getElementById("boundary-ne-lat-text");
        var ne_lng_text = document.getElementById("boundary-ne-lng-text");

        this.boundary = {
            sw: {
                lat: this.parseInput(sw_lat_text, "float"),
                lng: this.parseInput(sw_lng_text, "float")                
            },
            ne: {
                lat: this.parseInput(ne_lat_text, "float"),
                lng: this.parseInput(ne_lng_text, "float")               
            }
        };
    }
    getModelCenter() {
        this.modelCenter = {
            mode: document.getElementById("model-center-mode-select").value,
            lat: this.parseInput(document.getElementById("model-center-lat-text"), "float"),
            lng: this.parseInput(document.getElementById("model-center-lng-text"), "float")
        };
    }
    parseInput(el, outType) {
        var val = el.value.replace(/\s/g,'');
        if (val === '') {
            alert("Error: empty parameter");
        } else {
            if (outType==="int") {
                return parseInt(val);
            } else if (outType==="float") {
                return parseFloat(val);
            }
        }
    }
    parseInputs(el, outType) {
        let dataList = [];
        let inputDataListStr = el.value.split(/\s+/g);
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
            CN: this.parseInputs(textInput.CN, "float"),
            CS: this.parseInputs(textInput.CS, "float"),
            CE: this.parseInputs(textInput.CE, "float"),
            CW: this.parseInputs(textInput.CW, "float")
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
            input_mode: mode,
            block_mode: {
                CN: document.getElementById("CN-mode-select").value,
                CS: document.getElementById("CS-mode-select").value,
                CE: document.getElementById("CE-mode-select").value,
                CW: document.getElementById("CW-mode-select").value
            },
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
        let inputBlock = this.parseInputs(textInput, "float");
        let inputMode = document.getElementById("block-z-mode-select").value;
        this.blockZ = {input_mode: inputMode, id: null, size: null, distance: null};
        if (inputMode==="size") {
            this.blockZ.size = inputBlock;
            this.blockZ.distance = this.sumBlock(inputBlock);
        } else if (inputMode==="distance"){
            this.blockZ.size = this.breakSumBlock(inputBlock)
            this.blockZ.distance = inputBlock;
        }
        this.blockZ.id = Array.from({length: this.blockZ.size.length}, (_, i) => i + 1);
    }
    getIMCMReplace() {
        // var replaceIMCM = {im:[], cm:[]}
        var replaceIMCM = {};

        var useIMCMIM = document.getElementsByClassName("cm-cmi-use-im-im");
        var useIMCMSelects = document.getElementsByClassName("cm-cmi-use-im-cm-select");
        for (var i=0; i<useIMCMSelects.length; i++) {
            var key = parseInt(useIMCMIM[i].innerHTML);
            replaceIMCM[key] = this.parseInput(useIMCMSelects[i], "int");
        }
        return replaceIMCM;
    }
    replaceCMVals(inputVals, rFormat) {
        var nLayer = inputVals.length;
        var nCell = inputVals[0].length;

        var outputVals = new Array(nLayer);
        for (var i=0; i<nLayer; i++) {
            outputVals[i] = Array.apply(null, Array(nCell)).map(Number.prototype.valueOf, 0);
        }
        for (var i=0; i<inputVals.length; i++) {
            for (var j=0; j<inputVals[i].length; j++) {
                var key = (inputVals[i][j]).toString();
                outputVals[i][j] = rFormat[key];
            }
        }
        return outputVals;
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