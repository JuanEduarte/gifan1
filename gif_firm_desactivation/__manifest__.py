# -*- coding: utf-8 -*-
{
    'name': 'Gifan - Desactivación de timbrado',
    'version': '15.0.1',
    'summary': 'Desactiva timbrado para facturas',
    'description': '''
        Se indica en un checkbox si la factura se timbra o no con el cron.
        También los complementos de pago si es PPD.
    ''',
    'category': 'Accounting',
    'author': "Qualsys",
    'website': "http://www.qualsys.com.mx",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'account_accountant',
        'account_edi',
        'l10n_mx',
        'base_vat',
        'product_unspsc'
	],
    'data': [
        'views/gif_account_move_form.xml'
    ],
    'installable': True,
    'application': True,
    
}
