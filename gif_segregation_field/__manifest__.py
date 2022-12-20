# -*- coding: utf-8 -*-
{
    'name': "Gifan - campos de segregación",

    'summary': """
         Añadir campos de segregación""",

    'description': """
        Señalar campos de segregación
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'hr',
        'purchase',
        'sale',
        'account',
        'gif_sale_segregation',
        'gif_purchase_segregation'
    ],

    # always loaded
    'data': [
        'views/gif_purchase_order_views.xml',
        'views/gif_account_move_views.xml',
        'views/gif_account_payment_views.xml',
        'views/gif_account_batch_payment_views.xml'
    ],
    'assets':{
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
