class SaveParam extends AppUI {
    constructor() {
        super();
    }
    getUI_Boundary() {
        const boundary = {
            sw: { lat: this.el.boundary.sw_lat_text.value, lng: this.el.boundary.sw_lng_text.value },
            ne: { lat: this.el.boundary.ne_lat_text.value, lng: this.el.boundary.ne_lng_text.value }
        }
        return boundary;
    }
    getUI_ModelCenter() {
        const modelCenter = {
            mode: this.el.model_center.mode_select.selectedIndex.text,
            lat: this.el.model_center.lat_text.value,
            lng: this.el.model_center.lng_text.value
        };
        return modelCenter;
    }
    getUI_BlockXY() {
        const blockXY = {
            input: this.el.block_xy.input_select.selectedIndex.text,
            cn_mode: this.el.block_xy.cn_mode_select.selectedIndex.text,
            cs_mode: this.el.block_xy.cs_mode_select.selectedIndex.text,
            ce_mode: this.el.block_xy.ce_mode_select.selectedIndex.text,
            cw_mode: this.el.block_xy.cw_mode_select.selectedIndex.text,
            cn: this.el.block_xy.cn_text.value,
            cs: this.el.block_xy.cs_text.value,
            ce: this.el.block_xy.ce_text.value,
            cw: this.el.block_xy.cw_text.value
        };
        return blockXY;
    }
    getUI_BlockZ() {
        const blockZ = { 
            input: this.el.block_z.input_select.selectedIndex.text,
            z: this.el.block_z.z_text.value 
        };
        return blockZ;
    }
    getUI_DFResp() {
        return this.el.df.resp_select.selectedIndex.text;
    }
    getUI_DFPeriod() {
        var periods = [];
        for (var i=0; i<this.el.df.period_els.length; i++) {
            periods.push(this.el.df.period_els[i].value);
        }
        return periods;
    }
    getUI_DFErrPeriod() {
        return this.el.df.e_period_select.selectedIndex.text;
    }
    getUI_DFErrMapPeriod() {
        var err_map = {
            input_select: null,
            period: [], file: [], response: [], value: []
        };
        err_map.input_select = this.el.df.em_period_select.selectedIndex.text;
        if (err_map.input_select === "change") {
            for (var i=0; i<this.el.df.em_period_els.length; i++) {
                err_map.period.push(this.el.df.em_period_els[i].value);
                err_map.file.push(this.el.df.em_file_els[i].value);
                err_map.response.push(this.el.df.em_response_els[i].value);
                err_map.value.push(this.el.df.em_value_els[i].value);
            }
        }
        return err_map;
    }
    getUI_DFOutput() {
        return this.el.df.output_text.value;
    }
    
    getUI_IMTitle() {
        return this.el.im.title_text.value;
    }
    getUI_IMResistivity() {
        var res_obj = { resistiviy: [], color: [] };
        for (var i=0; i<this.el.im.resistivity_els.length; i++) {
            res_obj.resistiviy.push(this.el.im.resistivity_els[i].value),
            res_obj.color.push(this.el.im.color_els[i].value)
        }
        return res_obj;
    }
    getUI_IMLRI() {
        var lri = {
            si_layer: this.el.im.si_layer_select.selectedIndex.text,
            si_value: this.el.im.si_value_select.selectedIndex.text,
            cl_value: this.el.im.cl_value_select.selectedIndex.text,
            al_mode: this.el.im.al_mode_select.selectedIndex.text,
            al_layer_single: this.el.im.al_single_select.selectedIndex.text,
            al_layer_ms: this.el.im.al_ms_select.selectedIndex.text,
            al_layer_me: this.el.im.al_me_select.selectedIndex.text
        };
        return lri;
    }
    getUI_IMShowLayer() {
        return this.el.im.show_layer_select.selectedIndex.text;
    }
    getUI_IMOutput() {
        return this.el.im.output_text.value;
    }
    getUI_CMCMI() {
        var lri = {
            si_layer: this.el.cm.si_layer_select.selectedIndex.text,
            si_value: this.el.cm.si_value_select.selectedIndex.text,
            cl_value: this.el.cm.cl_value_select.selectedIndex.text,
            al_mode: this.el.cm.al_mode_select.selectedIndex.text,
            al_layer_single: this.el.cm.al_single_select.selectedIndex.text,
            al_layer_ms: this.el.cm.al_ms_select.selectedIndex.text,
            al_layer_me: this.el.cm.al_me_select.selectedIndex.text
        };
        return lri;
    }
    getUI_CMShowLayer() {
        return this.el.cm.show_layer_select.selectedIndex.text;
    }
    getUI_CMOutput() {
        return this.el.cm.output_text.value;
    }
    process() {
        var data_obj = {
            boundary: this.getUI_Boundary(),
            model_center: this.getUI_ModelCenter(),
            block_xy: this.getUI_BlockXY(),
            block_z: this.getUI_BlockZ(),
            df_resp: this.getUI_DFResp(),
            df_period: this.getUI_DFPeriod(),
            df_err_period: this.getUI_DFErrPeriod(),
            df_err_map: this.getUI_DFErrMapPeriod(),
            df_output: this.getUI_DFOutput(),

            im_title: this.getUI_IMTitle(),
            im_resistivity: this.getUI_IMResistivity(),
            im_lri: this.getUI_IMLRI(),
            im_show_layer: this.getUI_IMShowLayer(),
            im_output: this.getUI_IMOutput(),
            im_cell_val: this.im_cell_val,

            cm_cmi: this.getUI_CMCMI(),
            cm_show_layer: this.getUI_CMShowLayer(),
            cm_output: this.getUI_CMOutput(),
            cm_cell_val: this.cm_cell_val,
        };
        if (this.boundary!==undefined) {
            data_obj.boundary_test = this.b;
        }
        if (this.el.coord_input.files.length>0) {
            data_obj.coord_file = this.el.coord_input.files[0].name;
        }
        if (this.el.df.sta_input.files.length>0) {
            data_obj.df_sta_file = [];
            for (var i=0; i<this.el.df.sta_input.files.length; i++) {
                data_obj.df_sta_file.push(this.el.df.sta_input.files[i].name);
            }
        }
        return data_obj;

    }
    download(content, fileName, contentType) {
        const json_content = JSON.stringify(content);
        var a = document.createElement("a");
        var file = new Blob([json_content], {type: contentType});
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    }
}

class LoadParam extends AppUI {
    constructor() {
        super();
        this.data = null;
        const inputFile = document.getElementById("menu-bar-file-project-input");
        inputFile.addEventListener("change", ()=>{
            var fr = new FileReader();
            fr.readAsText(inputFile.files[0]);
            fr.addEventListener("load", ()=> {
                this.data = JSON.parse(fr.result);
                console.log(this.data);
                this.setBoundary(this.data.boundary);
                this.setModelCenter(this.data.model_center);
                this.setBlockXY(this.data.block_xy);
                this.setBlockZ(this.data.block_z);
            });
            // fr.onload = function(){
            //     console.log(this.data);

            // }
            // this.setBoundary(this.data.boundary);

        });
    }
    loadProject() {
        const chooseFile = document.get_ElementById("menu-bar-file-project-input");

    }
    parseProject(file) {

    }
    setBoundary(boundary) {
        this.el.boundary.sw_lat_text.value = boundary.sw.lat;
        this.el.boundary.sw_lng_text.value = boundary.sw.lng;
        this.el.boundary.ne_lat_text.value = boundary.ne.lat;
        this.el.boundary.ne_lng_text.value = boundary.ne.lng;
    }
    setModelCenter(model_center) {
        this.setSelect(this.el.model_center.mode_select, model_center.mode);
        this.el.model_center.lat_text.value = model_center.lat;
        this.el.model_center.lng_text.value = model_center.lng;
    }
    setBlockXY(block_xy) {
        this.setSelect(this.el.block_xy.input_select, block_xy.input);

        this.setSelect(this.el.block_xy.cn_mode_select, block_xy.cn_mode);
        this.setSelect(this.el.block_xy.cs_mode_select, block_xy.cs_mode);
        this.setSelect(this.el.block_xy.ce_mode_select, block_xy.ce_mode);
        this.setSelect(this.el.block_xy.cw_mode_select, block_xy.cw_mode);

        this.el.block_xy.cn_text.value = block_xy.cn;
        this.el.block_xy.cs_text.value = block_xy.cs;
        this.el.block_xy.ce_text.value = block_xy.ce;
        this.el.block_xy.cw_text.value = block_xy.cw;
    }
    setBlockZ(block_z) {
        this.setSelect(this.el.block_z.input_select, block_z.input);
        this.el.block_z.z_text.value = block_z.z;
    }

    setSelect(el, text) {
        for (var i=0; i<el.options.length; ++i) {
            if (el.options[i].text===text) {
                el.options[i].selected = true;
            }
        }
    }

}