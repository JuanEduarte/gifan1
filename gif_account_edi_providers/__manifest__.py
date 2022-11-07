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
        'base',
        'account',
        'gif_sale_segregation',
        'gif_purchase_segregation',
        ],
    'data': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}