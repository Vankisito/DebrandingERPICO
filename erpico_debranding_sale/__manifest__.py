{
    'name': 'Erpico Sale Debranding',
    'version': '19.0.1.0.1',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from sale/purchase portals',
    'description': """
Extiende la suite `erpico_debranding` al portal de ventas y compras: oculta
el botón "Connect with your software!" y su modal sobre las cotizaciones y
órdenes de compra publicadas en el portal (Odoo 19).
    """,
    'author': 'Habitat Digital',
    'website': 'https://github.com/Vankisito/DebrandingERPICO',
    'license': 'LGPL-3',
    'depends': ['erpico_debranding', 'sale', 'purchase'],
    'data': [
        'views/sale_portal_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
}