class Map {
    constructor() {
        let nullLayer = new L.TileLayer('');
        let basicLayer = new L.TileLayer("https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=kC7gdFCvOXPQM2jFMSUM", {
            attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
        });
        let satelliteLayer = new L.TileLayer("https://api.maptiler.com/maps/hybrid/{z}/{x}/{y}.jpg?key=kC7gdFCvOXPQM2jFMSUM", {
            attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
        });
        let stamenLayer = new L.TileLayer("https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg", {
            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
        });
        this.map = L.map('map', {
            center: [-9.463708, 125.931099],
            zoom: 11,
            layers: [nullLayer],
            fadeAnimation: false,
            zoomAnimation: false
        });
        this.baseMaps = {
            "Empty": nullLayer,
            "Basic": basicLayer,
            "Satellite": satelliteLayer,
            "Terrain": stamenLayer
        };
        this.overlayMaps = {};
        this.controlLayer = L.control.layers(this.baseMaps, this.overlayMaps).addTo(this.map);
        this.staOverlay = null;
        this.staCenter = null;
        this.imBlockCellsOverlay = null;
        this.pmBlockCellsOverlay = null;
        this.showedBlockCells = null;
        this.bcName = {init: "Initial Model", pri: "Prior Model"};
        this.popup = L.popup();
        this.showLatLngClick();

    }
    showLatLngClick() {
        this.map.on('click', e => {
            var mouseModeSelect = document.getElementById("mouse-set-mode-select");
            if (mouseModeSelect.value === "showLatLng") {
                var lat = e.latlng.lat.toFixed(8).toString();
                var lng = e.latlng.lng.toFixed(8).toString();
                this.popup
                .setLatLng(e.latlng)
                .setContent("lat: "+lat+"<br>"+"lng: "+lng)
                .openOn(this.map);
            }
        });
    }
    addModelBoundary(bounds) {
        let rectOptions = {
            color: "blue",
            weight: 2,
            fillOpacity: 0,
            interactive: false
        }
        this.modelBoundaryOverlay = L.layerGroup([]);
        this.modelBoundary = L.rectangle(bounds, rectOptions).addTo(this.modelBoundaryOverlay);
        this.map.addLayer(this.modelBoundaryOverlay)
        this.controlLayer.addOverlay(this.modelBoundaryOverlay, "Boundary");
    }

    plotModelBoundary(sw, ne) {
        var southWest = L.latLng(sw);
        var northEast = L.latLng(ne);
        var bounds = L.latLngBounds(southWest, northEast);
        if (this.modelBoundaryOverlay == null) {
            this.addModelBoundary(bounds);
        } else {
            this.modelBoundary.setBounds(bounds);
        }
        this.modelBoundLatLng = {
            south: this.modelBoundary.getBounds().getSouth(),
            west: this.modelBoundary.getBounds().getWest(),
            north: this.modelBoundary.getBounds().getNorth(),
            east: this.modelBoundary.getBounds().getEast()
        }
        this.modelBoundarySouth = this.modelBoundary.getBounds().getSouth();
        this.modelBoundaryWest = this.modelBoundary.getBounds().getWest();
        this.modelBoundaryNorth = this.modelBoundary.getBounds().getNorth();
        this.modelBoundaryEast = this.modelBoundary.getBounds().getEast();
        this.map.fitBounds(bounds);
    }
    addModelCenter(hStart, hEnd, vStart, vEnd) {
        this.centerAxisOverlay = L.layerGroup([]);
        this.centerHline = L.polyline([hStart, hEnd], {weight:1, color: "red", interactive: false}).addTo(this.centerAxisOverlay);
        this.centerVline = L.polyline([vStart, vEnd], {weight:1, color: "red", interactive: false}).addTo(this.centerAxisOverlay);
        this.map.addLayer(this.centerAxisOverlay)
        this.controlLayer.addOverlay(this.centerAxisOverlay, "Model Center");
    }
    plotModelCenter(mode, latInput, lngInput) {
        if (mode==="rect-center"){
            this.modelCenter = this.modelBoundary.getBounds().getCenter();
            document.getElementById("textModelCenterLat").value = this.modelCenter.lat.toFixed(8);
            document.getElementById("textModelCenterLng").value = this.modelCenter.lng.toFixed(8);
        } else if (mode==="sta-center"){
            this.modelCenter = this.staCenter;
            document.getElementById("textModelCenterLat").value = this.modelCenter.lat.toFixed(8);
            document.getElementById("textModelCenterLng").value = this.modelCenter.lng.toFixed(8);
        } else if (mode==="manual"){
            this.modelCenter = {lat: latInput, lng: lngInput};
        }
        let hStart = L.latLng(this.modelCenter.lat, this.modelBoundaryWest);
        let hEnd = L.latLng(this.modelCenter.lat, this.modelBoundaryEast);
        let vStart = L.latLng(this.modelBoundaryNorth, this.modelCenter.lng);;
        let vEnd = L.latLng(this.modelBoundarySouth, this.modelCenter.lng);

        if (this.centerAxisOverlay==null) {
            this.addModelCenter(hStart, hEnd, vStart, vEnd);
        } else {
            this.centerHline.setLatLngs([hStart, hEnd]);
            this.centerVline.setLatLngs([vStart, vEnd]);
        }
    }
    addBlockLine(latlngs) {
        this.blockLineOverlay = L.layerGroup([]);
        this.blockLine = L.polyline(latlngs, {weight: 1, color: "black", interactive: false}).addTo(this.blockLineOverlay);
        this.map.addLayer(this.blockLineOverlay)
        this.controlLayer.addOverlay(this.blockLineOverlay, "Block Line");
    }
    plotBlockLine(latlngs) {
        if (this.blockLineOverlay==null) {
            this.addBlockLine(latlngs);
        } else {
            this.blockLine.setLatLngs(latlngs);
        }
    }
    createBlockCells(bounds) {
        var blockCellOverlay = L.layerGroup([]);
        for (var i=0; i<bounds.lat.length-1; i++) {
            for (var j=0; j<bounds.lng.length-1; j++) {
                var point1 = [bounds.lat[i], bounds.lng[j+1]];
                var point2 = [bounds.lat[i+1], bounds.lng[j]];
                var bound = [point1, point2];
                let rectOptions = {
                    color: 'white',
                    weight: 0.3,
                    fillOpacity: 0.05,
                    interactive: true,
                    value: null,
                    colorID: null
                }
                var blockCell = L.rectangle(bound, rectOptions);
                blockCellOverlay.addLayer(blockCell);
            }
        }
        return blockCellOverlay;
    }
    addOverlayToMap(layerGroup, name) {
        this.map.addLayer(layerGroup)
        this.controlLayer.addOverlay(layerGroup, name);
    }
    removeOverlay(layerGroup, name) {
        if (this.map.hasLayer(layerGroup)) {
            this.map.removeLayer(layerGroup);
            if (name) {
               this.controlLayer.removeLayer(layerGroup, name);     
            }
        }
    }
    resetOverlay(layerGroup, name) {
        if (layerGroup != null) {
            this.removeOverlay(layerGroup, name);
            return true;
        } else { return false; }
    }
    getBlockCellVal(layerGroup) {
        var cellVals = [];
        layerGroup.eachLayer(layer => {
            cellVals.push(layer.options.value);
        });
        return cellVals;
    }
    setBlockCellValAll(layerGroup, val) {
        layerGroup.eachLayer(layer => {
            layer.options.value = val;
        });       
    }
    setBlockCellColorAll(layerGroup, val) {
        if (val==-1) {
            layerGroup.eachLayer(layer => {
                layer.setStyle({ color: "white" });
            });   
        }
    }

    setBlockCellVal(layerGroup, cellsVal) {
        var i = 0;
        layerGroup.eachLayer(layer => {
            if (cellsVal[i] != null) {
                layer.options.value = cellsVal[i];
                if (layer.options.fillOpacity<0.5) {
                    layer.options.fillOpacity = 0.5;
                }
            } else {
                layer.options.fillOpacity = 0.05; 
            }
            i++;
        });
    }
    setBlockCellColor(layerGroup, startVal, colorEls) {
        var i = 0;
        layerGroup.eachLayer(layer => {
            var colorID = layer.options.value - startVal;
            layer.setStyle({ color: colorEls[colorID].value});
            i++;
        });
    }
    addBlockCellEvt(layerGroup, cellValEl, startVal, colorEls) {
        layerGroup.eachLayer(function(layer){
            layer.addEventListener("click", function() {
                var cellVal = parseInt(cellValEl.value);
                var colorID = cellVal-startVal;
                layer.options.value = cellVal;
                layer.options.colorID = cellVal-startVal;
                layer.setStyle({color: colorEls[colorID].value});
            });
        });
    }
    createStation(staObj) {
        // staObj = {sta1:{lat: lng:}, sta2:{lat: lng:}}
        var staOverlay = L.featureGroup([]);
        for (var key in staObj) {
            var staMarkerOptions = {radius: 5, staName: key};
            var staLatLng = [staObj[key]["lat"],staObj[key]["lng"]];
            var staMarker = L.circleMarker(staLatLng, staMarkerOptions);
            staMarker.bindPopup(key).openPopup();
            staOverlay.addLayer(staMarker);
        }
        return staOverlay;
        // for (var i=0; i<staObj.name.length; i++) {
        //     var staMarkerOptions = {radius: 5, staName: staObj.name[i]};
        //     var staLatLng =  [staObj.lat[i], staObj.lng[i]];
        //     var staMarker = L.circleMarker(staLatLng, staMarkerOptions);
        //     staMarker.bindPopup(staObj.name[i]).openPopup();
        //     staOverlay.addLayer(staMarker);
        // }
    }
}