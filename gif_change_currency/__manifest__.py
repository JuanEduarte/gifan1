# -*- coding: utf-8 -*-
{
    'name': "Gifan - Tipo de cambio",

    'summary': """
        Moneda de cambio personalizada""",

    'description': """
        Requerimientos que cumple:
        
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'sale',
        'gif_purchase_segregation',
        
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/gif_sale_order_inherit_views.xml',
        'views/gif_purchase_order_inherit_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
