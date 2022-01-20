class AppSave extends AppUI {
    constructor() {
        super();
        this.data = {
            df: {
                response: this.get_ui_df_resp(),
                e_period: this.get_ui_df_e_period(),
                output: this.get_ui_df_output()
            }, 
            im: {
                title: this.get_ui_im_title(),
                show_layer: this.get_ui_im_show_layer(),
                output: this.get_ui_im_output()
            },
            pcm: {
                show_layer: this.get_ui_pcm_show_layer(),
                output: this.get_ui_pcm_output()
            } 
        };
    }
    get_ui_df_resp() {
        const select_index = this.el.df.resp_select.selectedIndex;
        return this.el.df.resp_select[select_index].value;
    }
    get_ui_df_e_period() {
        var select_index = this.el.df.e_period_select.selectedIndex;
        var mode = this.el.df.e_period_select[select_index].value;
        var e_period = { mode: mode };
        if (mode==="manual") {
            e_period.value = this.el.df.e_period_text.value
        }
        return e_period;
    }
    get_ui_df_output() {
        return this.el.df.output_text.value;
    }

    get_ui_im_title() {
        return this.el.im.title_text.value;
    }
    get_ui_im_show_layer() {
        return this.el.im.show_layer_select.value;
    }
    get_ui_im_output() {
        return this.el.im.output_text.value;
    }

    get_ui_pcm_show_layer() {
        return this.el.pcm.show_layer_select.value;
    }
    get_ui_pcm_output() {
        return this.el.pcm.output_text.value;
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
        // this.addLoadEvt();
    }
    addLoadEvt() {
        var projectInput = document.getElementById("menu-bar-file-project-input");
        projectInput.addEventListener("change", ()=>{
            var fr = new FileReader();
            fr.addEventListener("load", ()=>{
                this.data = JSON.parse(fr.result);
            });
            fr.readAsText(projectInput.files[0]);            
        });
    }
    setBoundary(boundary) {
        this.el.boundary.sw_lat_text.value = boundary.sw.lat;
        this.el.boundary.sw_lng_text.value = boundary.sw.lng;
        this.el.boundary.ne_lat_text.value = boundary.ne.lat;
        this.el.boundary.ne_lng_text.value = boundary.ne.lng;
        this.el.boundary.ok_btn.click();
    }
    setModelCenter(center) {
        this.setSelect(this.el.model_center.mode_select, center.mode);
        this.el.model_center.lat_text.value = center.lat;
        this.el.model_center.lng_text.value = center.lng;
        this.el.model_center.ok_btn.click();
    }
    setBlockXY(block_xy) {
        this.setSelect(this.el.block_xy.input_select, block_xy.input_mode);
        this.setSelect(this.el.block_xy.cn_mode_select, block_xy.block_mode.CN);
        this.setSelect(this.el.block_xy.cs_mode_select, block_xy.block_mode.CS);
        this.setSelect(this.el.block_xy.ce_mode_select, block_xy.block_mode.CE);
        this.setSelect(this.el.block_xy.cw_mode_select, block_xy.block_mode.CW);
        const input_mode = block_xy.input_mode;
        this.setBlockText(this.el.block_xy.cn_text, block_xy[input_mode].CN);
        this.setBlockText(this.el.block_xy.cs_text, block_xy[input_mode].CS);
        this.setBlockText(this.el.block_xy.ce_text, block_xy[input_mode].CE);
        this.setBlockText(this.el.block_xy.cw_text, block_xy[input_mode].CW);
        this.el.block_xy.ok_btn.click();
    }

    setBlockZ(block_z) {
        this.setSelect(this.el.block_z.input_select, block_z.input_mode);
        const input_mode = block_z.input_mode;
        this.setBlockText(this.el.block_z.z_text, block_z[input_mode]);
        this.el.block_z.ok_btn.click();
    }
    setDFResponse(response) {
        this.setSelect(this.el.df.resp_select, response);
    }
    setDFUsedValue(used_value) {
        this.setSelect(this.el.df.uv_mode_select, used_value.mode);
        const n_val = used_value.value.length
        for (var i=0; i<n_val; i++) {
            this.el.df.uv_els[i].value = used_value.value[i];
            if (i<n_val-1) {
                this.el.df.uv_pls_btn[i].click();
            }
        }
        this.el.df.uv_ok_btn.click();
    }
    setDFEP(e_period) {
        this.setSelect(this.el.df.e_period_select, e_period.mode);
        if(e_period.mode==="manual") {
            this.el.df.e_period_text.value = e_period.value;
        }
    }
    setDFEMP(em_period) {
        this.setSelect(this.el.df.em_period_select, em_period.mode);
        if(em_period.mode==="change") {
            this.el.df.em_period_change.style.display = "" ;
            const nChange = Object.keys(em_period.change_param).length;

            var i=0;
            for (var key of Object.keys(em_period.change_param)) {
                this.setSelect(this.el.df.em_uv_els[i], em_period.change_param[key].frequency_period.toString());
                var file_str = null;
                if (em_period.change_param[key].file === "all") {
                    file_str = "all";
                } else {
                    file_str = this.listToTextS(em_period.change_param[key].file);
                }
                this.el.df.em_file_els[i].value = file_str;
                var response_str = null;
                if (em_period.change_param[key].response === "all") {
                    response_str = "all";
                } else {
                    response_str = this.listToTextS(em_period.change_param[key].response);
                }
                this.el.df.em_response_els[i].value = response_str;
                this.el.df.em_value_els[i].value = em_period.change_param[key].final_value;
                if (i<nChange-1) { this.el.df.em_plus_btn[i].click(); }
                i+=1;
            }
        }
        this.el.df.em_period_ok_btn.click();
    }
    setDFOutput(output) {
        this.el.df.output_text.value = output;
    }

    setIMTitle(title) {
        this.el.im.title_text.value = title;
    }
    setIMRes(resistivity) {
        const nResistivity = resistivity.values.length;
        for (var i=0; i<nResistivity-1; i++) {
            this.el.im.resistivity_plus_btn[i].click();
        }
        for (var i=0; i<nResistivity; i++) {
            this.el.im.resistivity_els[i].value = resistivity.values[i];
            this.el.im.resistivity_color_els[i].value = resistivity.colors[i];
        }
        this.el.im.resistivity_ok_btn.click();
    }
    setIMOutput(output) {
        this.el.im.output_text.value = output;
    }

    setPCMColor(colors) {
        for (var i=0; i<colors.length; i++) {
            this.el.pcm.i_colors[i].value = colors[i];
        }
    }
    setPCMI(rFormat) {
        const nRow = this.el.pcm.mi_use_im_r.length;
        for (var i=0; i<nRow; i++) {
            var key = parseInt(this.el.pcm.mi_use_im_r[i].innerText);
            var mi = rFormat[key].toString();
            this.setSelect(this.el.pcm.mi_use_im_select[i], mi);
        }
        this.el.pcm.mi_use_im_ok_btn.click();
    }
    setPCMOutput(output) {
        this.el.pcm.output_text.value = output;
    }

    setSelect(el, value) {
        for (var i=0; i<el.options.length; ++i) {
            if (el.options[i].value===value) {
                el.options[i].selected = true;
            }
        }
    }
    setBlockText(el, data_list) {
        var data_str = "";
        for (var i=0; i<data_list.length; i++) {
            data_str += data_list[i].toString();
            if (i!=data_list.length-1) {
                data_str += "\n";
            }
        }
        el.value = data_str;
    }
    listToTextS(data_list) {
        var data_str = "";
        for (var i=0; i<data_list.length; i++) {
            data_str += data_list[i].toString();
            if (i!=data_list.length-1) {
                data_str += " ";
            }
        }
        return data_str;
    }

}