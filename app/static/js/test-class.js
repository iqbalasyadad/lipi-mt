class Test {
    constructor() {}
    boundary() {
        let point1 = [-9.681256, 124.815378];
        let point2 = [-9.244726, 125.243898];
        document.getElementById("textBoundSWlat").value = point1[0];
        document.getElementById("textBoundSWlng").value = point1[1];
        document.getElementById("textBoundNElat").value = point2[0];
        document.getElementById("textBoundNElng").value = point2[1];
        document.getElementById("boundary-plot-btn").click();
    }
    model_center() {
        document.getElementById("model-center-plot-btn").click();
    }
    block_xy() {
        document.getElementById("CN-textarea").value = "1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000";
        document.getElementById("CS-textarea").value = "1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000";
        document.getElementById("CE-textarea").value = "1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000";
        document.getElementById("CW-textarea").value = "1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000";
        document.getElementById("block-xy-ok-btn").click();
    }
    block_z() {
        document.getElementById("block-z-textarea").value = "1000 2000 2000 2000 2000 3000 3000";
        document.getElementById("block-z-ok-btn").click();
    }

}