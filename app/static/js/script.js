window.onload = function() {
    let myParam = new Parameter();
    let myWindow = new MainWindow();
    let myMap = new Map();
    let myModel = new Model();

    document.getElementById("df-period-apply-btn").onclick = function() {
        var selectedPeriods = myParam.getdfPeriod();
        var errMapSelect = document.getElementsByClassName("errmap-period-select");

        errMapPeriodIdSelect = numberRange(1, selectedPeriods.length+1)
        myWindow.updateOptions(errMapSelect, "class", errMapPeriodIdSelect, errMapPeriodIdSelect);
    };
    // document.getElementById("df-errperiod-apply-btn").onclick = function() {
    //     console.log(myParam.getdfErrorPeriod());
    // };
    document.getElementById("hide-panel-left-btn").onclick = function() {
        var leftPanel = document.getElementById("cmc2l-panel-container");
        leftPanelStyle = leftPanel.currentStyle || window.getComputedStyle(leftPanel);
        if (leftPanelStyle.display === 'block') {leftPanel.style.display = 'none';} 
        else {leftPanel.style.display = 'block';}
    };
    document.getElementById("hide-panel-right-btn").onclick = function() {
        var rightPanel = document.getElementById("cmc2r-panel-container");
        rightPanelStyle = rightPanel.currentStyle || window.getComputedStyle(rightPanel);
        if (rightPanelStyle.display === 'block') {rightPanel.style.display = 'none';} 
        else {rightPanel.style.display = 'block';}
    };
    var drawRect = new L.Draw.Rectangle(myMap.map);
    document.getElementById("boundary-draw-btn").addEventListener("click", ()=> {
        var rectOptions = {
            showArea: false,
            shapeOptions: {
                fill: false,
                color: "blue",
                weight: 2
            }
        };
        drawRect.enable();
        drawRect.setOptions(rectOptions);
    });
    myMap.map.on('draw:created', function (e) {
        var type = e.layerType
        if (type === 'rectangle') {
            var layer = e.layer;
            document.getElementById("textBoundSWlat").value = layer.getBounds().getSouthWest().lat.toFixed(8);
            document.getElementById("textBoundSWlng").value = layer.getBounds().getSouthWest().lng.toFixed(8);
            document.getElementById("textBoundNElat").value = layer.getBounds().getNorthEast().lat.toFixed(8);
            document.getElementById("textBoundNElng").value = layer.getBounds().getNorthEast().lng.toFixed(8);

            myParam.getBundaries();
            myModel.boundary.sw = myParam.boundaries.point1;
            myModel.boundary.ne = myParam.boundaries.point2;
            myMap.plotModelBoundary(myModel.boundary.sw, myModel.boundary.ne);
        }
    });
    document.getElementById("boundary-plot-btn").onclick = function() {
        myParam.getBundaries();
        myModel.boundary.sw = myParam.boundaries.point1;
        myModel.boundary.ne = myParam.boundaries.point2;
        myMap.plotModelBoundary(myModel.boundary.sw, myModel.boundary.ne);
    };
    document.getElementById("boundary-delete-btn").onclick = function() {
        if (myMap.resetOverlay(myMap.modelBoundaryOverlay, "Boundary")) {
            myMap.modelBoundaryOverlay = null
        }
    };
    document.getElementById("model-center-plot-btn").onclick = function() {
        myParam.getModelCenter();
        let mode = myParam.modelCenter.mode;
        myMap.plotModelCenter(mode, myParam.modelCenter.latManual, myParam.modelCenter.lngManual);
    };
    document.getElementById("model-center-delete-btn").onclick = function() {
        if (myMap.resetOverlay(myMap.centerAxisOverlay, "Model Center")) {
            myMap.centerAxisOverlay = null;
        }
    };
    document.getElementById("block-xy-delete-btn").onclick = function() {
        if (myMap.resetOverlay(myMap.blockLineOverlay, "Block Line")) {
            myMap.blockLineOverlay = null;
        }
        if (myMap.resetOverlay(myMap.imBlockCellsOverlay, "Initial Model")) {
            myMap.imBlockCellsOverlay = null;
        }
        if (myMap.resetOverlay(myMap.pmBlockCellsOverlay, "Prior Model")) {
            myMap.pmBlockCellsOverlay = null;
        }
    };
    document.getElementById("block-xy-ok-btn").onclick = function() {
        myParam.getBlockXY();
        myModel.blockXY.size = myParam.blockXY.size;
        myModel.blockXY.distance = myParam.blockXY.distance;

        // create block line
        myModel.blockLatLngList = myParam.getBlockXYLatLng(myModel.blockXY.distance, myMap.modelBoundLatLng, myMap.modelCenter);
        myMap.plotBlockLine(myModel.blockLatLngList);
        if (myMap.imBlockCellsOverlay != null) {
            myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            myMap.imBlockCellsOverlay = null;
        }
        if (myMap.pmBlockCellsOverlay != null) {
            myMap.removeOverlay(myMap.pmBlockCellsOverlay, myMap.bcName.pri);
            myMap.pmBlockCellsOverlay = null;
        }
    };

    // OK BUTTON BLOCK Z //
    document.getElementById("block-z-ok-btn").onclick = function() {
        myParam.getBlockZ();

        var imLRICLLayerSelect = document.getElementsByClassName("im-lri-al-layer-select");
        myWindow.updateOptions(imLRICLLayerSelect, "class", myParam.blockZ.id, myParam.blockZ.id)

        var impmSILayerSelectOptText = ["all", "design"];
        impmSILayerSelectOptText.push.apply(impmSILayerSelectOptText, myParam.blockZ.id);
        var impmSILayerSelectOptVal = ["all", "design"];
        impmSILayerSelectOptVal.push.apply(impmSILayerSelectOptVal, myParam.blockZ.id);

        var imLRISILayerSelect = document.getElementById("im-lri-si-layer-select");
        myWindow.updateOptions(imLRISILayerSelect, "id", impmSILayerSelectOptText, impmSILayerSelectOptVal);

        var impmShowLayerSelectOptText = ["design"];
        impmShowLayerSelectOptText.push.apply(impmShowLayerSelectOptText, myParam.blockZ.id);
        var impmShowLayerSelectOptVal = ["design"];
        impmShowLayerSelectOptVal.push.apply(impmShowLayerSelectOptVal, myParam.blockZ.id);

        var imShowLayerSelect = document.getElementById("im-show-layer-select");
        myWindow.updateOptions(imShowLayerSelect, "id", impmShowLayerSelectOptText, impmShowLayerSelectOptVal)

        /// prior model
        var pmCMICLLayerSelect = document.getElementsByClassName("pm-cmi-al-layer-select");
        myWindow.updateOptions(pmCMICLLayerSelect, "class", myParam.blockZ.id, myParam.blockZ.id)
        var pmCMISILayerSelect = document.getElementById("pm-cmi-si-layer-select");
        myWindow.updateOptions(pmCMISILayerSelect, "id", impmSILayerSelectOptText, impmSILayerSelectOptVal);
        var pmShowLayerSelect = document.getElementById("pm-show-layer-select");
        myWindow.updateOptions(pmShowLayerSelect, "id", impmShowLayerSelectOptText, impmShowLayerSelectOptVal)
    };
    // INITIAL MODEL SECTION //
    document.getElementById("im-res-ok-btn").onclick = function() {
        var imRes = myParam.getIMRes();
        var imLRISIValSelect = document.getElementById("im-lri-si-value-select");
        myWindow.updateOptions(imLRISIValSelect, "id", imRes.ids, imRes.ids)

        var imLRICLValSelect = document.getElementById("im-lri-cl-value-select");
        myWindow.updateOptions(imLRICLValSelect, "id", imRes.ids, imRes.ids)
    };
    document.getElementById("im-lri-si-ok-btn").onclick = function() {
        if (myMap.imBlockCellsOverlay===null) {
            myMap.imBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
            myMap.addOverlayToMap(myMap.imBlockCellsOverlay, myMap.bcName.init);
            myMap.showedBlockCells = "im";
            var imLRICLValSelect = document.getElementById("im-lri-cl-value-select");
            var imrtColorEls = document.getElementsByClassName("imrt-color-input");
            myMap.addBlockCellEvt(myMap.imBlockCellsOverlay, imLRICLValSelect, 1, imrtColorEls);
        }

        var siParam = myParam.getimInitialCells();
        var nCell = myMap.imBlockCellsOverlay.getLayers().length;
        if (siParam.layer==="design") {
            myParam.imCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
        } else if (siParam.layer==="all"){
            myParam.imCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.imCellsVal);
            myParam.imCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
        } else {
            myParam.imCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.imCellsVal);
        }
        imShowLayer()
    };
    document.getElementById("im-lri-al-ok-btn").onclick = function() {
        var layerSelectedidx = myParam.getimChangeL();
        var cellsValue = myMap.getBlockCellVal(myMap.imBlockCellsOverlay);
        myParam.imCellsVal = myParam.setCellVal(layerSelectedidx, cellsValue, myParam.imCellsVal);
    };
    document.getElementById("im-showlayer-ok-btn").onclick = function() {
        imShowLayer()
    };
    function imShowLayer() {
        var layer = myParam.getimShowLayer();
        var imrtColorEls = document.getElementsByClassName("imrt-color-input");
        if (layer === "design") {
            myMap.setBlockCellVal(myMap.imBlockCellsOverlay, myParam.imCellsValDesign);
        } else {
            myMap.setBlockCellVal(myMap.imBlockCellsOverlay, myParam.imCellsVal[layer-1]);
        }
        myMap.setBlockCellColor(myMap.imBlockCellsOverlay, 1, imrtColorEls);
    }
    // event tab
    document.getElementById("initialmodel-tab-btn").onclick = function() {
        if (myMap.blockLineOverlay == null) {return}
        if (myMap.showedBlockCells != null) {
            if (myMap.showedBlockCells=="pm") {
                myMap.removeOverlay(myMap.pmBlockCellsOverlay, myMap.bcName.pri);
            } else if (myMap.showedBlockCells=="im") {
                myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            }
            if (myMap.imBlockCellsOverlay != null) {
                myMap.addOverlayToMap(myMap.imBlockCellsOverlay, myMap.bcName.init);
                myMap.showedBlockCells = "im";
            }
        }
    };
    document.getElementById("priormodel-tab-btn").onclick = function() {
        if (myMap.blockLineOverlay == null) {return}
        if (myMap.showedBlockCells != null) {
            if (myMap.showedBlockCells=="pm") {
                myMap.removeOverlay(myMap.pmBlockCellsOverlay, myMap.bcName.pri);
            } else if (myMap.showedBlockCells=="im") {
                myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            }
            if (myMap.pmBlockCellsOverlay != null) {
                myMap.addOverlayToMap(myMap.pmBlockCellsOverlay, myMap.bcName.pri);
                myMap.showedBlockCells = "pm";
            }
        }
    };

    // PRIOR MODEL SECTION //
    document.getElementById("pm-cmi-si-ok-btn").onclick = function() {
        if (myMap.pmBlockCellsOverlay===null) {
            myMap.pmBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
            myMap.addOverlayToMap(myMap.pmBlockCellsOverlay, myMap.bcName.pri);
            myMap.showedBlockCells = "pm";
            var pmCMICLValSelect = document.getElementById("pm-cmi-cl-value-select");
            var pmitColorEls = document.getElementsByClassName("pmit-color-input");
            myMap.addBlockCellEvt(myMap.pmBlockCellsOverlay, pmCMICLValSelect, 0, pmitColorEls);
        }
        var siParam = myParam.getpmInitialCells();
        var nCell = myMap.pmBlockCellsOverlay.getLayers().length;
        if (siParam.layer==="design") {
            myParam.pmCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
        } else if (siParam.layer==="all") {
            myParam.pmCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
            myParam.pmCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.pmCellsVal);
        }
        else {
            myParam.pmCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.pmCellsVal);
        }
        pmShowLayer();
    };
    document.getElementById("pm-cmi-cl-ok-btn").onclick = function() {
        var layerSelectedidx = myParam.getpmChangeL();
        var cellsValue = myMap.getBlockCellVal(myMap.pmBlockCellsOverlay);
        myParam.pmCellsVal = myParam.setCellVal(layerSelectedidx, cellsValue, myParam.pmCellsVal);
    };
    document.getElementById("pm-showlayer-ok-btn").onclick = function() {
        pmShowLayer();
    };
    function pmShowLayer() {
        var layer = myParam.getpmShowLayer();
        var pmitColorEls = document.getElementsByClassName("pmit-color-input");
        if (layer === "design") {
            myMap.setBlockCellVal(myMap.pmBlockCellsOverlay, myParam.pmCellsValDesign);
        } else {
            myMap.setBlockCellVal(myMap.pmBlockCellsOverlay, myParam.pmCellsVal[layer-1]);
        }
        myMap.setBlockCellColor(myMap.pmBlockCellsOverlay, 0, pmitColorEls);
    }
    document.getElementById('datafile-tab-btn').click();

    // lasso
    myLasso = new Lasso();
    const lassoControl = L.control.lasso().addTo(myMap.map);
    var lassoStatusTd = document.getElementById("td-lasso-status");
    var lassoModeSelect = document.getElementById("lasso-mode-select");
    // myMap.map.on('mousedown', () => {
    //     myLasso.resetSelectedState(myMap.pmBlockCellsOverlay);
    // });
    myMap.map.on('lasso.finished', event => {
        if (myWindow.rightTabActive==="priormodel-tab") {
            var cellValElSelect = document.getElementById("pm-cmi-cl-value-select");
            var colorEls = document.getElementsByClassName("pmit-color-input");
            var startVal = 0;
        } else if (myWindow.rightTabActive==="initialmodel-tab"){
            var cellValElSelect = document.getElementById("im-lri-cl-value-select");
            var colorEls = document.getElementsByClassName("imrt-color-input");
            var startVal = 1;
        }
        myLasso.setSelectedLayers(myMap.pmBlockCellsOverlay, event.layers, cellValElSelect, startVal, colorEls);

    });
    myMap.map.on('lasso.enabled', () => {
        lassoStatusTd.innerHTML = 'enabled';
        myMap.removeOverlay(myMap.modelBoundaryOverlay);
        myMap.removeOverlay(myMap.centerAxisOverlay);
        myMap.removeOverlay(myMap.blockLineOverlay);
        myMap.removeOverlay(myMap.staOverlay);
        
    });
    myMap.map.on('lasso.disabled', () => {
        lassoStatusTd.innerHTML = 'disabled';
    });
    lassoModeSelect.addEventListener("change", ()=>{
        if (lassoModeSelect.value=="intersect") {
            lassoControl.setOptions({ intersect: true });
        } else if (lassoModeSelect.value=="contain") {
            lassoControl.setOptions({ intersect: false });
        }
    });

    //////////// START FLASK PROCESS ////////////////

    // PLOT STATION //
    coordForm = document.getElementById("coord-form");
    coordForm.addEventListener('submit', e => {
        e.preventDefault();
        var formData = new FormData();
        formData.append("myfile", document.getElementById("coordinate-input").files[0]);
        var url = "/uploadcoordinates";
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'json';

        // log response
        xhr.onload = () => {
            let staObj = xhr.response;
            if (myMap.staOverlay!=null) {
                myMap.removeOverlay(myMap.staOverlay, "station");
            }
            myMap.staOverlay = myMap.createStation(staObj);
            myMap.addOverlayToMap(myMap.staOverlay, "station");
            myMap.staCenter = myMap.staOverlay.getBounds().getCenter();
            myMap.map.fitBounds(myMap.staOverlay.getBounds());
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(formData);
    });
    // END PLOT STATION //

    // DATAFILE //
    // FILE INPUT //
    var dfStaForm = document.getElementById("df-sta-form");
    var dfStaInput = document.getElementById("df-sta-input");
    dfStaForm.addEventListener('submit', e => {
        e.preventDefault();
        var formData = new FormData();
        for (var i=0; i<dfStaInput.files.length; i++) {
            formData.append("file[]", dfStaInput.files[i]);
        }
        var url = "/uploadstations";
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'json';

        xhr.onload = () => {
            //pass
        };
        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    staName = xhr.response;
                    myWindow.dfSetFileTable(staName);
                } else {
                    console.log("error request")
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(formData);
    });
    // END PLOT STATION //

    // DATAFILE ERROR MAP PERIOD //
    document.getElementById("df-empt-ok-btn").onclick = function() {
        var errMap = myParam.getErrMapParam();
    };
    // END DATAFILE ERROR MAP PERIOD //

    // FLASK DATAFILE
    document.getElementById("df-output-save-btn").onclick = function() {
        dfProcessFlask("save");
    }
    document.getElementById("df-output-preview-btn").onclick = function() {
        dfProcessFlask("preview");
    }
    function dfProcessFlask(mode) {
        var url = "/dfsave";
        if (mode==="save") { var url = "/dfsave"; }
        else if (mode==="preview") { var url = "/dfpreview"; }
        var dfData = {
            mCenterLatLng: myMap.modelCenter,
            nResponse: parseInt(document.getElementById("df-resp-number-select").value),
            periods: myParam.getdfPeriod(),
            errPeriod: myParam.getdfErrorPeriod(),
            errMap: myParam.getErrMapParam(),
            saveName: myParam.getdfSaveName()
        }
        jsonDfData = JSON.stringify(dfData);

        var xhr = new XMLHttpRequest();

        xhr.onload = () => {
            //pass
        };
        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    if (mode==="save") {alert("Success");}
                    else if (mode==="preview") { myWindow.showPreview(xhr.responseText); }
                } else {
                    console.log("error request")
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(jsonDfData);
    }
    // FLASK INITIAL MODEL //
    document.getElementById("im-output-save-btn").onclick = function() {
        imProcessFlask("save")
    };
    document.getElementById("im-output-preview-btn").onclick = function() {
        imProcessFlask("preview")
    };
    function imProcessFlask(mode) {
        if (mode=="save") { var url = "/imsave"; }
        else if (mode=="preview") { var url = "/impreview"; }

        myParam.getBlockXY();
        myParam.getBlockZ();
        var imRes = myParam.getIMRes();

        var layerID = numberRange(1, myParam.blockZ.id.length+1);
        var compressedL = compressLayer(layerID, myParam.imCellsVal);
        
        var imData = {
            blockRI: compressedL,
            blockXY: myParam.blockXY.size,
            blockZ: myParam.blockZ.size,
            title: myParam.getimTitle(),
            resistivity: imRes.values,
            nr: imRes.number,
            saveName: myParam.getimSaveName()
        };
        jsonImData = JSON.stringify(imData);
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    if (mode=="save") {alert("Success")}
                    else if (mode==="preview") { myWindow.showPreview(xhr.responseText); }
                } else {
                    console.log("error request")
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(jsonImData);
    }

    document.getElementById("pm-output-save-btn").onclick = function() {
        processPM("save")
    }

    document.getElementById("pm-output-preview-btn").onclick = function() {
        processPM("preview")
    };
    
    function processPM(mode) {
        if (mode=="save") { var url = "/pmsave"; }
        else if (mode=="preview") { var url = "/pmpreview"; }
        myParam.getBlockXY();
        myParam.getBlockZ();
        var nx = myParam.blockXY.size.CS.length + myParam.blockXY.size.CN.length;
        var ny = myParam.blockXY.size.CW.length + myParam.blockXY.size.CE.length;
        var nz = myParam.blockZ.size.length;
        layerID = numberRange(1, myParam.blockZ.id.length+1);
        var compressedL = compressLayer(layerID, myParam.pmCellsVal);

        var pmData = {
            nx: nx,
            ny: ny,
            nz: nz,
            layerCMI: compressedL,
            saveName: myParam.getpmSaveName()
        };
        
        jsonPmData = JSON.stringify(pmData);

        var xhr = new XMLHttpRequest();
        xhr.onload = () => {
            //pass
        };
        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                var status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    if (mode==="save") {alert("Success");}
                    else if (mode==="preview") {
                        myWindow.showPreview(xhr.responseText);
                    }
                } else {
                    console.log("error request")
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(jsonPmData);
    }

////// Test Section /////////
    // myTest = new Test();
    // myTest.boundary();
    // myTest.model_center();
    // myTest.block_xy();
    // myTest.block_z();
////////////////////////////
}
