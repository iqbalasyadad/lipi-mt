class Lasso {
    constructor() {
        //pass
    }
    resetSelectedState(map) {
        map.eachLayer(layer => {
            if (layer instanceof L.Marker) {
                layer.setIcon(new L.Icon.Default());
            } else if (layer instanceof L.Path) {
                layer.setStyle({ color: '#3388ff' });
            }
        });
    }
    setSelectedLayers(map, layers, cellValEl, startVal, colorEls) {
        // this.resetSelectedState(map);
        layers.forEach(layer => {
            if (layer instanceof L.Rectangle) {
                var cellVal = parseInt(cellValEl.value);
                var colorVal = colorEls[cellVal-startVal].value
                layer.options.value = cellVal;
                layer.setStyle({color: colorVal});
            }
        });
    }
}