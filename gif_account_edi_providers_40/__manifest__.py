# -*- coding: utf-8 -*-
{
    'name': "Gifan - Proveedores de timbrado 4.0",
    'summary': """Módulo para implementar nuevos proveedores de timbrado 4.0.""",
    'description': """
        Desarrollo de los siguientes requerimientos:
        RA-0006 Cambio de proveedor de timbrado
        RA-0003 Control en timbrado de Facturas de venta
    """,
    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    'category': 'Stock',
    'version': '15.0.1',
    'depends': [
        # 'base',
        'account',
        'l10n_mx_edi_40',
        #'l10n_mx_edi',
        # 'account_edi',
        # 'l10n_mx',
        # 'base_vat',
        # 'gif_sale_segregation',
        # 'gif_purchase_segregation',
        'gif_account_edi_providers',
        'gif_firm_desactivation'
        ],
    'data':[
        'data/4.0/cfdi.xml',
        # 'data/4.0/payment20.xml',
        # 'data/account_edi_data.xml'
        'views/gif_res_partner_inherit_view.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}