{
    'name': 'Erpico POS Debranding',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from POS receipts',
    'description': 'Replaces "Powered by Odoo" with "Powered by ERPICO" on POS sale receipts (Odoo 19).',
    'author': 'Erpico',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets_prod': [
            'erpico_debranding_pos/static/src/override/order_receipt.xml',
        ],
    },
}