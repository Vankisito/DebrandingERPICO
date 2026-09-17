# © 2026 Santiago Vásquez
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from werkzeug.exceptions import Forbidden

from odoo import http


class ErpicoDebranding(http.Controller):

    @http.route('/web/database/manager', type='http', auth='none')
    def database_manager(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/selector', type='http', auth='none')
    def database_selector(self, **kwargs):
        raise Forbidden()