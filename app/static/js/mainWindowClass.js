class MainWindow {
    constructor() {
        this.imColorInit = ["#34eb3a", "#3434eb", "#eb3434", "#9f34eb", "#1ec4e6", "#f0f059"];

        var dfptTable = document.getElementById("df-period-table");
        var dfptMinusBtns = document.getElementsByClassName("dfpt-minus-btn");
        var dfptPlusBtns = document.getElementsByClassName("dfpt-plus-btn");
        this.tablePLbtnAddEvt(dfptTable, dfptPlusBtns,dfptMinusBtns, 1, 0, true, 0);

        var dfemptTable = document.getElementById("df-errmap-period-table");
        var dfemptMinusBtns = document.getElementsByClassName("dfempt-minus-btn");
        var dfemptPlusBtns = document.getElementsByClassName("dfempt-plus-btn");
        this.tablePLbtnAddEvt(dfemptTable, dfemptPlusBtns, dfemptMinusBtns, 2, 0, false, 0);

        var imrtTable = document.getElementById("im-res-table");
        var imrtMinusBtns = document.getElementsByClassName("imrt-minus-btn");
        var imrtPlusBtns = document.getElementsByClassName("imrt-plus-btn");
        var imrtColorEls = document.getElementsByClassName("imrt-color-input");
        this.tablePLbtnAddEvtColor(imrtTable, imrtPlusBtns, imrtMinusBtns, 1, 0, true, 0, imrtColorEls, this.imColorInit);

        this.addLeftTabEvt();
        this.setInit();

    }

    setInit() {
        var selectErrPeriod = document.getElementById("errperiod-select");
        var rowErrPeriodManual = document.getElementById("tr-errperiod-manual");
        rowErrPeriodManual.style.display='none';
        selectErrPeriod.addEventListener("change", ()=> {
            if (selectErrPeriod.value==="=real") {
                rowErrPeriodManual.style.display='none';
            } else if (selectErrPeriod.value==="manual") {
                rowErrPeriodManual.style.display='';
            }
        });

        var imLRIALMode = document.getElementById("im-lri-al-mode-select");
        var imLRIALtrSingle = document.getElementById("tr-im-lri-al-layer-single");
        var imLRIALtrMultipleS = document.getElementById("tr-im-lri-al-layer-multiple-s");
        var imLRIALtrMultipleE = document.getElementById("tr-im-lri-al-layer-multiple-e");
        imLRIALtrMultipleS.style.display = 'none';
        imLRIALtrMultipleE.style.display = 'none';
        imLRIALMode.addEventListener("change", () => {
            if (imLRIALMode.value==="single") {
                imLRIALtrSingle.style.display = "";
                imLRIALtrMultipleS.style.display = "none";
                imLRIALtrMultipleE.style.display = "none";
            } else if (imLRIALMode.value==="multiple") {
                imLRIALtrSingle.style.display = "none";
                imLRIALtrMultipleS.style.display = "";
                imLRIALtrMultipleE.style.display = "";
            }
        });
        var pmiCMIALMode = document.getElementById("pm-cmi-al-mode-select");
        var pmiCMIALtrSingle = document.getElementById("tr-pm-cmi-al-layer-single");
        var pmiCMIALtrMultipleS = document.getElementById("tr-pm-cmi-al-layer-multiple-s");
        var pmiCMIALtrMultipleE = document.getElementById("tr-pm-cmi-al-layer-multiple-e");
        pmiCMIALtrMultipleS.style.display = 'none';
        pmiCMIALtrMultipleE.style.display = 'none';
        pmiCMIALMode.addEventListener("change", () => {
            if (pmiCMIALMode.value==="single") {
                pmiCMIALtrSingle.style.display = "";
                pmiCMIALtrMultipleS.style.display = "none";
                pmiCMIALtrMultipleE.style.display = "none";
            } else if (pmiCMIALMode.value==="multiple") {
                pmiCMIALtrSingle.style.display = "none";
                pmiCMIALtrMultipleS.style.display = "";
                pmiCMIALtrMultipleE.style.display = "";
            }
        });
        var mouseModeSelect = document.getElementById("mouse-set-mode-select");
        var trLasso = document.getElementsByClassName("tr-lasso");
        for(var i=0; i<trLasso.length; i++) {
            trLasso[i].style.display = "none";
        }
        mouseModeSelect.addEventListener("change", function(){
            if (mouseModeSelect.value != "lasso") {
                for(var i=0; i<trLasso.length; i++) {
                    trLasso[i].style.display = "none";
                }
            } else {
                for(var i=0; i<trLasso.length; i++) {
                    trLasso[i].style.display = "";
                }}
        });

        // DATAFILE RESPONSE TABLE
        var dfRespNumSelect = document.getElementById("df-resp-number-select");
        var dfRespName4Tr = document.getElementsByClassName("df-resp-name-4-tr");
        var dfRespName8Tr = document.getElementsByClassName("df-resp-name-8-tr");
        this.setDisplayEls(dfRespName4Tr, "none");
        dfRespNumSelect.addEventListener("change", () => {
            var dfRespNumSelectVal = parseInt(dfRespNumSelect.value);
            if (dfRespNumSelectVal==4) {
                this.setDisplayEls(dfRespName4Tr, "");
                this.setDisplayEls(dfRespName8Tr, "none");
            }
            else if (dfRespNumSelectVal==8) {
                this.setDisplayEls(dfRespName4Tr, "none");
                this.setDisplayEls(dfRespName8Tr, "");
            }
        });

        // DATAFILE ERRMAP CHANGE MODE
        var dfErrmapModeSelect = document.getElementById("df-errmap-period-mode-select");
        var dfErrmapChangeTable = document.getElementById("df-errmap-period-table");
        var dfErrmapChangeScroll = document.getElementById("df-errmap-period-scroll");
        dfErrmapChangeTable.style.display = "none";
        dfErrmapChangeScroll.style.height = "auto";

        dfErrmapModeSelect.addEventListener("change", () => {
            if(dfErrmapModeSelect.value==="none") {
                dfErrmapChangeTable.style.display = "none";
                dfErrmapChangeScroll.style.height = "auto";
            } else if (dfErrmapModeSelect.value==="change") {
                dfErrmapChangeTable.style.display = "";
                dfErrmapChangeScroll.style.height = "200px";
            }
        });

    }
    setDisplayEls(els, displayMode) {
        for (var i=0; i<els.length; i++) {
            els[i].style.display = displayMode;
        }
    }
    addLeftTabEvt() {
        var tabBtn = document.getElementsByClassName("panelr-tablinks");
        var pageName = ["datafile-tab", "initialmodel-tab", "priormodel-tab"];
        for (var i=0; i<tabBtn.length; i++) {
            this.tabAddEvt(tabBtn[i], pageName[i]);
        }
    }
    tabAddEvt(tabBtn, pageName) {
        tabBtn.addEventListener("click", evt => {
            this.openRightTab(evt, pageName);
        });
    }

    openRightTab(evt, pageName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("panelr-tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(pageName).style.display = "block";
        evt.currentTarget.className += " active";
        this.rightTabActive = pageName;
    }
    getTR(evt) {
        let parent = evt.target;
        while(true) {
            if (parent.nodeName === null) {return}
            if (parent.nodeName.toLowerCase() === "tr") {
                return parent;
            }
            parent = parent.parentNode;
        }
    }
    tablePLbtnAddEvtColor(tableEl, plusBtnsClass, minusBtnsClass, startRow, btnIndex, autoNo, colNo, colorElements, colorList) {
        minusBtnsClass[btnIndex].addEventListener("click", evt => {
            if (minusBtnsClass.length>1) {
                var rowClicked = this.getTR(evt);
                var rowClickedIndex = rowClicked.rowIndex;
                tableEl.deleteRow(rowClickedIndex);
                if (autoNo==true) {
                    this.resetTableNo(tableEl, colNo);
                }
            }
        });
        plusBtnsClass[btnIndex].addEventListener("click", evt => {
            var rowClicked = this.getTR(evt);
            var rowHTML = rowClicked.innerHTML;
            var rowClickedIndex = rowClicked.rowIndex;
            var nextBtnIndex = rowClickedIndex-startRow+1;
            var row = tableEl.insertRow(rowClickedIndex+1);
            row.innerHTML = rowHTML;
            if (autoNo==true) {
                this.resetTableNo(tableEl, 0);
            }
            this.updateColor(colorElements, colorList);
            this.tablePLbtnAddEvtColor(tableEl, plusBtnsClass, minusBtnsClass, startRow, nextBtnIndex, autoNo, colNo, colorElements, colorList);
        });
    }

    tablePLbtnAddEvt(tableEl, plusBtnsClass, minusBtnsClass, startRow, btnIndex, autoNo, colNo) {
        minusBtnsClass[btnIndex].addEventListener("click", evt => {
            if (minusBtnsClass.length>1) {
                var rowClicked = this.getTR(evt);
                var rowClickedIndex = rowClicked.rowIndex;
                tableEl.deleteRow(rowClickedIndex);
                if (autoNo==true) {
                    this.resetTableNo(tableEl, colNo);
                }
            }
        });
        plusBtnsClass[btnIndex].addEventListener("click", evt => {
            var rowClicked = this.getTR(evt);
            var rowHTML = rowClicked.innerHTML;
            var rowClickedIndex = rowClicked.rowIndex;
            var nextBtnIndex = rowClickedIndex-startRow+1;
            var row = tableEl.insertRow(rowClickedIndex+1);
            row.innerHTML = rowHTML;
            if (autoNo==true) {
                this.resetTableNo(tableEl, 0);
            }
            this.tablePLbtnAddEvt(tableEl, plusBtnsClass, minusBtnsClass, startRow, nextBtnIndex, autoNo, colNo);
        });
    }

    resetTableNo(tableEl, colIndex) {
        for (var i=0; i<tableEl.rows.length-1; i++) {
            tableEl.rows[i+1].cells[colIndex].innerText = i+1;
        }
    }
    updateOptions(selectElementsInput, type, optText, optValue) {
        var selectElements = [];
        if (type==="id") {
            selectElements.push(selectElementsInput);
        } else if (type==="class") {
            selectElements = selectElementsInput;
        }
        for (var i=0; i<selectElements.length; i++) {
            var selectElement = selectElements[i];
            var j, L = selectElement.options.length - 1;
            for(j = L; j>=0; j--) {
               selectElement.remove(j);
            }
            for (var k=0; k<optText.length; k++) {
                var option = document.createElement("option");
                option.text = optText[k];
                option.value = optValue[k];
                selectElement.add(option);
            }
        }
    }
    updateColor(colorElements, colorList) {
        if (colorElements.length <= colorList.length) {
            for (var i=0; i<colorElements.length; i++) {
                colorElements[i].value = colorList[i];
            }
        }
    }
    dfSetFileTable(filesName) {
        var table = document.getElementById("df-sta-name-table");
        var tabletBody = document.getElementById("df-sta-name-tbody");
        while (table.rows.length > 1) {
            table.deleteRow(1);
          }
        for (var i=0; i<filesName.length; i++) {
            var newRow = table.insertRow(-1);
            newRow.innerHTML = "<tr><td class='table-label-panel-lr df-sta-name-tr'>"+(i+1)+"</td><td class=' table-label-panel-lr df-sta-name-tr'>"+filesName[i]+"</td></tr>"
        }
    }
    showPreview(text) {
        var myWindow = window.open("", "MsgWindow", "width=800,height=700");
        myWindow.document.write("<p style='font-family:Arial; white-space:pre-wrap; word-spacing:5px;'>"+text+"</p>");
    }
}