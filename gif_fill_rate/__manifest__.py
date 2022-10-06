{
    'name': "Gifan - Fill Rate",
    'version': '15.0.1',
    'depends': ['base', 'sale','stock','account', 'account_batch_payment'],
    'author': "Qualsys Consulting",
    'sumary' : "Campo para clientes con Fill Rate",
    'category': 'customization',
    'description': """
        Requerimientos que cumple:
        +RU-0059 Visualización de Fill Rate
    """,
    
    # data files always loaded at installation
    'data': [
        'views/gif_fill_rate_views.xml',
        'views/sale_order_views.xml',
        'views/gif_sale_order_views.xml',
        'views/gif_stock_picking_views.xml',
        'views/gif_stock_picking_batch_views.xml',
        'views/gif_stock_move_views.xml',
        'views/gif_stock_move_line_views.xml',
        'views/gif_account_move_views.xml',
        'views/gif_account_payment_views.xml',
        'views/gif_account_batch_payment_views.xml',
    ],
    
    
    # data files containing optionally loaded demonstration data
    'demo': [
        #'demo/demo_data.xml',
    ],
    
    
    'license': 'LGPL-3',
}
