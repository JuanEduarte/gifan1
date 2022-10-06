# -*- coding: utf-8 -*-
{
    'name': "Gifan - Segregación de flujos de negocio",

    'summary': """
         Clasificar y Segregar flujos de negocio - Gifan""",

    'description': """
        Requerimientos que cumple:
        +RU-0014 Clasificación y segregación de Facturas de compra.
        +RU-0015 Clasificación y segregación de Facturas de venta.
        +RU-0016 Clasificación y segregación de Notas de crédito de Facturas de compra.
        +RU-0017 Clasificación y segregación de Notas de crédito de Facturas de venta.
        +RU-0049 Clasificación y segregación de Pedidos de venta.
        +RU-0087 Clasificación y segregación de Pedidos de compra.
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
        'gif_purchase_segregation',
    ],

    # always loaded
    'data': [
        'views/gif_sale_order_inherit_views.xml',
        'views/gif_purchase_order_inherit_views.xml',
        'views/gif_account_move_inherit_views.xml',
        'views/gif_account_payment_inherit_views.xml',
    ],
    'assets':{
       'web.assets_backend':[
           'gif_segregate_flow/static/src/js/gif_segregate_cells.js'
       ]
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}