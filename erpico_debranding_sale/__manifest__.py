{
    'name': 'Erpico Sale Debranding',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from sale/purchase portals',
    'description': 'Hides the "Connect with your software!" EDI button and modal on sale/purchase portal pages (Odoo 19).',
    'author': 'Erpico',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': ['erpico_debranding', 'sale', 'purchase'],
    'data': [
        'views/sale_portal_templates.xml',
    ],
}