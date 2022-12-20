# -*- coding: utf-8 -*-
{
    'name': "Gifan - Reporte Anual de Ventas por Importes",

    'summary': """
        Gifan""",

    'description': """
        lorem
    """,

    'author': "Qualsys Consulting",
    'category': '',
    'version': '15.0.1',
    'depends': [
        'base', 'sale','gif_sale_segregation'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/gif_reports_params_view.xml'
    ],
    'assets': {
    },
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
