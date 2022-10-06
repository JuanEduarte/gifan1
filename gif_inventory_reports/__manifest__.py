
{
    'name': "Gifan - Reportes de inventario.",
    'version': '15.0.1',
    'depends': ['base',
                'stock',
                'gif_sale_autorization',
    ],
    'author': 'Qualsys Consulting',
    'category': 'Customizations',
    'description': """
        Módulo para hacer reportes del inventario.
    """,
    'data': [
        'security/ir.model.access.csv',
        # 'views/gif_base_report_view.xml',
        'views/gif_existences_report_view.xml',
        'views/gif_inventory_report_view.xml',
        'views/gif_locations_report_view.xml',
        'views/gif_expiration_date_report_view.xml',
        'views/gif_details_expiration_date_report_view.xml',
        'views/gif_invoice_expiration_report_view.xml',
        'views/gif_warehouse_report_view.xml',
        'views/gif_brand_report_view.xml',
    ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3'
}