import re

_POWERED_RE = re.compile(r'Powered by <a[^>]*>Odoo</a>')
_TOUR_RE = re.compile(r'<a[^>]*>Odoo Tour</a>')
_MARKETING_RE = re.compile(
    r'Never heard of Odoo\?.*?increase your productivity\.\s*',
    flags=re.S,
)

_REPLACEMENTS = (
    ('invites you to connect to Odoo', 'invites you to connect to ERPICO'),
    ('Welcome to Odoo', 'Welcome to ERPICO'),
    ('>OdooBot</t>', '>Your administrator</t>'),
    ('to connect on Odoo.', 'to connect on ERPICO.'),
    ('Your Odoo domain is:', 'Your domain is:'),
    ('>http://yourcompany.odoo.com</a>', '>http://yourcompany.example.com</a>'),
    ('Enjoy Odoo!', 'Enjoy ERPICO!'),
)

LEGACY_EMAIL_XMLIDS = (
    'auth_signup.set_password_email',
    'auth_signup.portal_set_password_email',
    'auth_signup.mail_template_data_unregistered_users',
    'auth_signup.mail_template_user_signup_account_created',
)


def _clean(html):
    html = str(html)  # bypass markupsafe.Markup.replace quirk
    for old, new in _REPLACEMENTS:
        html = html.replace(old, new)
    html = _MARKETING_RE.sub('', html)
    html = _TOUR_RE.sub('ERPICO guide', html)
    return _POWERED_RE.sub('Powered by <b>ERPICO</b>', html)


def patch_legacy_emails(env):
    patched = []
    for xmlid in LEGACY_EMAIL_XMLIDS:
        rec = env.ref(xmlid, raise_if_not_found=False)
        if not rec or not rec.body_html:
            continue
        new_body = _clean(rec.body_html)
        if new_body != str(rec.body_html):
            rec.write({'body_html': new_body})
            patched.append(xmlid)
    bots = env['res.partner'].search(
        [('name', '=', 'OdooBot'), ('active', 'in', (True, False))])
    if bots:
        bots.write({'name': 'ERPICO Assistant'})
        patched.append('res.partner OdooBot -> ERPICO Assistant')
    return patched