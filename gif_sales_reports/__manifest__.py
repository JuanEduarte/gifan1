
{
    'name': "Gifan - Reportes de ingresos.",
    'version': '15.0.1',
    'depends': ['base',
                'sale',
                'gif_big_tables_reports',
                'gif_sale_segregation',
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
        'wizard/gif_reports_params_view.xml'
        # 'views/gif_account_move_reversal_views_inherit.xml'        
    ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3'
}