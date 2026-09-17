{
    'name': 'Erpico Debranding',
    'version': '19.0.1.1.0',
    'license': 'LGPL-3',
    'author': 'Erpico',
    'maintainer': 'Erpico',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from UI, emails and portal (Odoo 19)',
    'depends': [
        'web',
        'base_setup',
        'portal',
        'mail',
        'auth_signup',
        'payment',
    ],
    'data': [
        'data/ir_ui_menu.xml',
        'views/templates.xml',
        'views/emails.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'erpico_debranding/static/src/js/user_menu.js',
            'erpico_debranding/static/src/scss/debranding.scss',
            'erpico_debranding/static/src/settings_form_view/res_config_edition.xml',
        ],
        'web.assets_frontend': [
            'erpico_debranding/static/src/scss/debranding.scss',
        ],
    },
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}