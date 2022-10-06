{
    'name': "Gifan - Asociación de Pagos a Facturas",
    'version': '15.0.1',
    'depends': ['base','account'],
    'author': "Qualsys Consulting",
    'sumary' : "Asociación de Pagos a Facturas",
    'category': 'customization',
    'description': """
        Requerimientos que cumple:
        +RA-0001 Asociación de Pagos a Facturas
    """,
    
    # data files always loaded at installation
    'data': [
        'views/gif_account_payment_views.xml',
        'views/gif_account_payment_register_views.xml',
    ],
    
    
    # data files containing optionally loaded demonstration data
    'demo': [
        #'demo/demo_data.xml',
    ],
    
    
    'license': 'LGPL-3',
}
