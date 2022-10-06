# -*- coding: utf-8 -*-
{
    'name': "Gifan - Reportes de Ingresos y Egresos",

    'summary': """
        Establecer una serie de Informes / Reportes de los flujos transaccionales de Ingresos y Egresos - Gifan""",

    'description': """
        lorem
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/articulos_ubicaciones_views.xml'
    ],
    'assets':{
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
