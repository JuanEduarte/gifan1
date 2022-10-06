# -*- coding: utf-8 -*-
{
    'name': "Gifan - Inventario Ciclico",

    'summary': """
         Realización del inventario Ciclico - Gifan""",

    'description': """
        Requerimientos que cumple:
        
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'stock_barcode',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/gif_cyc_inventory_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
           'gif_cyclical_inventory/static/src/js/enter_like_tab.js'
       ]
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
