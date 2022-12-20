# -*- coding: utf-8 -*-
{
    'name': "Gifan - Proveedores de timbrado",
    'summary': """Módulo para implementar nuevos proveedores de timbrado.""",
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
        # 'l10n_mx_edi_40',
        'l10n_mx_edi',
        # 'account_edi',
        # 'l10n_mx',
        # 'base_vat',
        # 'gif_sale_segregation',
        # 'gif_purchase_segregation',
        # 'gif_firm_desactivation'
        ],
    'data':[
        'views/gif_res_partner_inherit_view.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}