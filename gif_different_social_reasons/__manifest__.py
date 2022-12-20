# -*- coding: utf-8 -*-
{
    'name': "Gifan - Clientes con diferentes razones sociales",

    'summary': """
        Agrupación de clientes - Gifan""",

    'description': """
        Requerimiento que cumple:
        +RU-106 Cliente con diferentes razones sociales.
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'sale',
        'account',
    ],

    # always loaded
    'data': [
        'wizard/wizard_show_groups_views.xml',
        'security/ir.model.access.csv',
        'views/gif_groups_views.xml',
        'views/gif_res_partner_inherit_views.xml',
        'views/gif_sale_order_inherit_views.xml',
        'views/gif_purchase_order_inherit_views.xml',
        'views/gif_account_move_inherit_views.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'gif_different_social_reasons/static/src/js/gif_hide_button.js'
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
