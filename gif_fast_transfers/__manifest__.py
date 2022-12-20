# -*- coding: utf-8 -*-
{
    'name': "Gifan - Agilización de movimientos",

    'summary': """
         Agilización de movimientos - Gifan""",

    'description': """
        Modulo para agilizar las recepciones, entregas y traslados de inventario.
        
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'sale',
        'purchase',
        'stock',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/gif_fast_transfer_views.xml',
        'views/gif_stock_picking_inherit_views.xml',
        'views/gif_product_template_inherit_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
           'gif_fast_transfers/static/src/js/enter_like_tab_again.js'
       ]
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
