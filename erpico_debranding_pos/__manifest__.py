{
    'name': 'Erpico POS Debranding',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from POS receipts',
    'description': """
Reemplaza la línea "Powered by Odoo" por "Powered by ERPICO" en el recibo de
venta de punto de venta (POS) de Odoo 19.
    """,
    'author': 'ERPICO, Santiago Vásquez',
    'website': 'https://github.com/Vankisito/DebrandingERPICO',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets_prod': [
            'erpico_debranding_pos/static/src/override/order_receipt.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
}