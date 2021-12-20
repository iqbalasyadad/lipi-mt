class Model {
    constructor() {
        this.boundary = {sw: null, ne: null};
        this.center = {lat: null, lng: null};
        this.blockXY = {
            size: {CN: null, CS: null, CE: null, CW: null},
            distance: {CN: null, CS: null, CE: null, CW: null}
        };
        this.blockZ = {size: null, distance: null};
        this.blockXYLatLngList = null;
    }
    setCenter(mode, latlng) {
        if (mode==="manual") {
            this.center.lat = latlng.lat;
            this.center.lng = latlng.lng;
        }
    }
    
}