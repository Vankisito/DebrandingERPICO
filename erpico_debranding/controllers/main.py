# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.addons.web.controllers.database import Database as WebDatabase


class ErpicoDebranding(WebDatabase):

    @http.route('/web/database/manager', type='http', auth='none')
    def manager(self, **kw):
        raise Forbidden()

    @http.route('/web/database/selector', type='http', auth='none')
    def selector(self, **kw):
        raise Forbidden()

    @http.route('/web/database/create', type='http', auth='none', methods=['POST'], csrf=False)
    def create(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/duplicate', type='http', auth='none', methods=['POST'], csrf=False)
    def duplicate(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/drop', type='http', auth='none', methods=['POST'], csrf=False)
    def drop(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/backup', type='http', auth='none', methods=['POST'], csrf=False)
    def backup(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/restore', type='http', auth='none', methods=['POST'], csrf=False)
    def restore(self, **kwargs):
        raise Forbidden()

    @http.route('/web/database/change_password', type='http', auth='none', methods=['POST'], csrf=False)
    def change_password(self, **kwargs):
        raise Forbidden()