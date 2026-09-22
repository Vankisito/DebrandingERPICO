# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from odoo import api, SUPERUSER_ID, tools


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partner = env.ref('base.partner_root', raise_if_not_found=False)
    if not partner:
        return
    with tools.file_open(
        'erpico_debranding/static/src/img/bot_placeholder.png', 'rb'
    ) as icon:
        image = base64.b64encode(icon.read())
    values = {'image_1920': image}
    if partner.name == 'OdooBot':
        values['name'] = 'ERPICO Assistant'
    partner.write(values)