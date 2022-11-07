# -*- coding: utf-8 -*-
{
    'name': "Gifan - Búsqueda de productos",
    'summary': """Se agrega funcionalidad en la búsqueda de los productos.""",
    'description': """
        Permite que los productos se puedan buscan por el código de barras o código individual del cliente.
    """,

    'author': "Qualsys Consulting",
    'website': "https://www.qualsys.com.mx",
    # 'category': 'Customization',
    'version': '15.0.1',
    'depends': [
        'base',
        'sale',
        'gif_sale_segregation',
        ],

    'data': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}