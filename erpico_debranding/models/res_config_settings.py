# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from lxml import etree

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def get_views(self, views, options=None):
        result = super().get_views(views, options=options)
        for res in result.get('views', {}).values():
            arch = res.get('arch')
            if not arch:
                continue
            tree = etree.fromstring(arch)
            for node in tree.xpath(".//field[@widget='upgrade_boolean']"):
                node.attrib.pop('widget', None)
            res['arch'] = etree.tostring(tree, encoding='unicode')
        return result