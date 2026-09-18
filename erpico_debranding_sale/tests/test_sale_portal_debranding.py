# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import HttpCase, TransactionCase, tagged


@tagged('erpico_debranding')
class TestSalePortalDebranding(HttpCase):

    def test_sale_order_portal_hides_connect_software(self):
        partner = self.env['res.partner'].create({'name': 'Portal Test'})
        order = self.env['sale.order'].create({
            'partner_id': partner.id,
        })
        access_token = order._portal_ensure_token()
        self.assertTrue(access_token, "access_token not generated")
        response = self.url_open(
            '/my/orders/%s?access_token=%s' % (order.id, access_token))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Connect with your software!', response.text)
        self.assertNotIn('portal_connect_software_modal', response.text)

    def test_purchase_order_portal_hides_connect_software(self):
        partner = self.env['res.partner'].create({'name': 'Portal Test'})
        order = self.env['purchase.order'].create({
            'partner_id': partner.id,
        })
        access_token = order._portal_ensure_token()
        self.assertTrue(access_token, "access_token not generated")
        response = self.url_open(
            '/my/purchase/%s?access_token=%s' % (order.id, access_token))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Connect with your software!', response.text)
        self.assertNotIn('portal_connect_software_modal', response.text)


@tagged('erpico_debranding')
class TestSalePortalOverride(TransactionCase):

    def test_sale_override_templates_registered(self):
        """Los overrides QWeb existen en el modelo de vistas."""
        for xmlid in (
            'erpico_debranding_sale.sale_hide_connect_software',
            'erpico_debranding_sale.purchase_hide_connect_software',
        ):
            self.assertTrue(self.env.ref(xmlid), xmlid)