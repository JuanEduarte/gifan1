# -*- coding: utf-8 -*-
{
    'name': "Gifan - Punto de control Calidad",

    'summary': """
        Punto de control en las alertas de calidad""",

    'description': """
        Requerimientos que cumple:
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'website': "http://www.qualsys.com.mx",

    'depends': [
        'base',
        'quality_control',
        'gif_sale_autorization',
    ],

    # always loaded
    'data': [
        'views/gif_quality_point_inherit_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
