/* © 2026 Habitat Digital */
/* License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html). */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Setting } from "@web/views/form/setting/setting";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

class ErpicoResConfigEdition extends Component {
    static template = "erpico_res_config_edition";
    static components = { Setting };
    static props = {
        ...standardWidgetProps,
    };
}

export const erpicoResConfigEdition = {
    component: ErpicoResConfigEdition,
};

registry.category("view_widgets").add("res_config_edition", erpicoResConfigEdition);