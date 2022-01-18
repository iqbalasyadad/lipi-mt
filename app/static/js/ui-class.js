class AppUI {
    constructor() {
        this.el = {
            coord_input: document.getElementById("coordinate-input"),
            boundary: {
                sw_lat_text: document.getElementById("boundary-sw-lat-text"),
                sw_lng_text: document.getElementById("boundary-sw-lng-text"),
                ne_lat_text: document.getElementById("boundary-ne-lat-text"),
                ne_lng_text: document.getElementById("boundary-ne-lng-text"),
                ok_btn: document.getElementById("boundary-plot-btn")
            },
            model_center: {
                mode_select: document.getElementById("model-center-mode-select"),
                lat_text: document.getElementById("model-center-lat-text"),
                lng_text: document.getElementById("model-center-lng-text"),
                ok_btn: document.getElementById("model-center-plot-btn")
            },
            block_xy: {
                input_select: document.getElementById("block-xy-mode-select"),
                cn_mode_select:  document.getElementById("CN-mode-select"),
                cs_mode_select: document.getElementById("CS-mode-select"),
                ce_mode_select: document.getElementById("CE-mode-select"),
                cw_mode_select: document.getElementById("CW-mode-select"),
                cn_text: document.getElementById("CN-textarea"),
                cs_text: document.getElementById("CS-textarea"),
                ce_text: document.getElementById("CE-textarea"),
                cw_text: document.getElementById("CW-textarea"),
                ok_btn: document.getElementById("block-xy-ok-btn"),
            },
            block_z: {
                input_select: document.getElementById("block-z-mode-select"),
                z_text: document.getElementById("block-z-textarea"),
                ok_btn: document.getElementById("block-z-ok-btn"),
            },
            df: {
                tab: document.getElementById("datafile-tab-btn"),
                sta_input: document.getElementById("df-sta-input"),
                resp_select: document.getElementById("df-resp-number-select"),
                uv_mode_select: document.getElementById("df-used-value-mode-select"), 
                uv_els: document.getElementsByClassName("df-used-value-inputs"),
                uv_pls_btn: document.getElementsByClassName("dfuvt-plus-btn"),
                uv_ok_btn: document.getElementById("df-used-value-apply-btn"),

                e_period_select: document.getElementById("df-errperiod-select"),
                e_period_text: document.getElementById("df-errperiod-text"),

                em_period_select: document.getElementById("df-errmap-period-mode-select"),
                em_period_change: document.getElementById("df-errmap-period-scroll"),
                em_uv_els: document.getElementsByClassName("errmap-used-value-select"),
                em_file_els: document.getElementsByClassName("errmap-file-input"),
                em_response_els: document.getElementsByClassName("errmap-response-input"),
                em_value_els: document.getElementsByClassName("errmap-value-input"),
                em_plus_btn: document.getElementsByClassName("dfempt-plus-btn"),
                em_period_ok_btn: document.getElementById("df-errmap-ok-btn"),
    
                output_text: document.getElementById("df-output-fname-textarea")
            },
            im: {
                tab: document.getElementById("initialmodel-tab-btn"),
                title_text: document.getElementById("im-title-textarea"),
                resistivity_els: document.getElementsByClassName("im-r-val-text"),
                resistivity_plus_btn: document.getElementsByClassName("imrt-plus-btn"),
                resistivity_color_els: document.getElementsByClassName("imrt-color-input"),
                resistivity_ok_btn: document.getElementById("im-res-ok-btn"),
                
                si_layer_select: document.getElementById("im-lri-si-layer-select"),
                si_value_select: document.getElementById("im-lri-si-value-select"),
                cl_value_select: document.getElementById("im-lri-cl-value-select"),
                al_mode_select: document.getElementById("im-lri-al-mode-select"),
                al_single_select: document.getElementById("im-lri-al-layer-single-select"),
                al_ms_select: document.getElementById("im-lri-al-layer-ms-select"),
                al_me_select: document.getElementById("im-lri-al-layer-me-select"),
                
                show_layer_select: document.getElementById("im-show-layer-select"),
                output_text: document.getElementById("im-output-fname-textarea")
            },
            pcm: {
                tab: document.getElementById("controlmodel-tab-btn"),
                mi_use_im_r: document.getElementsByClassName("cm-cmi-use-im-im"), 
                mi_use_im_select: document.getElementsByClassName("cm-cmi-use-im-cm-select"),
                mi_use_im_ok_btn: document.getElementById("cm-cmi-use-im-ok-btn"),
                si_layer_select: document.getElementById("cm-cmi-si-layer-select"),
                si_value_select: document.getElementById("cm-cmi-si-value-select"),
                cl_value_select: document.getElementById("cm-cmi-cl-value-select"),
                al_mode_select: document.getElementById("cm-cmi-al-mode-select"),
                al_single_select: document.getElementById("cm-cmi-al-layer-single-select"),
                al_ms_select: document.getElementById("cm-cmi-al-layer-ms-select"),
                al_me_select: document.getElementById("cm-cmi-al-layer-me-select"),
                show_layer_select: document.getElementById("cm-show-layer-select"),
                output_text: document.getElementById("cm-output-fname-textarea")
            }
        };
    }
}