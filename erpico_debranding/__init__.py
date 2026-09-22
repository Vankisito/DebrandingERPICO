# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from odoo import tools

from . import controllers
from . import models
from .patches.legacy_emails import patch_legacy_emails


def _rebrand_bot_partner(env):
    """Rename the bot partner and swap its avatar for the ERPICO placeholder."""
    partner = env.ref('base.partner_root', raise_if_not_found=False)
    if not partner:
        return
    values = {}
    if partner.name == 'OdooBot':
        values['name'] = 'ERPICO Assistant'
    with tools.file_open(
        'erpico_debranding/static/src/img/bot_placeholder.png', 'rb'
    ) as icon:
        image = base64.b64encode(icon.read())
    values['image_1920'] = image
    partner.write(values)


def post_init_hook(env):
    patch_legacy_emails(env)
    _rebrand_bot_partner(env)