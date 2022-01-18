window.onload = function() {
    let myParam = new Parameter();
    let myWindow = new MainWindow();
    let myMap = new Map();
    let myModel = new Model();

    let myUI = new AppUI;

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
            document.getElementById("boundary-sw-lat-text").value = layer.getBounds().getSouthWest().lat.toFixed(8);
            document.getElementById("boundary-sw-lng-text").value = layer.getBounds().getSouthWest().lng.toFixed(8);
            document.getElementById("boundary-ne-lat-text").value = layer.getBounds().getNorthEast().lat.toFixed(8);
            document.getElementById("boundary-ne-lng-text").value = layer.getBounds().getNorthEast().lng.toFixed(8);

            myParam.getModelBoundary();
            myMap.plotModelBoundary(myParam.boundary.sw, myParam.boundary.ne);
        }
    });
    document.getElementById("boundary-plot-btn").onclick = function() {
        myParam.getModelBoundary();
        myMap.plotModelBoundary(myParam.boundary.sw, myParam.boundary.ne);
    };
    document.getElementById("boundary-delete-btn").onclick = function() {
        if (myMap.resetOverlay(myMap.modelBoundaryOverlay, "Boundary")) {
            myMap.modelBoundaryOverlay = null;
        }
        document.getElementById("boundary-sw-lat-text").value = "";
        document.getElementById("boundary-sw-lng-text").value = "";
        document.getElementById("boundary-ne-lat-text").value = "";
        document.getElementById("boundary-ne-lng-text").value = "";
        myParam.boundary = null;

    };
    document.getElementById("model-center-plot-btn").onclick = function() {
        const mode_select = document.getElementById("model-center-mode-select");
        var lat_text = document.getElementById("model-center-lat-text");
        var lng_text = document.getElementById("model-center-lng-text");
        if (mode_select.value==="rect-center") {
            const rectCenter = myMap.modelBoundary.getBounds().getCenter();
            lat_text.value = rectCenter.lat.toFixed(8);
            lng_text.value = rectCenter.lng.toFixed(8);
        } else if (mode_select.value==="sta-center") {
            const staCenter = myMap.staOverlay.getBounds().getCenter();
            lat_text.value = staCenter.lat.toFixed(8);
            lng_text.value = staCenter.lng.toFixed(8);
        }
        myParam.getModelCenter();
        myMap.plotModelCenter(myParam.modelCenter.lat, myParam.modelCenter.lng);
    };
    document.getElementById("model-center-delete-btn").onclick = function() {
        if (myMap.resetOverlay(myMap.centerAxisOverlay, "Model Center")) {
            myMap.centerAxisOverlay = null;
        }
        document.getElementById("model-center-lat-text").value = "";
        document.getElementById("model-center-lng-text").value = "";
        myParam.modelCenter = null;
    };
    document.getElementById("block-xy-delete-btn").onclick = function() {
        myParam.blockXY = null;
        document.getElementById("CN-textarea").value = "";
        document.getElementById("CS-textarea").value = "";
        document.getElementById("CE-textarea").value = "";
        document.getElementById("CW-textarea").value = "";

        if (myMap.resetOverlay(myMap.blockLineOverlay, "Block Line")) {
            myMap.blockLineOverlay = null;
        }
        if (myMap.resetOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init)) {
            myMap.imBlockCellsOverlay = null;
        }
        if (myMap.resetOverlay(myMap.cmBlockCellsOverlay, myMap.bcName.pc)) {
            myMap.cmBlockCellsOverlay = null;
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
        if (myMap.cmBlockCellsOverlay != null) {
            myMap.removeOverlay(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            myMap.cmBlockCellsOverlay = null;
        }
    };

    // OK BUTTON BLOCK Z //
    document.getElementById("block-z-ok-btn").onclick = function() {
        myParam.getBlockZ();

        var imLRICLLayerSelect = document.getElementsByClassName("im-lri-al-layer-select");
        myWindow.updateOptions(imLRICLLayerSelect, "class", myParam.blockZ.id, myParam.blockZ.id)

        var imcmSILayerSelectOptText = ["all"];
        imcmSILayerSelectOptText.push.apply(imcmSILayerSelectOptText, myParam.blockZ.id);
        var imcmSILayerSelectOptVal = ["all"];
        imcmSILayerSelectOptVal.push.apply(imcmSILayerSelectOptVal, myParam.blockZ.id);

        var imLRISILayerSelect = document.getElementById("im-lri-si-layer-select");
        myWindow.updateOptions(imLRISILayerSelect, "id", imcmSILayerSelectOptText, imcmSILayerSelectOptVal);

        var imcmShowLayerSelectOptText = [];
        imcmShowLayerSelectOptText.push.apply(imcmShowLayerSelectOptText, myParam.blockZ.id);
        var imcmShowLayerSelectOptVal = [];
        imcmShowLayerSelectOptVal.push.apply(imcmShowLayerSelectOptVal, myParam.blockZ.id);

        var imShowLayerSelect = document.getElementById("im-show-layer-select");
        myWindow.updateOptions(imShowLayerSelect, "id", imcmShowLayerSelectOptText, imcmShowLayerSelectOptVal)

        /// control model
        var cmCMICLLayerSelect = document.getElementsByClassName("cm-cmi-al-layer-select");
        myWindow.updateOptions(cmCMICLLayerSelect, "class", myParam.blockZ.id, myParam.blockZ.id)
        var cmCMISILayerSelect = document.getElementById("cm-cmi-si-layer-select");
        myWindow.updateOptions(cmCMISILayerSelect, "id", imcmSILayerSelectOptText, imcmSILayerSelectOptVal);
        var cmShowLayerSelect = document.getElementById("cm-show-layer-select");
        myWindow.updateOptions(cmShowLayerSelect, "id", imcmShowLayerSelectOptText, imcmShowLayerSelectOptVal)
    };
    document.getElementById("block-z-delete-btn").onclick = function() {
        document.getElementById("block-z-textarea").value = "";
        myParam.blockZ = null;

        var imLRICLLayerSelect = document.getElementsByClassName("im-lri-al-layer-select");
        var imLRISILayerSelect = document.getElementById("im-lri-si-layer-select");
        var imShowLayerSelect = document.getElementById("im-show-layer-select");
        var cmCMICLLayerSelect = document.getElementsByClassName("cm-cmi-al-layer-select");
        var cmCMISILayerSelect = document.getElementById("cm-cmi-si-layer-select");
        var cmShowLayerSelect = document.getElementById("cm-show-layer-select");

        for (var i=0; i<imLRICLLayerSelect.length; i++) {
            myWindow.removeOptions(imLRICLLayerSelect[i]);
        };
        myWindow.removeOptions(imLRISILayerSelect);
        myWindow.removeOptions(imShowLayerSelect);
        for (var i=0; i<imLRICLLayerSelect.length; i++) {
            myWindow.removeOptions(cmCMICLLayerSelect[i]);
        };
        myWindow.removeOptions(cmCMISILayerSelect);
        myWindow.removeOptions(cmShowLayerSelect);

    };
    // INITIAL MODEL SECTION //
    document.getElementById("im-res-ok-btn").onclick = function() {
        var imRes = myParam.getIMRes();
        var imLRISIValSelect = document.getElementById("im-lri-si-value-select");
        myWindow.updateOptions(imLRISIValSelect, "id", imRes.ids, imRes.ids)
        myWindow.updateCMUseIMTable(imRes.number);
        myParam.im_resistivity = imRes;

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
        imShowLayer();
    };
    document.getElementById("im-lri-al-ok-btn").onclick = function() {
        var layerSelectedidx = myParam.getimChangeL();
        var cellsValue = myMap.getBlockCellVal(myMap.imBlockCellsOverlay);
        myParam.imCellsVal = myParam.setCellVal(layerSelectedidx, cellsValue, myParam.imCellsVal);
    };
    // document.getElementById("im-show-layer-ok-btn").onclick = function() {
    //     imShowLayer();
    // };
    document.getElementById("im-show-layer-select").onchange = function() {
        imShowLayer();
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
            if (myMap.showedBlockCells=="cm") {
                myMap.removeOverlay(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            } else if (myMap.showedBlockCells=="im") {
                myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            }
            if (myMap.imBlockCellsOverlay != null) {
                myMap.addOverlayToMap(myMap.imBlockCellsOverlay, myMap.bcName.init);
                myMap.showedBlockCells = "im";
            }
        }
    };
    document.getElementById("controlmodel-tab-btn").onclick = function() {
        if (myMap.blockLineOverlay == null) {return}
        if (myMap.showedBlockCells != null) {
            if (myMap.showedBlockCells=="cm") {
                myMap.removeOverlay(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            } else if (myMap.showedBlockCells=="im") {
                myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            }
            if (myMap.cmBlockCellsOverlay != null) {
                myMap.addOverlayToMap(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
                myMap.showedBlockCells = "cm";
            }
        }
    };

    // PRIOR MODEL SECTION //
    document.getElementById("cm-i-ok-btn").onclick = function() {
        myParam.cm_i_color = myParam.getcmIndexColor();
    }
    document.getElementById("cm-cmi-use-im-ok-btn").onclick = function() {
        var rFormat = myParam.getIMCMReplace();
        myParam.cmCellsVal = myParam.replaceCMVals(myParam.imCellsVal, rFormat);
        if (myMap.cmBlockCellsOverlay===null) {
            myMap.cmBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
            myMap.addOverlayToMap(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            myMap.showedBlockCells = "cm";
            var cmCMICLValSelect = document.getElementById("cm-cmi-cl-value-select");
            var cmitColorEls = document.getElementsByClassName("cmit-color-input");
            myMap.addBlockCellEvt(myMap.cmBlockCellsOverlay, cmCMICLValSelect, 0, cmitColorEls);
        }
        cmShowLayer();
        // myParam.cm_use_im = true;
    };

    document.getElementById("cm-cmi-si-ok-btn").onclick = function() {
        if (myMap.cmBlockCellsOverlay===null) {
            myMap.cmBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
            myMap.addOverlayToMap(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            myMap.showedBlockCells = "cm";
            var cmCMICLValSelect = document.getElementById("cm-cmi-cl-value-select");
            var cmitColorEls = document.getElementsByClassName("cmit-color-input");
            myMap.addBlockCellEvt(myMap.cmBlockCellsOverlay, cmCMICLValSelect, 0, cmitColorEls);
        }
        var siParam = myParam.getcmInitialCells();
        var nCell = myMap.cmBlockCellsOverlay.getLayers().length;
        if (siParam.layer==="design") {
            myParam.cmCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
        } else if (siParam.layer==="all") {
            myParam.cmCellsValDesign = myParam.setInitialCellsVal("design", siParam.value, 1, nCell, null);
            myParam.cmCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.cmCellsVal);
        }
        else {
            myParam.cmCellsVal = myParam.setInitialCellsVal(siParam.layer, siParam.value, myParam.blockZ.id.length, nCell, myParam.cmCellsVal);
        }
        cmShowLayer();
    };
    document.getElementById("cm-cmi-cl-ok-btn").onclick = function() {
        var layerSelectedidx = myParam.getcmChangeL();
        var cellsValue = myMap.getBlockCellVal(myMap.cmBlockCellsOverlay);
        myParam.cmCellsVal = myParam.setCellVal(layerSelectedidx, cellsValue, myParam.cmCellsVal);
    };
    // document.getElementById("cm-show-layer-ok-btn").onclick = function() {
    //     cmShowLayer();
    // };
    document.getElementById("cm-show-layer-select").onchange = function() {
        cmShowLayer();
    };
    function cmShowLayer() {
        var layer = myParam.getcmShowLayer();
        var cmitColorEls = document.getElementsByClassName("cmit-color-input");
        if (layer === "design") {
            myMap.setBlockCellVal(myMap.cmBlockCellsOverlay, myParam.cmCellsValDesign);
        } else {
            myMap.setBlockCellVal(myMap.cmBlockCellsOverlay, myParam.cmCellsVal[layer-1]);
        }
        myMap.setBlockCellColor(myMap.cmBlockCellsOverlay, 0, cmitColorEls);
    }

    // lasso
    myLasso = new Lasso();
    const lassoControl = L.control.lasso().addTo(myMap.map);
    var lassoStatusTd = document.getElementById("td-lasso-status");
    var lassoModeSelect = document.getElementById("lasso-mode-select");
    // myMap.map.on('mousedown', () => {
    //     myLasso.resetSelectedState(myMap.cmBlockCellsOverlay);
    // });
    myMap.map.on('lasso.finished', event => {
        if (myWindow.rightTabActive==="controlmodel-tab") {
            var cellValElSelect = document.getElementById("cm-cmi-cl-value-select");
            var colorEls = document.getElementsByClassName("cmit-color-input");
            var startVal = 0;
        } else if (myWindow.rightTabActive==="initialmodel-tab"){
            var cellValElSelect = document.getElementById("im-lri-cl-value-select");
            var colorEls = document.getElementsByClassName("imrt-color-input");
            var startVal = 1;
        }
        myLasso.setSelectedLayers(myMap.cmBlockCellsOverlay, event.layers, cellValElSelect, startVal, colorEls);

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
        var fileInfo = document.getElementById("coordinate-input").files[0];
        formData.append("myfile", fileInfo);
        var url = "/uploadcoordinates";
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'json';

        // log response
        xhr.onload = () => {
            let staObj = xhr.response;
            if (myMap.staOverlay!=null) {
                myMap.removeOverlay(myMap.staOverlay, "Station");
            }
            myMap.staOverlay = myMap.createStation(staObj);
            myMap.addOverlayToMap(myMap.staOverlay, "Station");
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
                    console.log("error request");
                    alert("Error request");
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
    document.getElementById("df-used-value-apply-btn").onclick = function() {
        myParam.df_used_value = myParam.getdfUsedValue();
        var errMapSelect = document.getElementsByClassName("errmap-used-value-select");
        errMapPeriodIdSelect = numberRange(1, myParam.df_used_value.value.length+1)
        var errMapUsedValueTh = document.getElementById("df-errmap-used-value-th");
        if (myParam.df_used_value.mode==="frequency") {
            errMapUsedValueTh.innerText = "Frequency";
        } else if (myParam.df_used_value.mode==="period") {
            errMapUsedValueTh.innerText = "Period";
        }
        myWindow.updateOptions(errMapSelect, "class", errMapPeriodIdSelect, errMapPeriodIdSelect);
    };


    // DATAFILE ERROR MAP PERIOD //
    document.getElementById("df-errmap-ok-btn").onclick = function() {
        myParam.df_em_period = myParam.getdfErrMapParam();
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
            usedValues: myParam.getdfUsedValue(),
            errPeriod: myParam.getdfErrorPeriod(),
            errMap: myParam.getdfErrMapParam(),
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
                    console.log("error request");
                    alert("Error request");
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
        imProcessFlask("save");
    };
    document.getElementById("im-output-preview-btn").onclick = function() {
        imProcessFlask("preview");
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
                    console.log("error request");
                    alert("Error request");
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(jsonImData);
    }

    document.getElementById("cm-output-save-btn").onclick = function() {
        processcm("save")
    }

    document.getElementById("cm-output-preview-btn").onclick = function() {
        processcm("preview")
    };
    
    function processcm(mode) {
        if (mode=="save") { var url = "/cmsave"; }
        else if (mode=="preview") { var url = "/cmpreview"; }
        myParam.getBlockXY();
        myParam.getBlockZ();
        var nx = myParam.blockXY.size.CS.length + myParam.blockXY.size.CN.length;
        var ny = myParam.blockXY.size.CW.length + myParam.blockXY.size.CE.length;
        var nz = myParam.blockZ.size.length;
        layerID = numberRange(1, myParam.blockZ.id.length+1);
        var compressedL = compressLayer(layerID, myParam.cmCellsVal);

        var cmData = {
            nx: nx,
            ny: ny,
            nz: nz,
            layerCMI: compressedL,
            saveName: myParam.getcmSaveName()
        };
        
        jsoncmData = JSON.stringify(cmData);

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
                    console.log("error request");
                    alert("Error request");
                }
            }
        };
        xhr.onerror = function() {
            alert("Error");
        }
        xhr.open("POST", url);
        xhr.send(jsoncmData);
    }
    document.getElementById("menu-bar-view-fit").onclick = function() {
        myMap.map.fitBounds(myMap.modelBoundary.getBounds());
    };
    // new save
    var modal = document.getElementById("save-modal");
    const menubarSaveBtn = document.getElementById("menu-bar-file-save-as");
    var span = document.getElementsByClassName("close-modal")[0];
    menubarSaveBtn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    var saveProjBtn = document.getElementById("modal-save-btn");
    saveProjBtn.addEventListener("click", ()=>{
        var mySave = new AppSave();

        var coord_file = document.getElementById("coordinate-input");
        if (coord_file.files.length>0){
            mySave.data.coord_file = coord_file.files[0].name;
        }
        if (myParam.boundary) {
            mySave.data.boundary = myParam.boundary;
        }
        if (myParam.modelCenter) {
            mySave.data.model_center = {
                mode: myParam.modelCenter.mode,
                lat: myMap.modelCenter.lat,
                lng: myMap.modelCenter.lng
            };
        }
        if (myParam.blockXY) {
            // mySave.data.block_xy = myParam.blockXY;
            Object.assign(mySave.data, {block_xy:  {}});
            Object.assign(mySave.data.block_xy, {block_mode: myParam.blockXY.block_mode, input_mode: myParam.blockXY.input_mode});
            if (myParam.blockXY.input_mode==="size") {
                Object.assign(mySave.data.block_xy, {size: myParam.blockXY.size});
            } else if(myParam.blockXY.input_mode==="distance") {
                Object.assign(mySave.data.block_xy, {distance: myParam.blockXY.distance});
            }
        };

        if (myParam.blockZ) {
            // mySave.data.block_z = myParam.blockZ;
            Object.assign(mySave.data, {block_z:  {}});
            Object.assign(mySave.data.block_z, {input_mode: myParam.blockZ.input_mode});
            if (myParam.blockZ.input_mode==="size") {
                Object.assign(mySave.data.block_z, {size: myParam.blockZ.size});
            } else if (myParam.blockZ.input_mode==="distance") {
                Object.assign(mySave.data.block_z, {distance: myParam.blockZ.distance});
            }
        };

        // datafile
        var sta_file_input = document.getElementById("df-sta-input");
        if (sta_file_input.files.length>0) {
            var sta_file_obj = [];
            for (var i=0; i<sta_file_input.files.length; i++){
                sta_file_obj.push(sta_file_input.files[i].name);
            }
            Object.assign(mySave.data.df, {sta_file: sta_file_obj});
        }
        if (myParam.df_used_value){
            Object.assign(mySave.data.df, {used_value: myParam.df_used_value});
        }
        if (myParam.df_em_period) {
            Object.assign(mySave.data.df, {em_period: {mode: "change", change_param: myParam.df_em_period}});
        }

        // initial model
        if (myParam.im_resistivity) {
            Object.assign(mySave.data.im, {resistivity: myParam.im_resistivity});
        }
        if (myParam.imCellsVal) {
            Object.assign(mySave.data.im, {cell_val: myParam.imCellsVal});
        }

        // control model
        if (myParam.cm_i_color) {
            Object.assign(mySave.data.pcm, {index_color: myParam.cm_i_color});
        }
        if (myParam.cm_use_im) {
            Object.assign(mySave.data.pcm, {use_im_format: myParam.getIMCMReplace()});
        }
        if (myParam.cmCellsVal) {
            Object.assign(mySave.data.pcm, {cell_val: myParam.cmCellsVal});
        }
        const filename = document.getElementById("modal-save-text").value;
        if (filename!="") {
            mySave.download(mySave.data, filename+".mtproject", 'text/plain');
        } 

    });



    myLoad = new LoadParam();

    var projectInput = document.getElementById("menu-bar-file-project-input");
    projectInput.addEventListener("change", ()=>{
        var fr = new FileReader();
        fr.addEventListener("load", ()=>{
            myLoad.data = JSON.parse(fr.result);
            set_loaded();
        });
        fr.readAsText(projectInput.files[0]);            
    });

    function set_loaded() {
        if(myLoad.data.boundary) {
            myLoad.setBoundary(myLoad.data.boundary);
        }
        if(myLoad.data.model_center && myLoad.data.model_center!="sta-center") {
            myLoad.setModelCenter(myLoad.data.model_center);
        }
        if(myLoad.data.block_xy) {
            myLoad.setBlockXY(myLoad.data.block_xy);
        }
        if(myLoad.data.block_z) {
            myLoad.setBlockZ(myLoad.data.block_z);
        }

        /////////////////////////// Load Data File //////////////////////////////////
        myLoad.setDFResponse(myLoad.data.df.response);
        if(myLoad.data.df.used_value) {
            myLoad.setDFUsedValue(myLoad.data.df.used_value);
        }
        myLoad.setDFEP(myLoad.data.df.e_period);
        if(myLoad.data.df.em_period) {
            myLoad.setDFEMP(myLoad.data.df.em_period);
        }
        if(myLoad.data.df.output) {
            myLoad.setDFOutput(myLoad.data.df.output);
        }
        /////////////////////////// Load Initial Model //////////////////////////////////
        if(myLoad.data.im.title) {
            myLoad.setIMTitle(myLoad.data.im.title);
        }
        if(myLoad.data.im.resistivity) {
            myLoad.setIMRes(myLoad.data.im.resistivity);
        }
        if(myLoad.data.im.cell_val) {

            if (myMap.imBlockCellsOverlay===null) {
                myMap.imBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
                myMap.addOverlayToMap(myMap.imBlockCellsOverlay, myMap.bcName.init);
                myMap.showedBlockCells = "im";
                var imLRICLValSelect = document.getElementById("im-lri-cl-value-select");
                var imrtColorEls = document.getElementsByClassName("imrt-color-input");
                myMap.addBlockCellEvt(myMap.imBlockCellsOverlay, imLRICLValSelect, 1, imrtColorEls);
            }

            myParam.imCellsVal = myLoad.data.im.cell_val;
            if (myMap.cmBlockCellsOverlay != null) {
                myMap.removeOverlay(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
            }
            imShowLayer();
            document.getElementById("initialmodel-tab-btn").click();
        }
        if(myLoad.data.im.output) {
            myLoad.setIMOutput(myLoad.data.im.output);
        }

        /////////////////////////// Load Prior/Control Model //////////////////////////////////
        if(myLoad.data.pcm.cell_val) {
            if (myMap.imBlockCellsOverlay != null) {
                myMap.removeOverlay(myMap.imBlockCellsOverlay, myMap.bcName.init);
            }
            if (myLoad.data.pcm.use_im_format){
                myLoad.setPCMI(myLoad.data.pcm.use_im_format);
            } else {
                if (myMap.cmBlockCellsOverlay===null) {
                    myMap.cmBlockCellsOverlay = myMap.createBlockCells(myParam.blockCells);
                    myMap.addOverlayToMap(myMap.cmBlockCellsOverlay, myMap.bcName.pc);
                    myMap.showedBlockCells = "cm";
                    var cmCMICLValSelect = document.getElementById("cm-cmi-cl-value-select");
                    var cmitColorEls = document.getElementsByClassName("cmit-color-input");
                    myMap.addBlockCellEvt(myMap.cmBlockCellsOverlay, cmCMICLValSelect, 0, cmitColorEls);
                }
                var siParam = myParam.getcmInitialCells();
                var nCell = myMap.cmBlockCellsOverlay.getLayers().length;
                myParam.cmCellsVal = myParam.setInitialCellsVal("all", siParam.value, myParam.blockZ.id.length, nCell, myParam.cmCellsVal);
            }
            myParam.cmCellsVal = myLoad.data.pcm.cell_val;
            cmShowLayer();
            document.getElementById("controlmodel-tab-btn").click();
        }
        if(myLoad.data.pcm.output) {
            myLoad.setPCMOutput(myLoad.data.pcm.output);
        }
    }


////// Test Section /////////

    // myTest = new Test();
    // myTest.boundary();
    // myTest.model_center();
    // myTest.block_xy();
    // myTest.block_z();
    // myTest.df_used_value();
    // myTest.im_title();
    // myTest.im_resistivity();
    // myTest.im_lri_si();
    // myTest.cm_tab();
    // myTest.cm_mi();

////////////////////////////

}
