# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    @api.readonly
    def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):
        if self._name == 'ir.module.module' and not self.env.context.get(
            'debranding_show_enterprise'
        ):
            domain = [*domain, ('to_buy', '=', False)]
        return super().search_fetch(
            domain,
            field_names=field_names,
            offset=offset,
            limit=limit,
            order=order,
        )

    @api.model
    @api.readonly
    def search_count(self, domain, limit=None):
        if self._name == 'ir.module.module' and not self.env.context.get(
            'debranding_show_enterprise'
        ):
            domain = [*domain, ('to_buy', '=', False)]
        return super().search_count(domain, limit=limit)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    @api.model
    @api.readonly
    def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):
        if not self.env.context.get('debranding_show_enterprise'):
            domain = [*domain, ('module_to_buy', '=', False)]
        return super().search_fetch(
            domain,
            field_names=field_names,
            offset=offset,
            limit=limit,
            order=order,
        )