# -*- coding: utf-8 -*-
{
    'name': "Gifan - Agrupación de Rutas de entrega",

    'summary': """
        Agrupación de rutas de entrega - Gifan""",

    'description': """
        Requerimiento que cumple:
        +RU-106 
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gif_res_partner_inherit_views.xml',
        'views/gif_group_routes_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
