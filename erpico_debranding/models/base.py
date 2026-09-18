# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


def _prepare_domain(domain):
    """Normalize a domain to a mutable list.

    ``None`` and tuples are converted to a list; legacy string domains
    are passed through untouched (the ORM still accepts them).
    """
    if domain is None:
        return []
    if isinstance(domain, (list, tuple)):
        return list(domain)
    return domain


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        if self._name == 'ir.module.module' and not self.env.context.get(
            'debranding_show_enterprise'
        ):
            domain = _prepare_domain(domain)
            if isinstance(domain, list):
                domain = [*domain, ('to_buy', '=', False)]
        return super().search(
            domain, offset=offset, limit=limit, order=order)

    @api.model
    @api.readonly
    def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):
        if self._name == 'ir.module.module' and not self.env.context.get(
            'debranding_show_enterprise'
        ):
            domain = _prepare_domain(domain)
            if isinstance(domain, list):
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
            domain = _prepare_domain(domain)
            if isinstance(domain, list):
                domain = [*domain, ('to_buy', '=', False)]
        return super().search_count(domain, limit=limit)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        if not self.env.context.get('debranding_show_enterprise'):
            domain = _prepare_domain(domain)
            if isinstance(domain, list):
                domain = [*domain, ('module_to_buy', '=', False)]
        return super().search(
            domain, offset=offset, limit=limit, order=order)

    @api.model
    @api.readonly
    def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):
        if not self.env.context.get('debranding_show_enterprise'):
            domain = _prepare_domain(domain)
            if isinstance(domain, list):
                domain = [*domain, ('module_to_buy', '=', False)]
        return super().search_fetch(
            domain,
            field_names=field_names,
            offset=offset,
            limit=limit,
            order=order,
        )