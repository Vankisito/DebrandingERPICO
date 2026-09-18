# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import importlib.util
from pathlib import Path

from odoo.addons.erpico_debranding.patches import legacy_emails
from odoo.addons.erpico_debranding.patches.legacy_emails import (
    LEGACY_EMAIL_XMLIDS,
)
from odoo.tests import HttpCase, TransactionCase, tagged


@tagged('erpico_debranding')
class TestLegacyEmails(TransactionCase):

    def test_legacy_bodies_rebranded(self):
        for xmlid in LEGACY_EMAIL_XMLIDS:
            body = str(self.env.ref(xmlid).body_html or '')
            self.assertNotIn('Odoo', body, xmlid)
            self.assertNotIn('odoo.com', body, xmlid)
        # el template de set-password lleva marca ERPICO tras el parche
        set_password_body = str(
            self.env.ref('auth_signup.set_password_email').body_html or '')
        self.assertIn('ERPICO', set_password_body)

    def test_bot_partner_renamed(self):
        bots = self.env['res.partner'].search([
            ('name', '=', 'OdooBot'),
            ('active', 'in', (True, False)),
        ])
        self.assertFalse(bots)


@tagged('erpico_debranding')
class TestEnterpriseHidden(TransactionCase):

    def test_module_to_buy_hidden_from_search_fetch(self):
        module = self.env['ir.module.module'].create({
            'name': 'test_enterprise_hidden',
            'state': 'uninstalled',
            'to_buy': True,
        })
        res = self.env['ir.module.module'].search_fetch(
            [('name', '=', 'test_enterprise_hidden')]
        )
        self.assertNotIn(module, res)
        res_all = self.env['ir.module.module'].with_context(
            debranding_show_enterprise=True
        ).search_fetch([('name', '=', 'test_enterprise_hidden')])
        self.assertIn(module, res_all)
        self.assertEqual(
            self.env['ir.module.module'].search_count(
                [('name', '=', 'test_enterprise_hidden')]
            ), 0)
        # el filtro también aplica a search() plano (wizards/API)
        res_plain = self.env['ir.module.module'].search(
            [('name', '=', 'test_enterprise_hidden')]
        )
        self.assertNotIn(module, res_plain)
        res_plain_all = self.env['ir.module.module'].with_context(
            debranding_show_enterprise=True
        ).search([('name', '=', 'test_enterprise_hidden')])
        self.assertIn(module, res_plain_all)

    def test_payment_provider_module_to_buy_hidden(self):
        module = self.env['ir.module.module'].create({
            'name': 'test_enterprise_module',
            'state': 'uninstalled',
            'to_buy': True,
        })
        provider = self.env['payment.provider'].create({
            'name': 'Test Enterprise Provider',
            'code': 'none',
            'module_id': module.id,
        })
        res = self.env['payment.provider'].search_fetch(
            [('code', '=', 'none'), ('name', '=', 'Test Enterprise Provider')]
        )
        self.assertNotIn(provider, res)
        res_all = self.env['payment.provider'].with_context(
            debranding_show_enterprise=True
        ).search_fetch(
            [('code', '=', 'none'), ('name', '=', 'Test Enterprise Provider')]
        )
        self.assertIn(provider, res_all)
        # filtro también en search() plano
        res_plain = self.env['payment.provider'].search(
            [('code', '=', 'none'), ('name', '=', 'Test Enterprise Provider')]
        )
        self.assertNotIn(provider, res_plain)
        res_plain_all = self.env['payment.provider'].with_context(
            debranding_show_enterprise=True
        ).search(
            [('code', '=', 'none'), ('name', '=', 'Test Enterprise Provider')]
        )
        self.assertIn(provider, res_plain_all)

    def test_search_handles_legacy_domains(self):
        # los domains None y tuple no deben romper el filtro ni el ORM
        self.env['ir.module.module'].search(None)
        self.env['ir.module.module'].search(())
        self.env['payment.provider'].search(None)
        self.env['payment.provider'].search(())
        # y el filtro sigue activo con domain None
        hidden = self.env['ir.module.module'].create({
            'name': 'test_legacy_domain_hidden',
            'state': 'uninstalled',
            'to_buy': True,
        })
        self.assertNotIn(
            hidden,
            self.env['ir.module.module'].search(
                [('name', '=', 'test_legacy_domain_hidden')]),
        )


@tagged('erpico_debranding')
class TestSettingsView(TransactionCase):

    def test_get_views_strips_upgrade_boolean(self):
        view = self.env.ref('base_setup.res_config_settings_view_form')
        # la vista real contiene el widget en los campos Enterprise heredados
        self.assertIn('upgrade_boolean', view.arch)
        result = self.env['res.config.settings'].get_views([(view.id, 'form')])
        arch = result['views']['form']['arch']
        self.assertNotIn('upgrade_boolean', arch)
        self.assertGreater(len(arch), 1000)


@tagged('erpico_debranding')
class TestMenus(TransactionCase):

    def test_store_menus_reparented(self):
        parent = self.env.ref('base.menu_ir_property')
        for xmlid in ('base.theme_store', 'base.menu_theme_store',
                      'base.menu_third_party'):
            self.assertEqual(self.env.ref(xmlid).parent_id.id, parent.id)


@tagged('erpico_debranding')
class TestBrandedRenders(TransactionCase):

    def test_brand_promotion_message(self):
        html = str(self.env['ir.qweb']._render('web.brand_promotion_message'))
        self.assertIn('ERPICO', html)
        self.assertNotIn('Odoo', html)
        self.assertNotIn('odoo.com', html)

    def test_mail_layout_render(self):
        message = self.env['mail.message'].search([], limit=1)
        self.assertTrue(message)
        values = {
            'message': message,
            'company': self.env.ref('base.main_company'),
            'email_notification_force_footer': True,
        }
        html = str(self.env['ir.qweb']._render(
            'mail.mail_notification_layout', values))
        self.assertIn('ERPICO', html)
        self.assertNotIn('odoo.com', html)


@tagged('erpico_debranding')
class TestDebrandingHttp(HttpCase):

    def test_database_manager_blocked(self):
        response = self.url_open('/web/database/manager')
        self.assertEqual(response.status_code, 403)

    def test_database_selector_blocked(self):
        response = self.url_open('/web/database/selector')
        self.assertEqual(response.status_code, 403)

    def test_login_debranded(self):
        response = self.url_open('/web/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Powered by <b>ERPICO</b>', response.text)
        self.assertNotIn('web/database/manager', response.text)
        self.assertIn('erpico-isotipo.png', response.text)

    def test_database_post_endpoints_blocked(self):
        """Todos los POST de gestión de BD devuelven 403 (R-001 fix)."""
        endpoints = [
            '/web/database/create',
            '/web/database/duplicate',
            '/web/database/drop',
            '/web/database/backup',
            '/web/database/restore',
            '/web/database/change_password',
        ]
        for ep in endpoints:
            response = self.url_open(ep, data={'master_pwd': 'x'})
            self.assertEqual(response.status_code, 403, ep)


@tagged('erpico_debranding')
class TestPatchMigrationParity(TransactionCase):
    """Verifica que la migración autocontenida y el parche compartan la misma configuración."""

    def _load_migration(self):
        migration_path = (
            Path(__file__).resolve().parents[1]
            / 'migrations' / '19.0.1.1.0' / 'post-migrate.py'
        )
        spec = importlib.util.spec_from_file_location(
            'post_migrate_parity', str(migration_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_replacements_parity(self):
        migration = self._load_migration()
        self.assertEqual(
            legacy_emails._REPLACEMENTS, migration._REPLACEMENTS,
            "_REPLACEMENTS mismatch between patch and migration")
        self.assertEqual(
            legacy_emails.LEGACY_EMAIL_XMLIDS, migration.LEGACY_EMAIL_XMLIDS,
            "LEGACY_EMAIL_XMLIDS mismatch between patch and migration")
        self.assertEqual(
            legacy_emails._POWERED_RE.pattern, migration._POWERED_RE.pattern,
            "_POWERED_RE pattern mismatch")
        self.assertEqual(
            legacy_emails._TOUR_RE.pattern, migration._TOUR_RE.pattern,
            "_TOUR_RE pattern mismatch")
        self.assertEqual(
            legacy_emails._MARKETING_RE.pattern, migration._MARKETING_RE.pattern,
            "_MARKETING_RE pattern mismatch")

    def test_patch_idempotent(self):
        """Segunda ejecución del parche no modifica nada."""
        from odoo.addons.erpico_debranding.patches.legacy_emails import (
            patch_legacy_emails)
        result = patch_legacy_emails(self.env)
        self.assertEqual(result, [], "Patch was not idempotent")