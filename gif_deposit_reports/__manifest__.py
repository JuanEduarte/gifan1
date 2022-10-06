
{
    'name': "Gifan - Reportes de ingresos.",
    'version': '15.0.1',
    'depends': ['base',
                'sale',
    ],
    'author': 'Qualsys Consulting',
    'category': 'Customizations',
    'description': """
        Módulo para hacer reportes de ingresos.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/gif_diary_sales_report_view.xml',
        'views/gif_goals_view.xml',
    ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3'
}